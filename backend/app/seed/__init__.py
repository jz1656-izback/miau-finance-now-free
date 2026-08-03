import logging
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    OntologyType, OntologyProperty, OntologyLink, OntologyObject,
    OntologyObjectLink, Instrument, Portfolio, Position, Counterparty,
    Trade, Watchlist, WatchlistItem,
)
from app.database import async_session

logger = logging.getLogger(__name__)


SECTORS = [
    "Technology", "Healthcare", "Financials", "Energy", "Consumer Discretionary",
    "Industrials", "Materials", "Utilities", "Real Estate", "Communication Services",
]

INDUSTRY_MAP = {
    "Technology": ["Software", "Hardware", "Semiconductors", "Cloud Computing", "Cybersecurity"],
    "Healthcare": ["Pharmaceuticals", "Biotechnology", "Medical Devices", "Healthcare Services"],
    "Financials": ["Banking", "Insurance", "Asset Management", "Fintech"],
    "Energy": ["Oil & Gas", "Renewables", "Utilities", "Energy Services"],
    "Consumer Discretionary": ["E-Commerce", "Automotive", "Luxury Goods", "Travel"],
    "Industrials": ["Aerospace & Defense", "Machinery", "Logistics", "Construction"],
    "Materials": ["Chemicals", "Metals & Mining", "Forestry", "Packaging"],
    "Utilities": ["Electric Utilities", "Water Utilities", "Gas Utilities"],
    "Real Estate": ["REITs", "Property Management", "Development"],
    "Communication Services": ["Media", "Telecom", "Internet", "Entertainment"],
}

SAMPLE_TICKERS = {
    "Technology": [
        ("AAPL", "Apple Inc.", "Software"), ("MSFT", "Microsoft Corporation", "Software"),
        ("NVDA", "NVIDIA Corporation", "Semiconductors"), ("GOOGL", "Alphabet Inc.", "Internet"),
        ("AMZN", "Amazon.com Inc.", "E-Commerce"), ("META", "Meta Platforms Inc.", "Internet"),
        ("CRM", "Salesforce Inc.", "Cloud Computing"), ("AMD", "Advanced Micro Devices", "Semiconductors"),
        ("INTC", "Intel Corporation", "Semiconductors"), ("ORCL", "Oracle Corporation", "Software"),
    ],
    "Healthcare": [
        ("JNJ", "Johnson & Johnson", "Pharmaceuticals"), ("PFE", "Pfizer Inc.", "Pharmaceuticals"),
        ("UNH", "UnitedHealth Group", "Healthcare Services"), ("ABBV", "AbbVie Inc.", "Pharmaceuticals"),
    ],
    "Financials": [
        ("JPM", "JPMorgan Chase & Co.", "Banking"), ("GS", "Goldman Sachs Group", "Banking"),
        ("BLK", "BlackRock Inc.", "Asset Management"), ("V", "Visa Inc.", "Fintech"),
    ],
    "Energy": [
        ("XOM", "Exxon Mobil Corporation", "Oil & Gas"), ("CVX", "Chevron Corporation", "Oil & Gas"),
        ("NEE", "NextEra Energy", "Renewables"),
    ],
    "Consumer Discretionary": [
        ("TSLA", "Tesla Inc.", "Automotive"), ("HD", "Home Depot Inc.", "Retail"),
    ],
}


async def seed_ontology_types(session: AsyncSession) -> dict[str, uuid.UUID]:
    type_ids = {}
    type_defs = [
        ("instrument", "Instrument", "Financial instruments (stocks, bonds, derivatives)"),
        ("portfolio", "Portfolio", "Investment portfolios"),
        ("counterparty", "Counterparty", "Trading counterparties and brokers"),
        ("sector", "Sector", "Market sectors"),
        ("strategy", "Strategy", "Trading and investment strategies"),
    ]
    for name, display, desc in type_defs:
        obj = OntologyType(name=name, display_name=display, description=desc)
        session.add(obj)
        type_ids[name] = obj.id
    await session.flush()
    return type_ids


async def seed_instruments(session: AsyncSession, type_ids: dict[str, uuid.UUID]) -> list[uuid.UUID]:
    ids = []
    for sector, tickers in SAMPLE_TICKERS.items():
        for ticker, name, industry in tickers:
            instrument = Instrument(
                ticker=ticker,
                name=name,
                instrument_type="equity",
                currency="USD",
                sector=sector,
                industry=industry,
                ontology_object_id=None,
            )
            session.add(instrument)
            ids.append(instrument.id)
    await session.flush()
    return ids


async def seed_counterparties(session: AsyncSession) -> list[uuid.UUID]:
    counterparties = [
        Counterparty(short_name="GS", legal_name="Goldman Sachs & Co.", counterparty_type="broker_dealer"),
        Counterparty(short_name="JPM", legal_name="JPMorgan Securities", counterparty_type="bank"),
        Counterparty(short_name="MS", legal_name="Morgan Stanley & Co.", counterparty_type="broker_dealer"),
        Counterparty(short_name="Citi", legal_name="Citigroup Global Markets", counterparty_type="bank"),
    ]
    for cp in counterparties:
        session.add(cp)
    await session.flush()
    return [cp.id for cp in counterparties]


async def seed_watchlist(session: AsyncSession, user_id: str = "default") -> uuid.UUID:
    wl = Watchlist(user_id=user_id, name="Default")
    session.add(wl)
    await session.flush()
    items = [
        WatchlistItem(watchlist_id=wl.id, ticker="AAPL", notes="Core holding"),
        WatchlistItem(watchlist_id=wl.id, ticker="MSFT", notes="Cloud growth"),
        WatchlistItem(watchlist_id=wl.id, ticker="NVDA", notes="AI/ML leader"),
        WatchlistItem(watchlist_id=wl.id, ticker="GOOGL", notes="Search monopolist"),
        WatchlistItem(watchlist_id=wl.id, ticker="SPY", notes="S&P 500 ETF"),
    ]
    for item in items:
        session.add(item)
    await session.flush()
    return wl.id


async def seed_all() -> dict:
    async with async_session() as session:
        async with session.begin():
            logger.info("Seeding ontology types...")
            type_ids = await seed_ontology_types(session)

            logger.info("Seeding instruments...")
            instrument_ids = await seed_instruments(session, type_ids)

            logger.info("Seeding counterparties...")
            counterparty_ids = await seed_counterparties(session)

            logger.info("Seeding watchlist...")
            watchlist_id = await seed_watchlist(session)

        logger.info(
            f"Seeded: {len(type_ids)} types, {len(instrument_ids)} instruments, "
            f"{len(counterparty_ids)} counterparties, 1 watchlist"
        )

    return {
        "ontology_types": type_ids,
        "instruments": instrument_ids,
        "counterparties": counterparty_ids,
        "watchlist_id": watchlist_id,
    }


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_all())