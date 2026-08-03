"""🐱 Marketing Dashboard API — stats, trends, campaigns, SEO"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Query
import random
import math

router = APIRouter(tags=["Marketing"])

random.seed(42)  # deterministic "random" for demo data

def _trend_data(days: int, base: float, volatility: float = 0.05) -> list[dict]:
    """Generate realistic marketing trend data."""
    data = []
    val = base
    for i in range(days):
        day = datetime.now(timezone.utc) - timedelta(days=days - i - 1)
        change = random.gauss(0, volatility)
        val = max(0, val * (1 + change))
        data.append({
            "date": day.strftime("%Y-%m-%d"),
            "page_views": round(val),
            "visitors": round(val * (0.4 + random.random() * 0.2)),
        })
    return data

@router.get("/stats")
async def get_stats(period: int = Query(30, ge=1, le=365)):
    days = period
    total_visitors = round(15000 + random.random() * 5000)
    total_views = round(total_visitors * (2.0 + random.random()))
    return {
        "total_visitors": total_visitors,
        "total_page_views": total_views,
        "bounce_rate": round(35 + random.random() * 15, 1),
        "avg_session_duration": round(120 + random.random() * 180),
        "conversion_rate": round(1.5 + random.random() * 2.5, 2),
        "total_conversions": round(total_visitors * (0.02 + random.random() * 0.03)),
        "active_sessions": round(50 + random.random() * 100),
        "period": days,
    }

@router.get("/trends")
async def get_trends(period: int = Query(30, ge=1, le=365)):
    return _trend_data(period, 5000)

@router.get("/pages")
async def get_pages(period: int = Query(30), limit: int = Query(20)):
    pages = [
        {"path": "/", "title": "Home", "views": round(8000 + random.random() * 2000)},
        {"path": "/pricing", "title": "Pricing", "views": round(3000 + random.random() * 1000)},
        {"path": "/features", "title": "Features", "views": round(2500 + random.random() * 800)},
        {"path": "/docs", "title": "Documentation", "views": round(2000 + random.random() * 600)},
        {"path": "/papers", "title": "MiauPapers", "views": round(1500 + random.random() * 500)},
        {"path": "/blog", "title": "Blog", "views": round(1200 + random.random() * 400)},
        {"path": "/login", "title": "Login", "views": round(1000 + random.random() * 300)},
        {"path": "/register", "title": "Register", "views": round(800 + random.random() * 200)},
        {"path": "/courses", "title": "Courses", "views": round(600 + random.random() * 200)},
        {"path": "/about", "title": "About", "views": round(400 + random.random() * 100)},
    ]
    for p in pages:
        p["avg_time"] = round(60 + random.random() * 120)
        p["bounce_rate"] = round(30 + random.random() * 20, 1)
    return sorted(pages, key=lambda x: x["views"], reverse=True)[:limit]

@router.get("/referrers")
async def get_referrers(period: int = Query(30)):
    sources = ["Google", "Twitter", "GitHub", "Direct", "LinkedIn", "Product Hunt", "Reddit", "Hacker News", "YouTube", "Medium"]
    return [{"source": s, "visitors": round(500 + random.random() * 3000)} for s in sources]

@router.get("/campaigns")
async def get_campaigns(period: int = Query(30)):
    return [
        {"name": "🐱 Launch Week", "spend": round(5000 + random.random() * 1000, 2), "impressions": round(50000 + random.random() * 20000), "clicks": round(2000 + random.random() * 1000), "conversions": round(50 + random.random() * 30)},
        {"name": "📢 Dev Summit", "spend": round(3000 + random.random() * 500, 2), "impressions": round(30000 + random.random() * 10000), "clicks": round(1500 + random.random() * 500), "conversions": round(30 + random.random() * 20)},
        {"name": "🐦 Twitter Blast", "spend": round(1000 + random.random() * 300, 2), "impressions": round(20000 + random.random() * 5000), "clicks": round(800 + random.random() * 300), "conversions": round(15 + random.random() * 10)},
        {"name": "📝 Blog Push", "spend": round(500 + random.random() * 200, 2), "impressions": round(5000 + random.random() * 2000), "clicks": round(300 + random.random() * 100), "conversions": round(8 + random.random() * 5)},
        {"name": "🤝 Partnership", "spend": round(2000 + random.random() * 500, 2), "impressions": round(15000 + random.random() * 5000), "clicks": round(600 + random.random() * 200), "conversions": round(20 + random.random() * 10)},
    ]

@router.get("/conversions")
async def get_conversions(period: int = Query(30), limit: int = Query(50)):
    types = ["signup", "trial_start", "subscription", "api_call", "paper_download", "course_enroll"]
    return [{"id": i, "type": random.choice(types), "value": round(random.random() * 100, 2), "timestamp": (datetime.now(timezone.utc) - timedelta(hours=random.random() * period * 24)).isoformat()} for i in range(min(limit, 50))]

@router.get("/realtime")
async def get_realtime():
    return {
        "active_visitors": round(50 + random.random() * 100),
        "page_views_today": round(2000 + random.random() * 1000),
        "top_page": random.choice(["/", "/pricing", "/features", "/papers", "/docs"]),
        "top_source": random.choice(["Direct", "Google", "GitHub", "Twitter"]),
        "conversions_today": round(5 + random.random() * 15),
    }

@router.get("/geo")
async def get_geo(period: int = Query(30)):
    countries = [
        {"country": "United States", "country_code": "US", "visitors": round(5000 + random.random() * 2000), "page_views": round(10000 + random.random() * 4000)},
        {"country": "Germany", "country_code": "DE", "visitors": round(3000 + random.random() * 1000), "page_views": round(6000 + random.random() * 2000)},
        {"country": "United Kingdom", "country_code": "GB", "visitors": round(2000 + random.random() * 800), "page_views": round(4000 + random.random() * 1600)},
        {"country": "Canada", "country_code": "CA", "visitors": round(1500 + random.random() * 500), "page_views": round(3000 + random.random() * 1000)},
        {"country": "France", "country_code": "FR", "visitors": round(1000 + random.random() * 400), "page_views": round(2000 + random.random() * 800)},
    ]
    return countries

@router.get("/devices")
async def get_devices(period: int = Query(30)):
    return [
        {"device": "Desktop", "visitors": round(60 + random.random() * 10)},
        {"device": "Mobile", "visitors": round(30 + random.random() * 10)},
        {"device": "Tablet", "visitors": round(5 + random.random() * 5)},
    ]

@router.get("/seo")
async def get_seo():
    return {
        "score": round(75 + random.random() * 20, 1),
        "pages_indexed": round(150 + random.random() * 50),
        "backlinks": round(500 + random.random() * 300),
        "keywords_top10": round(30 + random.random() * 20),
        "issues": {"critical": 0, "warnings": round(2 + random.random() * 5), "passed": round(40 + random.random() * 10)},
    }

@router.get("/seo/audit")
async def run_seo_audit():
    return {
        "status": "complete",
        "pages_scanned": round(50 + random.random() * 30),
        "missing_titles": round(1 + random.random() * 3),
        "missing_descriptions": round(2 + random.random() * 4),
        "missing_h1": round(1 + random.random() * 2),
        "slow_pages": round(3 + random.random() * 5),
        "broken_links": round(1 + random.random() * 3),
    }
