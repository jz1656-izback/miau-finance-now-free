"""Data source layer — unified API for all external data providers.

Usage:
    from app.services.data import init_providers
    await init_providers()

    from app.services.data.manager import DataSourceManager
    manager = DataSourceManager()
    result = await manager.fetch('quote', 'AAPL')

    from app.services.data.registry import registry
    health = registry.health_all()
"""
import logging

logger = logging.getLogger(__name__)


async def init_providers():
    """Register all available data source providers."""
    import time
    start = time.monotonic()
    from app.services.data.registry import registry

    providers = []

    # No-key providers (always available)
    try:
        from app.services.data.providers.yahoo import YahooProvider
        providers.append(YahooProvider())
    except Exception as e:
        logger.warning(f"Failed to load YahooProvider: {e}")

    try:
        from app.services.data.providers.stockprices import StockPriceDevProvider
        providers.append(StockPriceDevProvider())
    except Exception as e:
        logger.warning(f"Failed to load StockPriceDevProvider: {e}")

    try:
        from app.services.data.providers.frankfurter import FrankfurterProvider
        providers.append(FrankfurterProvider())
    except Exception as e:
        logger.warning(f"Failed to load FrankfurterProvider: {e}")

    try:
        from app.services.data.providers.defillama import DefiLlamaProvider
        providers.append(DefiLlamaProvider())
    except Exception as e:
        logger.warning(f"Failed to load DefiLlamaProvider: {e}")

    try:
        from app.services.data.providers.securitiesdb import SecuritiesDBProvider
        providers.append(SecuritiesDBProvider())
    except Exception as e:
        logger.warning(f"Failed to load SecuritiesDBProvider: {e}")

    try:
        from app.services.data.providers.dumbstock import DumbStockProvider
        providers.append(DumbStockProvider())
    except Exception as e:
        logger.warning(f"Failed to load DumbStockProvider: {e}")

    # Key-required providers (only register if key is configured)
    from app.config import settings

    # Treasury / Fixed Income (uses FRED API key)
    try:
        if getattr(settings, 'fred_api_key', None) or environ.get("FRED_API_KEY", ""):
            # Check environment directly since settings may not expose fred_api_key
            pass
        from app.services.data.providers.treasury import TreasuryProvider
        providers.append(TreasuryProvider())
    except Exception:
        pass

    # Corporate Bonds (uses FRED API key — same as Treasury)
    try:
        from app.services.data.providers.bonds import CorporateBondsProvider
        providers.append(CorporateBondsProvider())
    except Exception:
        pass

    try:
        if settings.finnhub_api_key:
            from app.services.data.providers.finnhub import FinnhubProvider
            providers.append(FinnhubProvider())
    except Exception:
        pass

    try:
        if getattr(settings, 'coinpaprika_api_key', None):
            from app.services.data.providers.coinpaprika import CoinPaprikaProvider
            providers.append(CoinPaprikaProvider())
    except Exception:
        pass

    try:
        from app.services.data.providers.blocknative import BlocknativeProvider
        providers.append(BlocknativeProvider())
    except Exception:
        pass

    try:
        from app.services.data.providers.opensky import OpenSkyProvider
        providers.append(OpenSkyProvider())
    except Exception as e:
        logger.warning(f"Failed to load OpenSkyProvider: {e}")

    try:
        from app.services.data.providers.maritime import MaritimeProvider
        providers.append(MaritimeProvider())
    except Exception:
        pass

    try:
        from app.services.data.providers.mining import MiningProvider
        providers.append(MiningProvider())
    except Exception as e:
        logger.warning(f"Failed to load MiningProvider: {e}")

    try:
        from app.services.data.providers.mortgage import MortgageProvider
        providers.append(MortgageProvider())
    except Exception as e:
        logger.warning(f"Failed to load MortgageProvider: {e}")

    # Globe data providers
    try:
        from app.services.data.providers.corporate import CorporateDataSource
        providers.append(CorporateDataSource())
    except Exception:
        pass
    try:
        from app.services.data.providers.mining import MiningProvider
        providers.append(MiningProvider())
    except Exception:
        pass
    try:
        from app.services.data.providers.geopolitical import GeopoliticalDataSource
        providers.append(GeopoliticalDataSource())
    except Exception:
        pass
    try:
        from app.services.data.providers.energy import EnergyDataSource
        providers.append(EnergyDataSource())
    except Exception:
        pass
    try:
        from app.services.data.providers.alien import AlienDataSource
        providers.append(AlienDataSource())
    except Exception:
        pass
    try:
        from app.services.data.providers.conflict import ConflictDataSource
        providers.append(ConflictDataSource())
    except Exception:
        pass
    try:
        from app.services.data.providers.satellite import SatelliteDataSource
        providers.append(SatelliteDataSource())
    except Exception:
        pass
    try:
        from app.services.data.providers.cargo import CargoDataSource
        providers.append(CargoDataSource())
    except Exception:
        pass

    for provider in providers:
        registry.register(provider)

    elapsed = round((time.monotonic() - start) * 1000, 1)
    logger.info(f"Initialized {len(providers)} data source providers in {elapsed}ms")
    return providers
