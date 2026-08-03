import httpx
from datetime import datetime
from typing import Optional

YAHOO_OPTIONS_URL = "https://query2.finance.yahoo.com/v7/finance/options/{}"

YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
}


async def get_options_chain(ticker: str, expiration: Optional[str] = None) -> dict:
    url = YAHOO_OPTIONS_URL.format(ticker)
    if expiration:
        url += f"?date={expiration}"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, headers=YAHOO_HEADERS)
            if r.status_code != 200:
                return {"ticker": ticker, "error": f"Yahoo Finance HTTP {r.status_code}", "calls": [], "puts": []}

            data = r.json()
            result = data.get("optionChain", {}).get("result", [])
            if not result:
                return {"ticker": ticker, "error": "No options data available", "calls": [], "puts": []}

            option_data = result[0]
            quote = option_data.get("quote", {})
            underlying_price = quote.get("regularMarketPrice")

            expiration_dates = option_data.get("expirationDates", [])
            options = option_data.get("options", [])

            calls = []
            puts = []

            for opt_group in options:
                for contract in opt_group.get("calls", []):
                    calls.append(_parse_contract(contract))
                for contract in opt_group.get("puts", []):
                    puts.append(_parse_contract(contract))

            return {
                "ticker": ticker,
                "underlying_price": underlying_price,
                "expiration_dates": expiration_dates,
                "calls": calls,
                "puts": puts,
                "as_of": datetime.now().isoformat(),
                "source": "Yahoo Finance",
            }

    except Exception as e:
        return {"ticker": ticker, "error": str(e), "calls": [], "puts": []}


def _parse_contract(contract: dict) -> dict:
    return {
        "strike": contract.get("strike"),
        "last_price": contract.get("lastPrice"),
        "bid": contract.get("bid"),
        "ask": contract.get("ask"),
        "volume": contract.get("volume"),
        "open_interest": contract.get("openInterest"),
        "implied_volatility": contract.get("impliedVolatility"),
        "expiration": contract.get("expiration"),
        "change": contract.get("change"),
        "percent_change": contract.get("percentChange"),
    }
