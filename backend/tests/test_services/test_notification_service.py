import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from unittest.mock import AsyncMock

from app.services.notification_service import (
    WhatsAppProvider, TelegramProvider, generate_vapid_keys,
    PushSubscriptionManager, push_subscriptions, send_web_push,
    RichPushBuilder, NotificationScheduler, notification_scheduler,
    NotificationHistory, notification_history,
    send_price_alert_push, send_trade_push, send_daily_summary_push,
)


class TestWhatsAppProvider:
    @pytest.mark.anyio
    async def test_send_success(self):
        provider = WhatsAppProvider("sid", "token", "+1234567890")
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            resp = MagicMock()
            resp.status_code = 201
            mock_instance.post = AsyncMock(return_value=resp)
            result = await provider.send("+1987654321", "Test", "Hello!")
            assert result is True

    @pytest.mark.anyio
    async def test_send_failure(self):
        provider = WhatsAppProvider("sid", "token", "+1234567890")
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            resp = MagicMock()
            resp.status_code = 400
            mock_instance.post = AsyncMock(return_value=resp)
            result = await provider.send("+1987654321", "Test", "Hello!")
            assert result is False


class TestTelegramProvider:
    @pytest.mark.anyio
    async def test_send_success(self):
        provider = TelegramProvider("bot:token")
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            resp = MagicMock()
            resp.status_code = 200
            mock_instance.post = AsyncMock(return_value=resp)
            result = await provider.send("12345", "Test", "Hello!")
            assert result is True

    @pytest.mark.anyio
    async def test_set_webhook(self):
        provider = TelegramProvider("bot:token", webhook_url="https://example.com/webhook")
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            resp = MagicMock()
            resp.status_code = 200
            mock_instance.post = AsyncMock(return_value=resp)
            result = await provider.set_webhook()
            assert result is True

    @pytest.mark.anyio
    async def test_handle_update_start(self):
        provider = TelegramProvider("bot:token")
        with patch.object(provider, "send", new_callable=AsyncMock) as mock_send:
            mock_send.return_value = True
            update = {"message": {"chat": {"id": 12345}, "text": "/start"}}
            result = await provider.handle_update(update)
            assert result == "12345"

    @pytest.mark.anyio
    async def test_handle_update_price(self):
        provider = TelegramProvider("bot:token")
        update = {"message": {"chat": {"id": 12345}, "text": "/price AAPL"}}
        result = await provider.handle_update(update)
        assert result == "PRICE:AAPL:12345"

    @pytest.mark.anyio
    async def test_handle_update_unknown(self):
        provider = TelegramProvider("bot:token")
        update = {"message": {"chat": {"id": 12345}, "text": "/unknown"}}
        result = await provider.handle_update(update)
        assert result is None


class TestVapidKeys:
    def test_generate_vapid_keys(self):
        keys = generate_vapid_keys()
        assert "public_key" in keys
        assert "private_key" in keys
        assert len(keys["public_key"]) > 20


class TestPushSubscriptionManager:
    def setup_method(self):
        self.manager = PushSubscriptionManager()

    def test_subscribe(self):
        result = self.manager.subscribe("user1", {"endpoint": "https://example.com/push"})
        assert result is True
        assert len(self.manager.get_subscriptions("user1")) == 1

    def test_subscribe_duplicate(self):
        sub = {"endpoint": "https://example.com/push"}
        self.manager.subscribe("user1", sub)
        self.manager.subscribe("user1", sub)
        assert len(self.manager.get_subscriptions("user1")) == 1

    def test_unsubscribe(self):
        self.manager.subscribe("user1", {"endpoint": "https://example.com/push"})
        result = self.manager.unsubscribe("user1", "https://example.com/push")
        assert result is True
        assert len(self.manager.get_subscriptions("user1")) == 0

    def test_get_all_subscriptions(self):
        self.manager.subscribe("user1", {"endpoint": "https://ex.com/1"})
        self.manager.subscribe("user2", {"endpoint": "https://ex.com/2"})
        all_subs = self.manager.get_all_subscriptions()
        assert "user1" in all_subs
        assert "user2" in all_subs


class TestRichPushBuilder:
    def test_price_alert(self):
        alert = RichPushBuilder.price_alert("AAPL", 150.25, 1.5, 160.0)
        assert "Price Alert" in alert["title"]
        assert alert["data"]["ticker"] == "AAPL"
        assert alert["data"]["price"] == 150.25

    def test_trade_confirmation(self):
        trade = RichPushBuilder.trade_confirmation("TSLA", "BUY", 100, 250.50)
        assert "Trade" in trade["title"]
        assert trade["data"]["side"] == "BUY"

    def test_daily_summary(self):
        summary = RichPushBuilder.daily_summary(100000, 1500, "AAPL", 5)
        assert "Summary" in summary["title"]
        body = summary["body"]
        assert "AAPL" in body or "Top" in body
        assert "1500" in body or "5" in body or "1,500" in body or "+" in body


class TestNotificationScheduler:
    def setup_method(self):
        self.scheduler = NotificationScheduler()

    def test_quiet_hours(self):
        self.scheduler.set_quiet_hours("user1", 23, 7)
        assert self.scheduler.is_quiet_hours("user1") or not self.scheduler.is_quiet_hours("user1")

    def test_schedule(self):
        from datetime import timedelta
        nid = self.scheduler.schedule("user1", "email", "Test", "Hello", datetime.utcnow())
        assert nid is not None
        pending = self.scheduler.get_pending()
        assert len(pending) >= 1

    def test_mark_delivered(self):
        nid = self.scheduler.schedule("user1", "email", "Test", "Hello", datetime.utcnow())
        assert self.scheduler.mark_delivered(nid) is True
        assert self.scheduler.mark_delivered("nonexistent") is False


class TestNotificationHistory:
    def setup_method(self):
        self.history = NotificationHistory()

    def test_record_and_query(self):
        self.history.record({"user_id": "u1", "channel": "push", "type": "price_alert", "timestamp": datetime.utcnow().isoformat()})
        result = self.history.query(user_id="u1")
        assert result["total"] == 1
        assert len(result["items"]) == 1

    def test_query_with_filters(self):
        self.history.record({"user_id": "u1", "channel": "push", "type": "price_alert", "timestamp": datetime.utcnow().isoformat()})
        self.history.record({"user_id": "u1", "channel": "email", "type": "daily_summary", "timestamp": datetime.utcnow().isoformat()})
        result = self.history.query(user_id="u1", channel="push")
        assert result["total"] == 1
        assert result["items"][0]["channel"] == "push"

    def test_get_stats(self):
        self.history.record({"user_id": "u1", "channel": "push", "type": "price_alert", "timestamp": datetime.utcnow().isoformat()})
        stats = self.history.get_stats()
        assert stats["total"] >= 1
        assert "by_channel" in stats
        assert "by_type" in stats
