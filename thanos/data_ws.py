# src/thanos/data_ws.py
import asyncio
import logging
from typing import Dict
from thanos.ws import WSClient
from thanos.config import load_cfg

log = logging.getLogger("thanos.data_ws")

async def handle_message(msg: Dict):
    if "result" in msg and msg["result"] is None:
        return
    log.info("WS message: %s", msg)

async def run_data_ws(env: str = "testnet"):
    cfg = load_cfg(env)
    ws_cfg = cfg.get("ws", {})

    uri = ws_cfg.get("uri")
    subs = []
    for market in cfg.get("markets", []):
        subs.extend(market.get("subscriptions", []))

    client = WSClient(
        uri,
        subs,
        ping_interval=ws_cfg.get("ping_interval", 20),
        ping_timeout=ws_cfg.get("ping_timeout", 10),
        max_backoff=ws_cfg.get("max_backoff", 60),
        on_message=handle_message,
    )

    task = asyncio.create_task(client.run())
    try:
        await task
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt – shutting down.")
    finally:
        await client.close()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    # wybierasz środowisko: testnet / mainnet
    asyncio.run(run_data_ws(env="testnet"))
