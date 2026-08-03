import logging
import smtplib
import json
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import timezone, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import ABC, abstractmethod

import httpx

logger = logging.getLogger(__name__)


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class NotificationProvider(ABC):
    @abstractmethod
    async def send(self, recipient: str, subject: str, message: str) -> bool:
        pass


class EmailProvider(NotificationProvider):
    def __init__(self, smtp_host: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logger.info(f"Email sent to {recipient}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            return False


class WebhookProvider(NotificationProvider):
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}
        self.timeout = timeout

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            payload = {
                "recipient": recipient,
                "subject": subject,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(self.url, json=payload, headers=self.headers)
                if resp.status_code < 300:
                    logger.info(f"Webhook delivered to {self.url} for {recipient}")
                    return True
                logger.warning(f"Webhook returned {resp.status_code} for {self.url}: {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Webhook delivery failed to {self.url}: {e}")
            return False


class SMSProvider(NotificationProvider):
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
            payload = {
                "From": self.from_number,
                "To": recipient,
                "Body": f"{subject}\n\n{message}",
            }
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    url,
                    data=payload,
                    auth=(self.account_sid, self.auth_token),
                )
                if resp.status_code in (200, 201):
                    logger.info(f"SMS sent to {recipient}: {subject}")
                    return True
                logger.warning(f"Twilio returned {resp.status_code}: {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Failed to send SMS to {recipient}: {e}")
            return False


class PushProvider(NotificationProvider):
    def __init__(self, service_account_key: Optional[Dict] = None):
        self.service_account_key = service_account_key
        self._client = None

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            if not self.service_account_key:
                logger.debug(f"Push notification skipped (no FCM key): {recipient} - {subject}")
                return True

            payload = {
                "message": {
                    "token": recipient,
                    "notification": {"title": subject, "body": message},
                }
            }
            async with httpx.AsyncClient(timeout=10) as client:
                url = f"https://fcm.googleapis.com/v1/projects/{self.service_account_key.get('project_id', '')}/messages:send"
                headers = {
                    "Authorization": f"Bearer {self.service_account_key.get('access_token', '')}",
                    "Content-Type": "application/json",
                }
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code < 300:
                    logger.info(f"Push notification sent to {recipient}: {subject}")
                    return True
                logger.warning(f"FCM returned {resp.status_code}: {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Failed to send push notification to {recipient}: {e}")
            return False


class InAppProvider(NotificationProvider):
    def __init__(self):
        self.notifications: Dict[str, List[Dict[str, Any]]] = {}

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            if recipient not in self.notifications:
                self.notifications[recipient] = []
            self.notifications[recipient].append({
                "subject": subject,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "read": False,
            })
            logger.info(f"In-app notification created for {recipient}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to create in-app notification for {recipient}: {e}")
            return False

    def get_unread(self, user_id: str) -> List[Dict[str, Any]]:
        notifications = self.notifications.get(user_id, [])
        return [n for n in notifications if not n.get("read", False)]

    def get_all(self, user_id: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        all_notifs = self.notifications.get(user_id, [])
        unread_count = sum(1 for n in all_notifs if not n.get("read", False))
        total = len(all_notifs)
        items = list(reversed(all_notifs))[offset:offset + limit]
        return {
            "notifications": items,
            "total": total,
            "unread_count": unread_count,
        }

    def mark_read(self, user_id: str, index: Optional[int] = None) -> bool:
        if user_id not in self.notifications:
            return False
        if index is not None:
            notifs = self.notifications[user_id]
            real_idx = len(notifs) - 1 - index if index < len(notifs) else None
            if real_idx is not None and real_idx < len(notifs):
                notifs[real_idx]["read"] = True
                return True
            return False
        for n in self.notifications[user_id]:
            n["read"] = True
        return True

    def clear(self, user_id: str) -> int:
        count = len(self.notifications.get(user_id, []))
        self.notifications[user_id] = []
        return count


class NotificationService:
    def __init__(self):
        self.providers: Dict[NotificationChannel, Optional[NotificationProvider]] = {
            NotificationChannel.EMAIL: None,
            NotificationChannel.SMS: None,
            NotificationChannel.PUSH: None,
            NotificationChannel.IN_APP: InAppProvider(),
            NotificationChannel.WEBHOOK: None,
        }
        self.notification_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, List[NotificationChannel]] = {}

    def register_provider(self, channel: NotificationChannel, provider: NotificationProvider):
        self.providers[channel] = provider
        logger.info(f"Registered {channel.value} provider")

    def set_user_preferences(self, user_id: str, channels: List[NotificationChannel]):
        self.user_preferences[user_id] = channels
        logger.info(f"Updated notification preferences for {user_id}")

    def get_user_preferences(self, user_id: str) -> List[NotificationChannel]:
        return self.user_preferences.get(user_id, [NotificationChannel.IN_APP])

    def get_in_app_provider(self) -> InAppProvider:
        return self.providers[NotificationChannel.IN_APP]

    async def send_alert_notification(
        self,
        user_id: str,
        alert_id: str,
        alert_type: str,
        ticker: Optional[str],
        message: str,
        severity: str = "info",
    ) -> Dict[str, bool]:
        subject = f"Miau Alert: {alert_type.upper()} - {ticker or 'Portfolio'}"
        if severity in ("warning", "critical"):
            subject = f"⚠️ {subject}" if severity == "warning" else f"🚨 {subject}"
        results = {}
        channels = self.get_user_preferences(user_id)

        for channel in channels:
            provider = self.providers[channel]
            if not provider:
                logger.debug(f"Provider for {channel.value} not registered, skipping")
                results[channel.value] = False
                continue

            try:
                success = await provider.send(user_id, subject, message)
                results[channel.value] = success

                self.notification_history.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "user_id": user_id,
                    "alert_id": alert_id,
                    "channel": channel.value,
                    "status": "sent" if success else "failed",
                    "message": message,
                    "severity": severity,
                })
            except Exception as e:
                logger.error(f"Error sending {channel.value} notification to {user_id}: {e}")
                results[channel.value] = False

        return results

    async def send_custom_notification(
        self,
        user_id: str,
        subject: str,
        message: str,
        channels: Optional[List[NotificationChannel]] = None,
    ) -> Dict[str, bool]:
        target_channels = channels or self.get_user_preferences(user_id)
        results = {}

        for channel in target_channels:
            provider = self.providers[channel]
            if not provider:
                logger.warning(f"Provider for {channel.value} not registered")
                results[channel.value] = False
                continue

            try:
                success = await provider.send(user_id, subject, message)
                results[channel.value] = success
            except Exception as e:
                logger.error(f"Error sending {channel.value} notification: {e}")
                results[channel.value] = False

        return results

    def get_notification_history(
        self,
        user_id: Optional[str] = None,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        cutoff_date = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        history = [
            h for h in self.notification_history
            if h["timestamp"] >= cutoff_date
        ]
        if user_id:
            history = [h for h in history if h["user_id"] == user_id]
        return history


def init_notification_service() -> NotificationService:
    from app.config import settings

    svc = NotificationService()

    if settings.smtp_host and settings.smtp_port and settings.smtp_sender_email and settings.smtp_sender_password:
        svc.register_provider(
            NotificationChannel.EMAIL,
            EmailProvider(
                smtp_host=settings.smtp_host,
                smtp_port=settings.smtp_port,
                sender_email=settings.smtp_sender_email,
                sender_password=settings.smtp_sender_password,
            ),
        )
        logger.info("Email provider registered")

    if settings.webhook_notification_url:
        svc.register_provider(
            NotificationChannel.WEBHOOK,
            WebhookProvider(
                url=settings.webhook_notification_url,
                headers=settings.webhook_headers if hasattr(settings, 'webhook_headers') else None,
            ),
        )
        logger.info(f"Webhook provider registered: {settings.webhook_notification_url}")

    if settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_from_number:
        svc.register_provider(
            NotificationChannel.SMS,
            SMSProvider(
                account_sid=settings.twilio_account_sid,
                auth_token=settings.twilio_auth_token,
                from_number=settings.twilio_from_number,
            ),
        )
        logger.info("SMS (Twilio) provider registered")

    return svc


# ── WhatsApp Provider (9.3.10) ──

class WhatsAppProvider(NotificationProvider):
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
            payload = {
                "From": f"whatsapp:{self.from_number}",
                "To": f"whatsapp:{recipient}",
                "Body": f"*{subject}*\n\n{message}",
            }
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(url, data=payload, auth=(self.account_sid, self.auth_token))
                if resp.status_code in (200, 201):
                    logger.info(f"WhatsApp sent to {recipient}: {subject}")
                    return True
                logger.warning(f"Twilio WhatsApp returned {resp.status_code}: {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Failed to send WhatsApp to {recipient}: {e}")
            return False


# ── Telegram Bot Provider (9.3.11) ──

class TelegramProvider(NotificationProvider):
    def __init__(self, bot_token: str, webhook_url: Optional[str] = None):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.webhook_url = webhook_url

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        try:
            text = f"*{subject}*\n\n{message}"
            payload = {
                "chat_id": recipient,
                "text": text,
                "parse_mode": "Markdown",
            }
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(f"{self.base_url}/sendMessage", json=payload)
                if resp.status_code == 200:
                    logger.info(f"Telegram sent to {recipient}: {subject}")
                    return True
                logger.warning(f"Telegram returned {resp.status_code}: {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Failed to send Telegram to {recipient}: {e}")
            return False

    async def set_webhook(self) -> bool:
        if not self.webhook_url:
            return False
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(f"{self.base_url}/setWebhook", json={"url": self.webhook_url})
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Failed to set Telegram webhook: {e}")
            return False

    async def handle_update(self, update: dict) -> Optional[str]:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        if not chat_id or not text:
            return None
        if text == "/start":
            welcome = (
                "🐱 *Welcome to Miau Finance Bot!*\n\n"
                "Get real-time alerts on your portfolio.\n"
                "Commands:\n"
                "/subscribe — Enable notifications\n"
                "/unsubscribe — Disable notifications\n"
                "/price AAPL — Check a price\n"
                "/help — All commands"
            )
            await self.send(str(chat_id), "Miau Finance Bot", welcome)
            return str(chat_id)
        if text.lower().startswith("/price"):
            ticker = text.split(" ", 1)[1].upper() if " " in text else "AAPL"
            return f"PRICE:{ticker}:{chat_id}"
        if text == "/subscribe":
            return f"SUBSCRIBE:{chat_id}"
        if text == "/unsubscribe":
            return f"UNSUBSCRIBE:{chat_id}"
        return None


# ── VAPID Keys & Push Subscription (9.3.2, 9.3.3) ──

import base64
from cryptography.fernet import Fernet


def generate_vapid_keys() -> dict:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    def _to_urlsafe(key_bytes: bytes) -> str:
        return base64.urlsafe_b64encode(key_bytes).rstrip(b"=").decode()
    return {
        "public_key": _to_urlsafe(
            public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
        ),
        "private_key": _to_urlsafe(
            private_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
        ),
    }


class PushSubscriptionManager:
    def __init__(self):
        self._subscriptions: dict[str, list[dict]] = {}

    def subscribe(self, user_id: str, subscription: dict) -> bool:
        if user_id not in self._subscriptions:
            self._subscriptions[user_id] = []
        existing = [s for s in self._subscriptions[user_id] if s.get("endpoint") == subscription.get("endpoint")]
        if not existing:
            self._subscriptions[user_id].append(subscription)
            logger.info(f"Push subscription added for {user_id}")
        return True

    def unsubscribe(self, user_id: str, endpoint: str) -> bool:
        if user_id in self._subscriptions:
            self._subscriptions[user_id] = [s for s in self._subscriptions[user_id] if s.get("endpoint") != endpoint]
            logger.info(f"Push subscription removed for {user_id}")
            return True
        return False

    def get_subscriptions(self, user_id: str) -> list[dict]:
        return self._subscriptions.get(user_id, [])

    def get_all_subscriptions(self) -> dict[str, list[dict]]:
        return dict(self._subscriptions)


push_subscriptions = PushSubscriptionManager()


async def send_web_push(user_id: str, title: str, body: str, icon: str = "/icons/icon-192.svg") -> bool:
    subs = push_subscriptions.get_subscriptions(user_id)
    if not subs:
        logger.debug(f"No push subscriptions for {user_id}")
        return False
    success = False
    for sub in subs:
        try:
            payload = json.dumps({"title": title, "body": body, "icon": icon, "badge": icon})
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    sub["endpoint"],
                    json=payload,
                    headers={
                        "TTL": "86400",
                        "Content-Type": "application/json",
                        "Content-Encoding": "aes128gcm",
                    },
                )
                if resp.status_code < 300 or resp.status_code == 410:
                    success = True
                    if resp.status_code == 410:
                        push_subscriptions.unsubscribe(user_id, sub["endpoint"])
        except Exception as e:
            logger.error(f"Web push failed for {user_id}: {e}")
    return success


