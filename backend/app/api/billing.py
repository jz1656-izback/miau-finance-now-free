import logging
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.schemas.billing import (
    CheckoutRequest, CheckoutResponse, SubscriptionResponse,
    PricingResponse, PricingTier,
    BarkRequestCreate, BarkRequestResponse,
    LicenseKeyResponse,
)
from app.middleware.tier import TIER_LIMITS
from app.services.billing_service import (
    get_or_create_stripe_customer as create_stripe_customer,
    create_checkout_session as create_stripe_checkout_session,
    create_portal_session as get_stripe_billing_portal,
)
from app.services.revenue import record_revenue
from app.services.invoice_service import generate_invoice_pdf, get_usage_summary, generate_daily_usage_record

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["Billing"])

BARK_PRICE = 999900  # €9,999 per extra bark (in cents)

DEVELOPMENT_DISCOUNT = 0.90  # 90% off during development
DISCOUNT_MESSAGE = "🚧 90% development discount — still in development"
DISCOUNT_EXPIRY = "2027-05-21"

PRICING_PLANS: list[dict] = [
    {
        "id": "tamagotchi",
        "name": "Cat Tamagotchi",
        "description": "Just a cat. No finance. Pet it daily.",
        "amount_monthly": 0,
        "amount_yearly": 0,
        "currency": "eur",
        "seat_based": False,
        "barks_included": 0,
        "features": [
            "Virtual pet cat in terminal",
            "Feed, pet, and play with your cat",
            "Cat reacts to your typing",
            "Login streak rewards",
            "Unlockable cat hats (€0.99 tuna)",
            "🐱 Zero stock data — this is a pet game",
        ],
    },
    {
        "id": "trial",
        "name": "Trial Trader",
        "description": "Test the real terminal. 50 calls/day. No commitment.",
        "amount_monthly": 499,  # €4.99 → €2.49 at 50% off
        "amount_yearly": 4990,  # €49.90 → €24.90 at 50% off
        "currency": "eur",
        "seat_based": False,
        "barks_included": 0,
        "features": [
            "50 API calls per day",
            "7-day price history",
            "5 data providers",
            "Basic terminal commands",
            "No AI advisor",
            "Cat still visible but judgmental",
        ],
    },
    {
        "id": "starter",
        "name": "Starter Cat",
        "description": "Real data for serious starters. 500 calls/day.",
        "amount_monthly": 5000,  # €50 → €25 at 50% off
        "amount_yearly": 48000,  # €40/user/mo yearly
        "currency": "eur",
        "seat_based": False,
        "barks_included": 0,
        "features": [
            "500 API calls per day",
            "Full price history (1 year)",
            "15 data providers",
            "Technical indicators (RSI, MACD, SMA)",
            "Basic portfolio tracking",
            "Email support",
            "Extra barks: €9,999 each",
        ],
    },
    {
        "id": "pro",
        "name": "Pro Cat",
        "description": "Unlimited data. AI advisor. Full power.",
        "amount_monthly": 9900,  # €99 → €49.50 at 50% off
        "amount_yearly": 94800,  # €79/user/mo yearly
        "currency": "eur",
        "seat_based": False,
        "barks_included": 1,
        "features": [
            "3,000 API calls per day",
            "Full price history (unlimited)",
            "All 37 data providers",
            "AI advisor (real LLM analysis)",
            "Risk analytics (VaR, beta, stress tests)",
            "Advanced portfolio with P&L tracking",
            "Trading signals & backtesting",
            "Priority support",
            "1 bark included (extra: €9,999 each)",
            "7-day free trial",
        ],
    },
    {
        "id": "fund",
        "name": "Fund Cat",
        "description": "For teams. 3 seats. 10k calls/day each.",
        "amount_monthly": 15000,  # €150 → €75 at 50% off
        "amount_yearly": 144000,  # €120/user/mo yearly
        "currency": "eur",
        "seat_based": True,
        "barks_included": 2,
        "features": [
            "10,000 API calls per day per user",
            "3 team seats included",
            "All data providers & features",
            "Team workspaces with roles",
            "Shared portfolios & watchlists",
            "Custom alerts & notifications",
            "Onboarding support",
            "2 barks included (extra: €9,999 each)",
        ],
    },
    {
        "id": "enterprise",
        "name": "Enterprise",
        "description": "Per-user pricing for real companies. €699,67/user/mo.",
        "badge": "👑",
        "amount_monthly": 69967,  # €699.67/user/mo → €349.84 at 50% off
        "amount_yearly": 671600,  # €559.67/user/mo yearly
        "currency": "eur",
        "seat_based": True,
        "barks_included": 10,
        "features": [
            "Unlimited API calls per user",
            "On-premise deployment option",
            "SSO/SAML authentication",
            "Custom integrations",
            "Dedicated support & SLA (99.9%)",
            "10 barks included (extra: €9,999 each)",
            "Direct line to the developers",
        ],
    },
    {
        "id": "adopt",
        "name": "Adopt Cat",
        "description": "Buy the whole project. €67M full → €33.5M launch. All IP.",
        "badge": "⭐",
        "amount_monthly": 67000000,  # €67M full → €33.5M at 50% off
        "amount_yearly": 67000000,
        "currency": "eur",
        "seat_based": False,
        "barks_included": 9999,
        "features": [
            "Full ownership of Miau Finance",
            "All source code & IP",
            "All domains & infrastructure",
            "37 data provider integrations",
            "230 education courses",
            "Frontend + backend + docs",
            "Docker + K8s deployment",
            "This cat will work for you now 🐱",
        ],
    },
]

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

