import asyncio, json, logging, time
from tkinter import N
import websockets

log = logging.getLogger("thanos.ws")

class BinanceBookTickerWS:
    def __init__(self, symbol_ccxt: str):
        self.stream_symbol = symbol_ccxt.replace("/", "").lower()
        self.url = "wws://stream.tesnet.binance.vision/ws"
        self.best_bid = None
        self.best_ask = None
        self.last_ts = 0

    async def run(self):
        sub = {"method": "SUBSCRIBE", "params": [f"!bookTicker@{self.stream_symbol}"], "id": 1}
        while True:
            try:
                async with websockets.connect(self.url, ping_interval=20) as ws:
                    await ws.send(json.dumps(sub))
                    async for raw in ws:
                        msg = json.loads(raw)
                        b, a = msg.get("b"), msg.get("a")
                        if b is not None and a is not None:
                            try:
                                self.best_bid = float(b)
                                self.best_ask = float(a)
                                self.last_ts = time.time()
                                mid = (self.best_bid + self.best_ask) / 2
                                log.info("Book ticker: bid=%.2f ask=%.2f mid=%.2f", self.best_bid, self.best_ask, mid)
                            except Exception:
                                pass
            except Exception as e:
                log.error("WS error: %s -> reconnect in 2s", e)
                await asyncio.sleep(2)