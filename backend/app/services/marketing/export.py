import csv, io, json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def export_data(db: AsyncSession, dataset: str, format: str, period: int):
    queries = {
        "stats": ("SELECT * FROM get_overview(:period)", None),
        "pages": ("SELECT path, views, unique_views, avg_time_on_page, bounce_rate FROM top_pages(:period, 200)", None),
        "referrers": ("SELECT source, visitors, page_views, bounce_rate, conversions FROM referrer_stats(:period)", None),
        "campaigns": ("SELECT * FROM campaign_stats_fn(:period)", None),
        "trends": ("SELECT date::text, visitors, page_views, conversions FROM daily_trends(:period)", None),
        "conversions": ("SELECT id::text, conversion_type, page, referrer, value, utm_source, utm_medium, utm_campaign, timestamp::text FROM conversions WHERE timestamp > NOW() - INTERVAL '1 day' * :period ORDER BY timestamp DESC", None),
        "geo": ("SELECT country, country_code, visitors, page_views FROM geo_stats(:period)", None),
        "devices": ("SELECT device_type, visitors, page_views FROM device_stats_fn(:period)", None),
        "links": ("SELECT id::text, url, slug, short_url, title, campaign, source, medium, total_clicks, unique_visitors, created_at::text FROM tracked_links ORDER BY created_at DESC", None),
        "experiments": ("SELECT id::text, name, page, description, metric, min_sample_size, status, created_at::text FROM experiments ORDER BY created_at DESC", None),
        "alerts": ("SELECT id::text, name, metric, condition, threshold, period_minutes, channel, active, last_fired::text, created_at::text FROM marketing_alerts ORDER BY created_at DESC", None),
    }

    if dataset not in queries:
        return None, None, None

    sql, _ = queries[dataset]
    rows = await db.execute(text(sql), {"period": period})
    data = [dict(r._mapping) for r in rows]

    filename = f"marketing_{dataset}_{period}d"

    if format == "json":
        content = json.dumps(data, indent=2, default=str)
        return f"{filename}.json", "application/json", content

    output = io.StringIO()
    if data:
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return f"{filename}.csv", "text/csv", output.getvalue()
