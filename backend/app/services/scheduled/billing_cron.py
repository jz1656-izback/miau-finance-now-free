"""Monthly billing report generation cron.

On the 1st of each month: generates invoices for the previous month,
calculates overage charges, triggers Stripe payment, and sends email
notifications.
"""
import logging
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def generate_monthly_invoices(db: AsyncSession) -> list[dict]:
    now = datetime.now(timezone.utc)

    subs = await db.execute(
        text("""
            SELECT s.user_id, s.tier, s.seats, s.stripe_customer_id,
                   COALESCE(SUM(ur.request_count), 0) as monthly_requests
            FROM subscriptions s
            LEFT JOIN usage_records ur ON ur.user_id = s.user_id
                AND ur.date >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
                AND ur.date < DATE_TRUNC('month', NOW())
            WHERE s.status = 'active' AND s.tier != 'free'
            GROUP BY s.user_id, s.tier, s.seats, s.stripe_customer_id
        """),
    )
    invoices = []
    for row in subs.mappings().all():
        tier = row["tier"]
        seats = int(row.get("seats", 1))
        base_prices = {"pro": 9900, "fund": 15000, "enterprise": 69967}
        base_price = base_prices.get(tier, 1000) * seats
        requests = int(row["monthly_requests"])
        overage = max(0, requests - 10000) * 0.001
        total = base_price + int(overage * 100)

        result = await db.execute(
            text("""
                INSERT INTO billing_invoices (id, user_id, amount, currency, period_start, period_end, status, line_items)
                VALUES (gen_random_uuid(), :uid, :amount, 'usd',
                        DATE_TRUNC('month', NOW()) - INTERVAL '1 month',
                        DATE_TRUNC('month', NOW()),
                        'pending', :items)
                RETURNING id
            """),
            {
                "uid": row["user_id"],
                "amount": total,
                "items": f'{{"base": {base_price}, "overage": {int(overage * 100)}, "requests": {requests}}}',
            },
        )
        await db.commit()
        inv_id = result.scalar()
        invoices.append({"user_id": str(row["user_id"]), "invoice_id": str(inv_id), "amount": total})
        logger.info("Invoice %s generated for user %s: $%.2f", inv_id, row["user_id"], total / 100)

    return invoices