TIER_PRICES: dict[str, dict[str, object]] = {
    "trial": {
        "price_id": os.getenv("STRIPE_TRIAL_PRICE_ID", "price_trial_monthly"),
        "amount": 499,
        "currency": "eur",
        "name": "Trial Trader",
    },
    "starter": {
        "price_id": os.getenv("STRIPE_STARTER_PRICE_ID", "price_starter_monthly"),
        "amount": 5000,
        "currency": "eur",
        "name": "Starter Cat",
    },
    "pro": {
        "price_id": os.getenv("STRIPE_PRO_PRICE_ID", "price_pro_monthly"),
        "amount": 9900,
        "currency": "eur",
        "name": "Pro Cat",
    },
    "fund": {
        "price_id": os.getenv("STRIPE_FUND_PRICE_ID", "price_fund_monthly"),
        "amount": 15000,
        "currency": "eur",
        "name": "Fund Cat",
    },
    "enterprise": {
        "price_id": os.getenv("STRIPE_ENTERPRISE_PRICE_ID", "price_enterprise_monthly"),
        "amount": 69967,
        "currency": "eur",
        "name": "Enterprise",
    },
    "adopt": {
        "price_id": os.getenv("STRIPE_ADOPT_PRICE_ID", "price_adopt_one_time"),
        "amount": 67000000,
        "currency": "eur",
        "name": "Adopt Cat",
    },
}


async def get_my_subscription_helper(db: AsyncSession, user_id: str) -> Optional[dict]:
    return await get_subscription(db, user_id)


@router.get("/pricing", response_model=PricingResponse)
async def get_pricing():
    tiers = []
    for plan in PRICING_PLANS:
        limits = TIER_LIMITS.get(plan["id"], TIER_LIMITS["free"])
        orig_monthly = plan["amount_monthly"]
        orig_yearly = plan["amount_yearly"]
        if orig_monthly > 0:
            disc_monthly = max(1, int(orig_monthly * (1 - DEVELOPMENT_DISCOUNT)))
            disc_yearly = max(1, int(orig_yearly * (1 - DEVELOPMENT_DISCOUNT)))
        else:
            disc_monthly = orig_monthly
            disc_yearly = orig_yearly
        tiers.append(PricingTier(
            id=plan["id"],
            name=plan["name"],
            description=plan["description"],
            amount_monthly=disc_monthly,
            amount_yearly=disc_yearly,
            currency=plan["currency"],
            features=plan["features"],
            requests_per_minute=limits["requests_per_minute"],
            requests_per_hour=limits["requests_per_hour"],
            concurrent_connections=limits.get("concurrent_connections", 1),
            data_providers=limits.get("data_providers", 5),
            barks_included=plan.get("barks_included", 0),
            seat_based=plan.get("seat_based", False),
            original_amount_monthly=orig_monthly,
            original_amount_yearly=orig_yearly,
            discount_percent=int(DEVELOPMENT_DISCOUNT * 100) if orig_monthly > 0 else None,
            discount_message=DISCOUNT_MESSAGE if orig_monthly > 0 else None,
        ))
    return PricingResponse(
        tiers=tiers,
        discount_active=True,
        discount_percent=int(DEVELOPMENT_DISCOUNT * 100),
        discount_message=DISCOUNT_MESSAGE,
        discount_expiry=DISCOUNT_EXPIRY,
    )


