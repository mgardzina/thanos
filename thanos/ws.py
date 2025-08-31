# src/thanos/ws.py
import asyncio
import json
import logging
import random
from typing import Awaitable, Callable, Dict, List, Optional

import websockets
from websockets import WebSocketClientProtocol

log = logging.getLogger("thanos.ws")


class WSClient:
    """
    Robust Binance WebSocket client with:
    - secure WS (wss://)
    - ping/pong keepalive
    - exponential backoff + jitter reconnect
    - automatic re-subscription on reconnect
    - graceful shutdown
    """

    def __init__(
        self,
        uri: str,
        subscriptions: List[str],
        *,
        ping_interval: int = 20,
        ping_timeout: int = 10,
        max_backoff: int = 60,
        on_message: Optional[Callable[[Dict], Awaitable[None]]] = None,
    ) -> None:
        # Fix common typos
        uri = uri.replace("wws://", "wss://").replace("tesnet.", "testnet.")
        if not (uri.startswith("wss://") or uri.startswith("ws://")):
            raise ValueError(f"Invalid WS URI: {uri}")

        self.uri = uri
        self.subscriptions = subscriptions
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.max_backoff = max_backoff
        self.on_message = on_message

        self._ws: Optional[WebSocketClientProtocol] = None
        self._stop = asyncio.Event()

    async def _subscribe(self) -> None:
        if not self._ws or not self.subscriptions:
            return
        msg = {"method": "SUBSCRIBE", "params": self.subscriptions, "id": 1}
        await self._ws.send(json.dumps(msg))
        log.info("Subscribed: %s", self.subscriptions)

    async def _handle_messages(self) -> None:
        assert self._ws is not None
        async for raw in self._ws:
            try:
                data = json.loads(raw)
            except Exception:
                log.debug("Non-JSON WS payload: %r", raw)
                continue

            if self.on_message:
                try:
                    await self.on_message(data)
                except Exception as e:
                    log.exception("on_message error: %s", e)

    async def run(self) -> None:
        retries = 0
        while not self._stop.is_set():
            try:
                log.info("Connecting to WS: %s", self.uri)
                async with websockets.connect(
                    self.uri,
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout,
                ) as ws:
                    self._ws = ws
                    log.info("WS connected.")

                    await self._subscribe()
                    retries = 0  # reset after success

                    await self._handle_messages()

            except asyncio.CancelledError:
                log.info("WS run() cancelled.")
                break
            except Exception as e:
                log.error("WS error: %s", e)
            finally:
                self._ws = None

            if not self._stop.is_set():
                retries += 1
                base = min(self.max_backoff, 2**retries)
                delay = base + random.random()
                log.warning("Reconnecting in %.1fs...", delay)
                await asyncio.sleep(delay)

        log.info("WS loop terminated.")

    async def close(self) -> None:
        self._stop.set()
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
            self._ws = None
