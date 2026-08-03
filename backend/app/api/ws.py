import asyncio
import json
import random
import re
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.middleware.auth import verify_token

logger = logging.getLogger(__name__)
router = APIRouter()

# 🔒 Validate ticker symbols - must be 1-5 alphanumeric chars
VALID_TICKER_PATTERN = re.compile(r'^[A-Z0-9]{1,5}$')
MAX_TICKERS = 50  # Prevent DoS via massive ticker lists

def validate_ticker(ticker: str) -> bool:
    """Validate ticker symbol format"""
    if not isinstance(ticker, str):
        return False
    return bool(VALID_TICKER_PATTERN.match(ticker.upper()))


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self._tasks: dict[WebSocket, asyncio.Task] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        task = self._tasks.pop(websocket, None)
        if task:
            task.cancel()

    def start_push(self, websocket: WebSocket, tickers: list[str]):
        task = asyncio.create_task(self._push_prices(websocket, tickers))
        self._tasks[websocket] = task

    async def _push_prices(self, websocket: WebSocket, tickers: list[str]):
        base_prices = {}
        for ticker in tickers:
            price = round(random.uniform(10, 500), 2)
            base_prices[ticker] = {"price": price, "prev_close": price}
        try:
            while True:
                for ticker in tickers:
                    base = base_prices.get(ticker, {"price": 100, "prev_close": 100})
                    change = round(random.uniform(-2.0, 2.0), 2)
                    new_price = round(base["price"] + change, 2)
                    if new_price <= 0:
                        new_price = round(base["price"] * 0.99, 2)
                    change_pct = round((new_price - base["prev_close"]) / base["prev_close"] * 100, 2)
                    base_prices[ticker] = {"price": new_price, "prev_close": base["prev_close"]}
                    msg = {
                        "ticker": ticker,
                        "price": new_price,
                        "change_pct": change_pct,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    await websocket.send_json(msg)
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            logger.debug(f"Price push task cancelled for {tickers}")
        except Exception as e:
            logger.error(f"Error pushing prices for {tickers}: {e}", exc_info=True)


manager = ConnectionManager()


@router.websocket("/ws/prices")
async def prices_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        payload = json.loads(data)

        # 🔒 Authenticate via token in initial message
        token = payload.get("token")
        if not token:
            await websocket.send_json({"error": "Authentication required. Send token in first message."})
            await websocket.close(code=4001)
            return

        user = verify_token(token)
        if user is None:
            await websocket.send_json({"error": "Invalid or expired token"})
            await websocket.close(code=4001)
            return

        await manager.connect(websocket)
        tickers = payload.get("tickers", ["AAPL", "MSFT", "GOOGL"])
        
        # 🔒 CRITICAL FIX: Validate all tickers
        if not isinstance(tickers, list):
            logger.warning(f"Invalid ticker format received: {type(tickers)}")
            await websocket.send_json({"error": "Invalid tickers format"})
            await manager.disconnect(websocket)
            return
        
        if len(tickers) > MAX_TICKERS:
            logger.warning(f"Too many tickers requested: {len(tickers)} (max {MAX_TICKERS})")
            await websocket.send_json({"error": f"Too many tickers (max {MAX_TICKERS})"})
            await manager.disconnect(websocket)
            return
        
        # Filter and validate each ticker
        validated_tickers = []
        for ticker in tickers:
            if validate_ticker(ticker):
                validated_tickers.append(ticker.upper())
        
        if not validated_tickers:
            logger.info("No valid tickers provided, using defaults")
            validated_tickers = ["AAPL", "MSFT", "GOOGL"]
        
        logger.info(f"WebSocket connection established for tickers: {validated_tickers}")
        manager.start_push(websocket, validated_tickers)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.debug("WebSocket client disconnected")
        manager.disconnect(websocket)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received on WebSocket: {e}")
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket handler: {e}", exc_info=True)
        manager.disconnect(websocket)