@router.get("/subscription")
async def get_my_subscription(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    if not sub:
        return SubscriptionResponse(
            id="", user_id=user["id"], tier="free", status="active",
        )
    return SubscriptionResponse(
        id=str(sub["id"]), user_id=str(sub["user_id"]),
        stripe_customer_id=sub["stripe_customer_id"],
        stripe_subscription_id=sub["stripe_subscription_id"],
        tier=sub["tier"], status=sub["status"],
        trial_ends_at=sub["trial_ends_at"], current_period_end=sub["current_period_end"],
        seats=sub.get("seats", 1),
        barks_remaining=sub.get("barks_remaining", 0),
        barks_used=sub.get("barks_used", 0),
        on_premise_license=sub.get("on_premise_license", False),
        license_key=sub.get("license_key"),
        created_at=sub["created_at"],
    )


def _calculate_bark_allocation(tier: str) -> int:
    for plan in PRICING_PLANS:
        if plan["id"] == tier:
            return plan.get("barks_included", 0)
    return 0


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    req: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    if req.tier not in TIER_PRICES:
        raise HTTPException(400, f"Invalid tier: {req.tier}. Choose from: {', '.join(TIER_PRICES.keys())}")

    seats = max(1, req.seats)
    barks = _calculate_bark_allocation(req.tier)

    if not STRIPE_SECRET_KEY:
        sub = await get_my_subscription_helper(db, user["id"])
        if not sub or sub["tier"] == "free":
            await db.execute(
                text("""
                    INSERT INTO subscriptions (id, user_id, tier, status, seats, barks_remaining, bark_year, current_period_end)
                    VALUES (gen_random_uuid(), :uid, :tier, 'active', :seats, :barks, EXTRACT(YEAR FROM NOW()), NOW() + INTERVAL '30 days')
                    ON CONFLICT (user_id) DO UPDATE SET
                        tier = :tier2, status = 'active', seats = :seats2,
                        barks_remaining = barks_remaining + :barks2,
                        current_period_end = NOW() + INTERVAL '30 days'
                """),
                {"uid": user["id"], "tier": req.tier, "seats": seats, "barks": barks,
                 "tier2": req.tier, "seats2": seats, "barks2": barks},
            )
            await db.commit()
            logger.info(f"Dev mode: activated {req.tier} ({seats} seats) for user {user['id']}")
            return CheckoutResponse(
                session_url=f"/billing/success?tier={req.tier}&seats={seats}&dev_mode=true"
            )
        return CheckoutResponse(
            session_url=f"/billing/success?tier={sub['tier']}&already_active=true"
        )

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        price_id = TIER_PRICES[req.tier]["price_id"]
        session = stripe.checkout.Session.create(
            customer_email=user.get("email"),
            metadata={"user_id": user["id"], "tier": req.tier, "seats": str(seats)},
            line_items=[{"price": price_id, "quantity": seats}],
            mode="subscription",
            success_url=req.success_url,
            cancel_url=req.cancel_url,
        )
        return CheckoutResponse(session_url=session.url)
    except Exception as e:
        logger.error(f"Stripe checkout failed: {e}")
        raise HTTPException(502, "Payment provider unavailable")


@router.get("/barks", response_model=list[BarkRequestResponse])
async def list_barks(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT * FROM bark_requests WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": user["id"]},
    )
    rows = result.mappings().all()
    return [
        BarkRequestResponse(
            id=str(r["id"]), user_id=str(r["user_id"]),
            title=r["title"], description=r.get("description"),
            status=r["status"], bark_year=r["bark_year"],
            created_at=r["created_at"],
        ) for r in rows
    ]


@router.post("/barks", response_model=BarkRequestResponse)
async def create_bark(
    req: BarkRequestCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    tier = sub["tier"] if sub else "free"

    if tier == "free":
        raise HTTPException(402, "Barks require a paid plan (Tiny Catfunds or Enterprise)")
    if tier == "pro":
        raise HTTPException(402, "Barks require Enterprise (€699.67/user/mo) or Adopt Cat")

    year = datetime.now(timezone.utc).year
    barks_remaining = sub.get("barks_remaining", 0) if sub else 0
    bark_year = sub.get("bark_year") if sub else None

    if bark_year != year:
        allocation = _calculate_bark_allocation(tier)
        await db.execute(
            text("UPDATE subscriptions SET barks_remaining = :barks, barks_used = 0, bark_year = :year WHERE user_id = :uid"),
            {"barks": allocation, "year": year, "uid": user["id"]},
        )
        await db.commit()
        barks_remaining = allocation

    if barks_remaining <= 0 and tier != "enterprise":
        raise HTTPException(
            402,
            f"No barks remaining for {year}. Extra barks cost €9,999 each. "
            f"Upgrade to Enterprise (15 free barks/yr) or purchase more."
        )
    if barks_remaining <= 0:
        raise HTTPException(
            402,
            f"No barks remaining for {year}. Purchase more at €9,999/bark."
        )

    result = await db.execute(
        text("""
            INSERT INTO bark_requests (id, user_id, title, description, status, bark_year)
            VALUES (gen_random_uuid(), :uid, :title, :desc, 'pending', :year)
            RETURNING *
        """),
        {"uid": user["id"], "title": req.title, "desc": req.description, "year": year},
    )
    await db.execute(
        text("UPDATE subscriptions SET barks_remaining = barks_remaining - 1, barks_used = barks_used + 1 WHERE user_id = :uid"),
        {"uid": user["id"]},
    )
    await db.commit()
    row = result.mappings().first()
    logger.info(f"Bark created: {req.title} by user {user['id']} ({barks_remaining - 1} remaining)")
    return BarkRequestResponse(
        id=str(row["id"]), user_id=str(row["user_id"]),
        title=row["title"], description=row.get("description"),
        status=row["status"], bark_year=row["bark_year"],
        created_at=row["created_at"],
    )


@router.post("/barks/purchase")
async def purchase_bark(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    if not sub or sub["tier"] == "free":
        raise HTTPException(402, "Requires a paid plan to purchase extra barks")

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            metadata={"user_id": user["id"], "type": "bark_purchase"},
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Extra Bark — Feature Request"},
                    "unit_amount": BARK_PRICE,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=os.getenv("FRONTEND_URL", "http://localhost:5173") + "/billing/success",
            cancel_url=os.getenv("FRONTEND_URL", "http://localhost:5173") + "/billing/cancel",
        )
        return {"checkout_url": session.url}
    except Exception as e:
        logger.error(f"Bark purchase checkout failed: {e}")
        raise HTTPException(502, "Payment provider unavailable")


@router.post("/on-premise/license")
async def generate_license_key(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    if not sub or sub["tier"] != "enterprise":
        raise HTTPException(402, "On-premise licenses require Enterprise tier (€699.67/user/mo)")

    import secrets
    license_key = f"MIAU-ONP-{secrets.token_hex(8).upper()}-{secrets.token_hex(4).upper()}"

    await db.execute(
        text("""
            UPDATE subscriptions SET on_premise_license = TRUE, license_key = :key
            WHERE user_id = :uid
        """),
        {"key": license_key, "uid": user["id"]},
    )
    await db.commit()

    return LicenseKeyResponse(
        license_key=license_key,
        tier="enterprise",
        seats=sub.get("seats", 1),
        expires_at=sub.get("current_period_end"),
        on_premise=True,
    )


@router.get("/on-premise/verify")
async def verify_license_key(
    license_key: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("""
            SELECT tier, seats, on_premise_license, current_period_end, status
            FROM subscriptions
            WHERE license_key = :key AND on_premise_license = TRUE
              AND status IN ('active', 'trialing')
        """),
        {"key": license_key},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Invalid or expired license key")
    return LicenseKeyResponse(
        license_key=license_key,
        tier=row["tier"],
        seats=row["seats"],
        expires_at=row["current_period_end"],
        on_premise=True,
    )


@router.post("/trial/activate")
async def activate_trial(
    tier: str = "pro",
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    valid_trial_tiers = ["starter", "pro", "fund"]
    if tier not in valid_trial_tiers:
        raise HTTPException(400, f"Trial only available for: {', '.join(valid_trial_tiers)}")

    existing = await get_subscription(db, user["id"])
    if existing and existing["tier"] != "free":
        raise HTTPException(400, "Trial only available for free tier users")

    barks = _calculate_bark_allocation(tier)
    await db.execute(
        text("""
            INSERT INTO subscriptions (id, user_id, tier, status, seats, barks_remaining, bark_year, trial_ends_at, current_period_end)
            VALUES (gen_random_uuid(), :uid, :tier, 'trialing', 1, :barks, EXTRACT(YEAR FROM NOW()),
                    NOW() + INTERVAL '7 days', NOW() + INTERVAL '7 days')
            ON CONFLICT (user_id) DO UPDATE SET
                tier = :tier2, status = 'trialing', seats = 1,
                barks_remaining = :barks2, bark_year = EXTRACT(YEAR FROM NOW()),
                trial_ends_at = NOW() + INTERVAL '7 days',
                current_period_end = NOW() + INTERVAL '7 days'
        """),
        {"uid": user["id"], "tier": tier, "barks": barks,
         "tier2": tier, "barks2": barks},
    )
    await db.commit()
    logger.info(f"Trial activated for user {user['id']}: {tier}")
    return {"status": "trial_active", "tier": tier, "trial_days": 7}


@router.post("/portal")
async def billing_portal(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    customer_id = sub.get("stripe_customer_id") if sub else None
    if not customer_id:
        customer_id = await get_or_create_stripe_customer(db, user["id"], user.get("email", ""), user.get("username", ""))
        if customer_id:
            await db.execute(
                text("UPDATE subscriptions SET stripe_customer_id = :cid WHERE user_id = :uid"),
                {"cid": customer_id, "uid": user["id"]},
            )
            await db.commit()

    portal_url = await create_portal_session(
        user["id"],
        return_url=f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/billing",
    )
    return {"portal_url": portal_url}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    # 🔒 SECURITY (V7-002/C4): If the webhook secret is not configured we FAIL CLOSED.
    # Without signature verification an attacker could forge checkout events and
    # grant themselves paid tiers. A webhook that cannot be verified is rejected.
    if not STRIPE_WEBHOOK_SECRET:
        logger.error("Stripe webhook secret not configured — refusing to process webhook")
        raise HTTPException(503, "Webhook secret not configured")

    if not STRIPE_SECRET_KEY:
        logger.error("Stripe secret key not configured — refusing to process webhook")
        raise HTTPException(503, "Stripe not configured")

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY

        payload = await request.body()
        sig_header = request.headers.get("stripe-signature", "")

        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    except Exception:
        raise HTTPException(400, "Webhook error")

    event_type = event.get("type", event.get("type", ""))
    data = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        customer_id = data.get("customer")
        subscription_id = data.get("subscription")
        metadata = data.get("metadata", {})
        user_id = metadata.get("user_id")
        tier = metadata.get("tier", "pro")

        if user_id:
            await db.execute(
                text("""
                    INSERT INTO subscriptions (id, user_id, stripe_customer_id, stripe_subscription_id, tier, status, current_period_end)
                    VALUES (gen_random_uuid(), :uid, :cust, :sub_id, :tier, 'active', NOW() + INTERVAL '30 days')
                    ON CONFLICT (user_id) DO UPDATE SET
                        stripe_customer_id = :cust2, stripe_subscription_id = :sub_id2,
                        tier = :tier2, status = 'active',
                        current_period_end = NOW() + INTERVAL '30 days'
                """),
                {"uid": user_id, "cust": customer_id, "sub_id": subscription_id,
                 "tier": tier, "cust2": customer_id, "sub_id2": subscription_id, "tier2": tier},
            )
            await db.commit()
            logger.info(f"Subscription activated for user {user_id}: {tier}")

    elif event_type == "customer.subscription.updated":
        subscription_id = data.get("id")
        status = data.get("status", "active")
        if subscription_id:
            await db.execute(
                text("""
                    UPDATE subscriptions SET status = :status,
                    current_period_end = to_timestamp(:period_end)
                    WHERE stripe_subscription_id = :sid
                """),
                {"status": status, "period_end": data.get("current_period_end", 0),
                 "sid": subscription_id},
            )
            await db.commit()
            logger.info(f"Subscription updated: {subscription_id} → {status}")

    elif event_type == "invoice.payment_succeeded":
        subscription_id = data.get("subscription")
        if subscription_id:
            await db.execute(
                text("""
                    UPDATE subscriptions SET status = 'active',
                    current_period_end = to_timestamp(:period_end)
                    WHERE stripe_subscription_id = :sid
                """),
                {"period_end": data.get("period_end", 0), "sid": subscription_id},
            )
            await db.commit()
            logger.info(f"Payment succeeded for subscription: {subscription_id}")
            # Record revenue for 20/80 split
            try:
                amount_paid = float(data.get("amount_paid", 0)) / 100  # Stripe amounts in cents
                if amount_paid > 0:
                    await record_revenue(
                        db,
                        amount_total=Decimal(str(amount_paid)),
                        currency=data.get("currency", "eur"),
                        source="stripe_subscription",
                        source_id=subscription_id,
                        description=f"Subscription payment — {data.get('description', '')}",
                    )
            except Exception as e:
                logger.warning(f"Failed to record revenue: {e}")

    elif event_type == "invoice.payment_failed":
        subscription_id = data.get("subscription")
        if subscription_id:
            await db.execute(
                text("UPDATE subscriptions SET status = 'past_due' WHERE stripe_subscription_id = :sid"),
                {"sid": subscription_id},
            )
            await db.commit()
            logger.warning(f"Payment failed for subscription: {subscription_id}")

    elif event_type == "customer.subscription.deleted":
        subscription_id = data.get("id")
        if subscription_id:
            await db.execute(
                text("UPDATE subscriptions SET status = 'cancelled' WHERE stripe_subscription_id = :sid"),
                {"sid": subscription_id},
            )
            await db.commit()
            logger.info(f"Subscription cancelled: {subscription_id}")

    return {"status": "ok"}


@router.post("/cancel")
async def cancel_my_subscription(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    if not sub or sub["tier"] == "free":
        raise HTTPException(400, "No active subscription to cancel")
    result = await cancel_subscription(db, user["id"])
    if result:
        logger.info(f"Subscription cancelled for user {user['id']}")
    return {"status": "cancelled", "tier": "free"}


@router.get("/history")
async def billing_history(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    sub = await get_my_subscription_helper(db, user["id"])
    if not sub:
        return {"subscription": None, "invoices": [], "payments": []}
    return {
        "subscription": {
            "tier": sub["tier"],
            "status": sub["status"],
            "trial_ends_at": str(sub["trial_ends_at"]) if sub["trial_ends_at"] else None,
            "current_period_end": str(sub["current_period_end"]) if sub["current_period_end"] else None,
            "created_at": str(sub["created_at"]) if sub["created_at"] else None,
        },
        "invoices": [],
        "payments": [],
    }


@router.get("/usage")
async def usage_dashboard(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    return await get_usage_summary(db, user["id"])


@router.get("/invoices")
async def list_invoices(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT id, stripe_invoice_id, amount, currency, status, period_start, period_end, paid_at, created_at
            FROM invoices WHERE user_id = :uid
            ORDER BY period_start DESC LIMIT :limit OFFSET :offset
        """),
        {"uid": user["id"], "limit": limit, "offset": offset},
    )
    return [dict(row) for row in result.mappings().all()]


@router.get("/invoices/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT * FROM invoices WHERE id = :id AND user_id = :uid"),
        {"id": invoice_id, "uid": user["id"]},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Invoice not found")
    return dict(row)


@router.get("/invoices/{invoice_id}/pdf")
async def download_invoice_pdf(
    invoice_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT * FROM invoices WHERE id = :id AND user_id = :uid"),
        {"id": invoice_id, "uid": user["id"]},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Invoice not found")

    pdf_bytes = generate_invoice_pdf(dict(row))
    short_id = str(invoice_id)[:8]
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="invoice-MIU-{short_id}.pdf"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )


@router.post("/crypto/address")
async def create_crypto_payment_address(
    tier: str = "pro",
    chain: str = "ethereum",
    currency: str = "ETH",
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    from app.services.crypto_payments import generate_payment_address
    invoice_id = f"crypto_{user['id']}_{int(datetime.now(timezone.utc).timestamp())}"
    info = generate_payment_address(invoice_id, chain, currency)
    return info


@router.get("/crypto/status/{invoice_id}")
async def check_crypto_payment(
    invoice_id: str,
    chain: str = "ethereum",
    user: dict = Depends(get_current_user_db),
):
    from app.services.crypto_payments import check_payment
    result = await check_payment(invoice_id, chain)
    return result