# ── Rich Push Notifications (9.3.15) ──

class RichPushBuilder:
    @staticmethod
    def price_alert(ticker: str, price: float, change_pct: float, target: float) -> dict:
        direction = "📈" if change_pct >= 0 else "📉"
        return {
            "title": f"{direction} {ticker} Price Alert",
            "body": f"{ticker} is at ${price:.2f} ({change_pct:+.2f}%)\nTarget: ${target:.2f}",
            "data": {"type": "price_alert", "ticker": ticker, "price": price, "target": target},
            "icon": "/icons/icon-192.svg",
        }

    @staticmethod
    def trade_confirmation(ticker: str, side: str, quantity: float, price: float) -> dict:
        emoji = "🟢" if side.upper() == "BUY" else "🔴"
        return {
            "title": f"{emoji} Trade {side.title()}",
            "body": f"{side.upper()} {quantity} {ticker} @ ${price:.2f}",
            "data": {"type": "trade", "ticker": ticker, "side": side, "quantity": quantity, "price": price},
            "icon": "/icons/icon-192.svg",
        }

    @staticmethod
    def daily_summary(portfolio_value: float, pnl: float, top_ticker: str, trade_count: int) -> dict:
        emoji = "😸" if pnl >= 0 else "😿"
        return {
            "title": f"{emoji} Daily Portfolio Summary",
            "body": (
                f"Portfolio: ${portfolio_value:,.2f}\n"
                f"P&L: {pnl:+,.2f}\n"
                f"Top mover: {top_ticker}\n"
                f"Trades today: {trade_count}"
            ),
            "data": {"type": "daily_summary", "portfolio_value": portfolio_value, "pnl": pnl},
            "icon": "/icons/icon-192.svg",
        }


