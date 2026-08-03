import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

TIER_THRESHOLDS = {
    "tamagotchi": Decimal("5"),
    "trial": Decimal("10"),
    "starter": Decimal("25"),
    "pro": Decimal("50"),
    "fund": Decimal("100"),
    "enterprise": Decimal("200"),
}

TIER_TOPUP = {
    "tamagotchi": Decimal("10"),
    "trial": Decimal("25"),
    "starter": Decimal("50"),
    "pro": Decimal("100"),
    "fund": Decimal("200"),
    "enterprise": Decimal("500"),
}


async def check_and_topup(db: AsyncSession) -> list[dict]:
    results = []

    try:
        users = await db.execute(
            text("""
                SELECT u.id, u.username, s.tier,
                       COALESCE(b.balance, 0) as balance,
                       COALESCE(b.default_payment_id, '') as payment_id
                FROM users u
                JOIN subscriptions s ON s.user_id = u.id
                LEFT JOIN billing_balances b ON b.user_id = u.id
                WHERE s.status = 'active'
                  AND s.tier != 'free'
            """),
        )
    except Exception as e:
        logger.warning("Auto-topup skipped — billing_balances table not available: %s", e)
        return results

    for row in users.mappings().all():
        user_id = row["id"]
        tier = row["tier"]
        balance = Decimal(str(row["balance"]))
        threshold = TIER_THRESHOLDS.get(tier, TIER_THRESHOLDS["free"])
        topup_amount = TIER_TOPUP.get(tier, TIER_TOPUP["free"])

        if balance >= threshold:
            continue

        payment_id = row["payment_id"]
        if not payment_id:
            logger.warning("User %s below threshold but no payment method", user_id)
            continue

        try:
            import stripe
            stripe.PaymentIntent.create(
                amount=int(topup_amount * 100),
                currency="usd",
                customer=row.get("stripe_customer_id", ""),
                payment_method=payment_id,
                off_session=True,
                confirm=True,
            )
        except ImportError:
            logger.error("Stripe not installed — skipping topup for user %s", user_id)
            continue
        except Exception as e:
            logger.error("Stripe charge failed for user %s: %s", user_id, e)
            continue

        await db.execute(
            text("""
                INSERT INTO billing_transactions (id, user_id, amount, type, description)
                VALUES (gen_random_uuid(), :uid, :amount, 'topup', 'Auto top-up')
            """),
            {"uid": user_id, "amount": topup_amount},
        )

        await db.execute(
            text("UPDATE billing_balances SET balance = balance + :amount WHERE user_id = :uid"),
            {"uid": user_id, "amount": topup_amount},
        )

        await db.commit()
        results.append({"user_id": str(user_id), "topup": float(topup_amount)})
        logger.info("Auto top-up %s for user %s", topup_amount, user_id)

    return results
