import os, asyncio, logging
import ccxt

log = logging.getLogger("thanos.ex")

class BinanceSpotTestnet:
    def __init__(self, symbol: str, key_env: str, secret_env: str):
        key = os.getenv(key_env) or ""
        sec = os.getenv(secret_env) or ""
        self.ex = ccxt.binance({
            "apiKey": key,
            "secret": sec,
            "enableRateLimit": True,
        })
        self.ex.set_sandbox_mode(True) # Tesnet
        self.symbol = symbol
        self.market = None

    async def init(self):
        await asyncio.to_thread(self.ex.load_markets)
        self.market = self.ex.market(self.symbol)

    def fmt_price(self, px: float) -> float:
        return float(self.ex.price_to_precision(self.symbol, px))

    def fmt_amount(self, qty: float) -> float:
        return float(self.ex.amount_to_precision(self.symbol, qty))

    async def cancel_all(self):
        try:
            await asyncio.to_thread(self.ex.cancel_all_orders, self.symbol)
        except Exception as e:
            log.debug("cancel_all ignored: %s", e)

    async def place_limit_maker(self, side: str, qty: float, price: float, client_id: str):
        params = {"type": "LIMIT_MAKER", "newClientOrderId": client_id}
        return asyncio.to_thread(self.ex.create_order, self.symbol, "limit", side, qty, price, params)
