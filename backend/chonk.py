#!/usr/bin/env python3
"""
🐱 Miau DatChonk — Data Eating Service
Chonk never sleeps. Chonk always eats. Chonk serves fast.

A standalone service that continuously fetches and caches market data
from free providers (yahoo, coingecko, frankfurter). The main API
reads from Chonk's cache for instant responses.

Usage:
    python chonk.py          # Start on default port 8765
    python chonk.py --port 9876  # Custom port
"""
import asyncio
import json
import logging
import sys
import time
from datetime import datetime, timezone
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, '.')
sys.path.insert(0, 'app')

logging.basicConfig(level=logging.INFO, format='🐱 %(message)s')
logger = logging.getLogger('chonk')

# === In-memory chonk cache ===
_chonk: dict[str, dict] = {}
_chonk_meta: dict[str, float] = {}  # key -> timestamp

POPULAR_TICKERS = ['AAPL','MSFT','GOOGL','AMZN','TSLA','SPY','QQQ','NVDA','META','JPM','V','WMT','JNJ','PG','DIS','NFLX','ADBE','CRM','INTC','AMD','BAC','PFE','KO','PEP','NKE','MRK','ABNB','UBER','SNAP']
CRYPTO_COINS = ['bitcoin','ethereum','solana','cardano','ripple','polkadot','dogecoin','avalanche-2']
FX_PAIRS = ['EUR','GBP','JPY','CHF','CAD','AUD','NZD','CNY']

CACHE_TTL = 300  # 5 minutes
CHUNK_SIZE = 5   # fetch 5 at a time
REFRESH_INTERVAL = 30  # refresh every 30 seconds — chonk is finance
CHONK_DB = "/tmp/chonk_db.json"  # persistent storage — chonk never forgets

async def _fetch_price(ticker: str) -> Optional[dict]:
    """Fetch a single price from Yahoo Finance directly (no app imports)."""
    try:
        import httpx
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d"
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, headers=headers)
            if r.status_code != 200:
                return None
            data = r.json()
            results = data.get("chart", {}).get("result", [])
            if not results:
                return None
            result = results[0]
            meta = result.get("meta", {})
            quotes = result.get("indicators", {}).get("quote", [{}])[0]
            closes = [c for c in quotes.get("close", []) if c is not None]
            if not closes:
                return None
            price = closes[-1]
            prev = closes[-2] if len(closes) >= 2 else price
            highs = [h for h in quotes.get("high", []) if h is not None]
            lows = [l for l in quotes.get("low", []) if l is not None]
            volumes = [v for v in quotes.get("volume", []) if v is not None]
            return {
                "ticker": ticker, "price": round(price, 4),
                "prev_close": round(prev, 4), "change": round(price - prev, 4),
                "change_pct": round((price - prev) / prev * 100, 2) if prev else 0,
                "high": round(max(highs), 4) if highs else price,
                "low": round(min(lows), 4) if lows else price,
                "volume": int(volumes[-1]) if volumes else 0,
            }
    except Exception as e:
        logger.debug(f"  ⚠️  {ticker}: {e}")
    return None

async def _fetch_crypto(coin: str) -> Optional[dict]:
    """Fetch crypto price from CoinGecko with rate limit delay."""
    try:
        import httpx
        import asyncio
        await asyncio.sleep(0.8)  # avoid CoinGecko rate limit
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_24hr_change=true")
            if r.status_code == 200:
                data = r.json()
                coin_data = data.get(coin, {})
                usd = coin_data.get("usd")
                if usd:
                    return {"ticker": coin, "price": usd, "change_pct": coin_data.get("usd_24h_change")}
            elif r.status_code == 429:
                logger.warning(f"  ⏳ CoinGecko rate limited for {coin}, will retry next cycle")
                await asyncio.sleep(3)  # backoff
    except Exception:
        pass
    return None

async def _fetch_fx(base: str) -> Optional[dict]:
    """Fetch FX rate from open.er-api.com (free, no key)."""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://open.er-api.com/v6/latest/USD")
            if r.status_code == 200:
                data = r.json()
                if data.get("result") == "success":
                    rates = data.get("rates", {})
                    rate = rates.get(base)
                    if rate:
                        return {"ticker": f"USD/{base}", "price": rate}
    except Exception:
        pass
    return None

async def chomp_ticker(ticker: str) -> None:
    """Chomp one ticker into the chonk."""
    data = await _fetch_price(ticker)
    if data:
        _chonk[f"price:{ticker}"] = data
        _chonk_meta[f"price:{ticker}"] = time.time()
        logger.info(f"  ✅ {ticker}  ${data.get('price', '?')}")

