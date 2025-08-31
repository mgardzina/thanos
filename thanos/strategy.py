from dataclasses import dataclass

@dataclass
class Quote:
    bid_px: float
    ask_px: float
    qty: float

class Quoter:
    def __init__(self, spread_bps: float):
        self.spread = spread_bps / 10000.0

    def quote(self, best_bid: float, best_ask: float, order_qty: float) -> Quote:
        mid = (best_bid + best_ask) / 2.0
        half = self.spread / 2.0
        bid = mid * (1 - half)
        ask = mid * (1 + half)
        return Quote(bid_px=bid, ask_px=ask, qty=order_qty)