# ── Smart Notification Scheduling (9.3.12) ──

class NotificationScheduler:
    def __init__(self):
        self._scheduled: list[dict] = []
        self._quiet_hours: dict[str, tuple[int, int]] = {}

    def set_quiet_hours(self, user_id: str, start_hour: int, end_hour: int):
        self._quiet_hours[user_id] = (start_hour, end_hour)

    def is_quiet_hours(self, user_id: str) -> bool:
        if user_id not in self._quiet_hours:
            return False
        now_hour = datetime.now(timezone.utc).hour
        start, end = self._quiet_hours[user_id]
        if start <= end:
            return start <= now_hour < end
        return now_hour >= start or now_hour < end

    def should_deliver(self, user_id: str) -> bool:
        return not self.is_quiet_hours(user_id)

    def schedule(self, user_id: str, channel: str, subject: str, message: str, deliver_at: datetime) -> str:
        import uuid
        notif_id = str(uuid.uuid4())
        self._scheduled.append({
            "id": notif_id,
            "user_id": user_id,
            "channel": channel,
            "subject": subject,
            "message": message,
            "deliver_at": deliver_at.isoformat(),
            "delivered": False,
        })
        logger.info(f"Scheduled notification {notif_id} for {user_id} at {deliver_at}")
        return notif_id

    def get_pending(self) -> list[dict]:
        now = datetime.now(timezone.utc).isoformat()
        return [n for n in self._scheduled if not n["delivered"] and n["deliver_at"] <= now]

    def mark_delivered(self, notif_id: str) -> bool:
        for n in self._scheduled:
            if n["id"] == notif_id:
                n["delivered"] = True
                return True
        return False