async def chomp_crypto(coin: str) -> None:
    """Chomp one coin into the chonk."""
    data = await _fetch_crypto(coin)
    if data:
        _chonk[f"crypto:{coin}"] = data
        _chonk_meta[f"crypto:{coin}"] = time.time()

async def chomp_all_fx() -> None:
    """Chomp all FX pairs in one API call."""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://open.er-api.com/v6/latest/USD")
            if r.status_code == 200:
                data = r.json()
                if data.get("result") == "success":
                    rates = data.get("rates", {})
                    for base in FX_PAIRS:
                        rate = rates.get(base)
                        if rate:
                            _chonk[f"fx:{base}"] = {"ticker": f"USD/{base}", "price": rate}
                            _chonk_meta[f"fx:{base}"] = time.time()
    except Exception:
        pass

def _save_chonk():
    """Save chonk to disk — chonk never forgets."""
    try:
        import json
        data = {
            "data": {k: v for k, v in _chonk.items()},
            "meta": {k: v for k, v in _chonk_meta.items()},
            "updated": time.time()
        }
        with open(CHONK_DB, "w") as f:
            json.dump(data, f, default=str)
    except Exception as e:
        logger.debug(f"chonk save error: {e}")

def _load_chonk():
    """Load chonk from disk — chonk remembers everything."""
    try:
        import json
        with open(CHONK_DB) as f:
            data = json.load(f)
        _chonk.update(data.get("data", {}))
        _chonk_meta.update(data.get("meta", {}))
        logger.info(f"📂 Loaded {len(_chonk)} entries from disk — chonk remembers")
    except FileNotFoundError:
        logger.info("🆕 No saved chonk found — starting fresh")
    except Exception as e:
        logger.debug(f"chonk load error: {e}")

async def chonk_feeding_round() -> dict:
    """One round of chonk feeding — eat all the data."""
    results = {"prices": 0, "crypto": 0, "fx": 0}
    
    # Eat stock prices in chunks
    for i in range(0, len(POPULAR_TICKERS), CHUNK_SIZE):
        chunk = POPULAR_TICKERS[i:i+CHUNK_SIZE]
        tasks = [chomp_ticker(t) for t in chunk]
        await asyncio.gather(*tasks)
        results["prices"] += len(chunk)
    
    # Eat crypto
    for coin in CRYPTO_COINS:
        await chomp_crypto(coin)
        results["crypto"] += 1
    
    # Eat FX (all in one call)
    await chomp_all_fx()
    results["fx"] = len(FX_PAIRS)
    
    return results

async def chonk_forever():
    """Chonk never sleeps. Chonk always eats."""
    logger.info("╔══════════════════════════════════════╗")
    logger.info("║   🐱 Miau DatChonk — Data Eater     ║")
    logger.info("║   Chonk never sleeps. Chonk eats.   ║")
    logger.info("║   Chonk never forgets.              ║")
    logger.info("╚══════════════════════════════════════╝")
    
    # Load saved chonk from disk — chonk remembers
    _load_chonk()
    
    # First feed — eat everything
    logger.info("🌙 First feed — chonk is hungry...")
    results = await chonk_feeding_round()
    logger.info(f"✅ First feed done: {results['prices']} prices, {results['crypto']} crypto, {results['fx']} fx")
    
    # Continuous feeding loop
    cycle = 1
    while True:
        logger.info(f"🔄 Chonk cycle #{cycle} — refreshing data...")
        start = time.time()
        results = await chonk_feeding_round()
        elapsed = time.time() - start
        logger.info(f"✅ Cycle #{cycle}: {results['prices']} prices, {results['crypto']} crypto, {results['fx']} fx in {elapsed:.1f}s")
        
        # Save to disk — chonk never forgets
        _save_chonk()
        
        cycle += 1
        await asyncio.sleep(REFRESH_INTERVAL)

# === HTTP API ===
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Miau DatChonk API", version="1.0.0")


