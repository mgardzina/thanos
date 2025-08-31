import asyncio, time, logging, yaml
from thanos.data_ws import run_data_ws
from dataclasses import dataclass
from dotenv import load_dotenv

from thanos.data_ws import run_data_ws
from thanos.exchange_binance import BinanceSpotTestnet
from thanos.strategy import Quoter

load_dotenv() # load .env

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("thanos")

@dataclass
class Config:
    exchange: str
    symbol: str
    order_qty: float
    spread_bps: float
    requote_interval_ms: int
    max_inventory: float
    api_key_env: str
    api_secret_env: str

def load_cfg(path="src/config.yaml") -> Config:
    with open(path,"r",encoding="utf-8") as f:
        d = yaml.safe_load(f)
    return Config(**d)

async def main():
    cfg = load_cfg()

    md = run_data_ws(cfg.symbol)
    ws_task = asyncio.create_task(md.run())

    ex = BinanceSpotTestnet(cfg.symbol, cfg.api_key_env, cfg.api_secret_env)
    await ex.init()

    quoter = Quoter(cfg.spread_bps)

    last_ts = 0
    tag = f"thanos-{int(time.time())}"

    try:
        while True:
            if md.best_bid is None or md.best_ask is None:
                await asyncio.sleep(0.1); continue
            if md.last_ts and (time.time() - md.last_ts > 10):
                log.warning("Market data stale (>10s). Skipping quotes.")
                await asyncio.sleep(0.5)
                continue

            now = int(time.time()*1000)
            if now - last_ts < cfg.requote_interval_ms:
                await asyncio.sleep(0.05); continue
            last_ts = now

            q = quoter.quote(md.best_bid, md.best_ask, cfg.order_qty)

            bid = ex.fmt_price(q.bid_px)
            ask = ex.fmt_price(q.ask_px)
            qty = ex.fmt_amount(q.qty)

            log.info("Requote -> bid=%.2f ask=%.2f qty=%s", bid, ask, qty)

            await ex.cancel_all()
            try:
                await ex.place_limit_maker("buy", qty, bid, client_id=tag+"-b")
            except Exception as e:
                log.warning("BUY failed: %s", e)
            try:
                await ex.place_limit_maker("sell", qty, ask, client_id=tag+"-a")
            except Exception as e:
                log.warning("SELL failed: %s", e)

            await asyncio.sleep(0.01)
    finally:
        ws_task.cancel()
        try:
            await ws_task
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(run_data_ws(env="testnet"))