notification_scheduler = NotificationScheduler()


# ── Notification History (9.3.13) ──

class NotificationHistory:
    def __init__(self, max_size: int = 10000):
        self._history: list[dict] = []
        self._max_size = max_size

    def record(self, entry: dict):
        self._history.append(entry)
        if len(self._history) > self._max_size:
            self._history = self._history[-self._max_size:]

    def query(self, user_id: Optional[str] = None, channel: Optional[str] = None,
              notif_type: Optional[str] = None, days: int = 30,
              limit: int = 100, offset: int = 0) -> dict:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        results = [h for h in self._history if h.get("timestamp", "") >= cutoff]
        if user_id:
            results = [h for h in results if h.get("user_id") == user_id]
        if channel:
            results = [h for h in results if h.get("channel") == channel]
        if notif_type:
            results = [h for h in results if h.get("type") == notif_type]
        total = len(results)
        items = list(reversed(results))[offset:offset + limit]
        return {"items": items, "total": total, "offset": offset, "limit": limit}

    def get_stats(self, days: int = 7) -> dict:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        recent = [h for h in self._history if h.get("timestamp", "") >= cutoff]
        by_channel: dict[str, int] = {}
        by_type: dict[str, int] = {}
        for h in recent:
            ch = h.get("channel", "unknown")
            by_channel[ch] = by_channel.get(ch, 0) + 1
            tp = h.get("type", "unknown")
            by_type[tp] = by_type.get(tp, 0) + 1
        return {
            "period_days": days,
            "total": len(recent),
            "by_channel": by_channel,
            "by_type": by_type,
        }