@app.get("/", response_class=HTMLResponse)
async def chonk_page():
    """🐱 Miau DatChonk — web page of pure chonk"""
    prices = {k.replace("price:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("price:")}
    cryptos = {k.replace("crypto:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("crypto:")}
    fxs = {k.replace("fx:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("fx:")}
    
    chonk_ascii = """
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡶⠛⠉⠉⠀⠀⠀⠀⠀⠈⠙⠻⢶⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣧⠀⠀⠀⠀⠀
⠀⠀⠀⣰⠏⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⣤⣤⡄⠀⠀⠹⣧⠀⠀⠀⠀
⠀⠀⣼⠋⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠘⣷⠀⠀⠀
⠀⢰⡏⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢹⡇⠀⠀
⠀⣾⠁⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠈⣷⠀⠀
⢰⡇⠀⠀⠀⣤⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⠀⠀⢸⡇⠀
⢸⡇⣀⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣀⢸⡇⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀
⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀
⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀
⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀
"""
    
    def card(title, items, fmt="${:.2f}"):
        if not items:
            return f"<div class='card'><h3>{title}</h3><p class='dim'>🍽️  chonk is still eating...</p></div>"
        rows = "".join(f"<tr><td>{k}</td><td class='num'>{fmt.format(v) if v else '?'}</td></tr>" for k, v in sorted(items.items())[:15])
        more = f"<tr><td colspan='2' class='dim' style='text-align:center'>... and {len(items)-15} more</td></tr>" if len(items) > 15 else ""
        return f"<div class='card'><h3>{title} ({len(items)})</h3><table>{rows}{more}</table></div>"
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head><title>🐱 Miau DatChonk</title>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
      *{{margin:0;padding:0;box-sizing:border-box}}
      body{{font-family:'JetBrains Mono',monospace;background:#0a0a0a;color:#e0e0e0;overflow-x:hidden;position:relative}}
      /* Floating food rain */
      .food-rain{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden}}
      .food-item{{position:absolute;font-size:1.5rem;animation:fall linear infinite;opacity:0.15}}
      @keyframes fall{{0%{{transform:translateY(-10vh) rotate(0deg)}}100%{{transform:translateY(110vh) rotate(360deg)}}}}
      @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-20px)}}}}
      /* Food items scattered around */
      .food-scatter{{position:fixed;pointer-events:none;z-index:0;font-size:2rem;opacity:0.08}}
      
      .content{{position:relative;z-index:1;padding:30px;max-width:1200px;margin:0 auto}}
      h1{{font-size:2.2rem;color:#ffaa00;margin-bottom:4px;text-shadow:0 0 30px rgba(255,170,0,0.3);text-align:center}}
      .sub{{color:#888;font-size:0.8rem;margin-bottom:8px;text-align:center}}
      
      /* DATCHONK */
      .chonk-container{{text-align:center;margin:10px 0 20px;position:relative}}
      .chonk-art{{font-size:0.55rem;line-height:1.15;color:#ff8800;text-shadow:0 0 20px rgba(255,136,0,0.2);animation:float 4s ease-in-out infinite;display:inline-block;letter-spacing:1px;transform:scaleX(1.3)}}
      .chonk-label{{font-size:0.7rem;color:#ffaa00;margin-top:-10px;opacity:0.6;font-family:'JetBrains Mono',monospace;letter-spacing:4px}}
      .chonk-badge{{display:inline-block;background:rgba(255,136,0,0.1);border:1px solid rgba(255,136,0,0.25);border-radius:20px;padding:3px 12px;font-size:0.6rem;color:#ff8800;margin-top:4px}}
      
      .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:20px}}
      .card{{background:rgba(0,0,0,0.7);border:1px solid rgba(255,136,0,0.15);border-radius:12px;padding:16px;backdrop-filter:blur(10px)}}
      .card h3{{color:#ffaa00;font-size:0.85rem;margin-bottom:8px}}
      table{{width:100%;font-size:0.75rem}}
      td{{padding:2px 0;color:#aaa}}
      td.num{{text-align:right;color:#ffcc44}}
      .dim{{color:#555;font-size:0.7rem}}
      .footer{{margin-top:20px;text-align:center;color:#333;font-size:0.6rem}}
      
      /* cats running in background */
      .cat-run{{position:fixed;bottom:10px;font-size:2rem;animation:run linear infinite;z-index:0;pointer-events:none;opacity:0.1}}
      @keyframes run{{0%{{transform:translateX(-100px)}}100%{{transform:translateX(calc(100vw + 100px))}}}}
    </style>
    </head><body>
      <!-- Food rain background -->
      <div class="food-rain" id="foodRain"></div>
      
      <!-- Running cats -->
      <div class="cat-run" style="animation-duration:12s;bottom:30px">🐱🐟🐱🐟🐱</div>
      <div class="cat-run" style="animation-duration:18s;animation-delay:-5s;bottom:60px;font-size:1.5rem">🐈🐠🐈🐠🐈</div>
      <div class="cat-run" style="animation-duration:22s;animation-delay:-12s;bottom:15px;font-size:1.2rem">😸🍣😸🍣😸</div>
      
      <div class="content">
        <div class="sub">🍕 🍔 🍟 🌭 🍿 🥓</div>
        <h1>🐱 MIAU DATCHONK 🐱</h1>
        <div class="sub">chonk never sleeps · chonk always eats · chonk serves fast</div>
        
        <!-- DATCHONK in the middle -->
        <div class="chonk-container">
          <div class="chonk-art">{chonk_ascii}</div>
          <div class="chonk-label">🐟 DATCHONK · 20x CHONK · ALL DATA EATER 🐟</div>
          <div class="chonk-badge">🐱 {len(_chonk)} datums eaten · 📈 {len(prices)} stocks · ₿ {len(cryptos)} crypto · 💱 {len(fxs)} fx</div>
        </div>
        
        <div class="grid">
          {card("📈 STONKS", prices)}
          {card("₿ CRYPTO", cryptos, "{:.8f}")}
          {card("💱 FX RATES", fxs)}
        </div>
        
        <div class="footer">🐱 chonk v1.0 · om nom nom nom · https://github.com/LuZziD/cat-finance-analytics-shell-miau</div>
      </div>
      
      <script>
        // Food rain
        const foods = ['🍕','🍔','🍟','🌭','🍿','🥓','🍗','🍖','🥩','🍣','🍛','🍜','🍝','🌮','🌯','🥟','🍱','🍦','🍩','🍪','🧁','🍰','🎂','🍫','🍬','🍭','🫘','🥜','🌽','🥕','🥦','🧀','🥚','🍳','🥐','🍞','🥨','🧇','🥞','🧆','🥙'];
        const rain = document.getElementById('foodRain');
        for(let i=0;i<25;i++){{
          const el=document.createElement('div');
          el.className='food-item';
          el.textContent=foods[Math.floor(Math.random()*foods.length)];
          el.style.left=Math.random()*100+'%';
          el.style.animationDuration=(8+Math.random()*12)+'s';
          el.style.animationDelay=-(Math.random()*20)+'s';
          el.style.fontSize=(0.8+Math.random()*1.2)+'rem';
          rain.appendChild(el);
        }}
      </script>
    </body></html>
    """)


@app.get("/health")
async def health():
    return {
        "status": "chonky",
        "cached_prices": len([k for k in _chonk if k.startswith("price:")]),
        "cached_crypto": len([k for k in _chonk if k.startswith("crypto:")]),
        "cached_fx": len([k for k in _chonk if k.startswith("fx:")]),
    }


@app.get("/price/{ticker}")
async def get_price_chonk(ticker: str):
    """Get cached price from chonk. Returns instantly if available."""
    key = f"price:{ticker.upper()}"
    if key in _chonk:
        return {"source": "chonk", "data": _chonk[key]}
    return {"source": "chonk", "data": None, "note": f"{ticker} not in chonk yet"}


@app.get("/prices")
async def get_prices(tickers: str = Query("AAPL,MSFT,GOOGL")):
    """Get multiple cached prices from chonk."""
    t_list = [t.strip().upper() for t in tickers.split(",")]
    result = {}
    for t in t_list:
        key = f"price:{t}"
        if key in _chonk:
            result[t] = _chonk[key]
    return {"source": "chonk", "data": result, "count": len(result)}


@app.get("/chonk")
async def chonk_status():
    """Full chonk status report."""
    return {
        "prices": {k.replace("price:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("price:")},
        "crypto": {k.replace("crypto:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("crypto:")},
        "fx": {k.replace("fx:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("fx:")},
        "entries": len(_chonk),
    }

@app.get("/price/{ticker}")
async def get_price_chonk(ticker: str):
    """Get cached price from chonk. Returns instantly if available."""
    key = f"price:{ticker.upper()}"
    if key in _chonk:
        return {"source": "chonk", "data": _chonk[key]}
    return {"source": "chonk", "data": None, "note": f"{ticker} not in chonk yet"}

@app.get("/prices")
async def get_prices(tickers: str = Query("AAPL,MSFT,GOOGL")):
    """Get multiple cached prices from chonk."""
    t_list = [t.strip().upper() for t in tickers.split(",")]
    result = {}
    for t in t_list:
        key = f"price:{t}"
        if key in _chonk:
            result[t] = _chonk[key]
    return {"source": "chonk", "data": result, "count": len(result)}

@app.get("/chonk")
async def chonk_status():
    """Full chonk status report."""
    return {
        "prices": {k.replace("price:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("price:")},
        "crypto": {k.replace("crypto:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("crypto:")},
        "fx": {k.replace("fx:", ""): v.get("price") for k, v in _chonk.items() if k.startswith("fx:")},
        "entries": len(_chonk),
    }

def run(port: int = 8765):
    """Start chonk service."""
    import threading
    # Start feeding loop in background thread
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=lambda: loop.run_until_complete(chonk_forever()), daemon=True)
    t.start()
    # Start HTTP API
    logger.info(f"🐱 Miau DatChonk listening on :{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765
    run(port)