notification_history = NotificationHistory()


# ── Price Alert & Trade Push (9.3.4, 9.3.5) ──

async def send_price_alert_push(user_id: str, ticker: str, price: float, change_pct: float, target: float) -> bool:
    if notification_scheduler.is_quiet_hours(user_id):
        logger.debug(f"Quiet hours for {user_id}, deferring price alert")
        return False
    rich = RichPushBuilder.price_alert(ticker, price, change_pct, target)
    success = await send_web_push(user_id, rich["title"], rich["body"])
    notification_history.record({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "channel": "push",
        "type": "price_alert",
        "status": "sent" if success else "failed",
        "data": {"ticker": ticker, "price": price, "target": target},
    })
    return success


async def send_trade_push(user_id: str, ticker: str, side: str, quantity: float, price: float) -> bool:
    rich = RichPushBuilder.trade_confirmation(ticker, side, quantity, price)
    success = await send_web_push(user_id, rich["title"], rich["body"])
    notification_history.record({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "channel": "push",
        "type": "trade",
        "status": "sent" if success else "failed",
        "data": {"ticker": ticker, "side": side, "quantity": quantity, "price": price},
    })
    return success


# ── Daily Summary (9.3.7) ──

async def send_daily_summary_push(user_id: str, portfolio_value: float, pnl: float,
                                   top_ticker: str = "N/A", trade_count: int = 0) -> bool:
    rich = RichPushBuilder.daily_summary(portfolio_value, pnl, top_ticker, trade_count)
    success = await send_web_push(user_id, rich["title"], rich["body"])
    notification_history.record({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "channel": "push",
        "type": "daily_summary",
        "status": "sent" if success else "failed",
        "data": {"portfolio_value": portfolio_value, "pnl": pnl},
    })
    return success


notification_service = NotificationService()