import MetaTrader5 as mt5
import time


class TradingEngine:

    def __init__(self):

        self.symbol = "BTCUSDm"

        # DEFAULTS (will be overwritten by dashboard)
        self.volume = 0.01
        self.tp_points = 200
        self.sl_points = 100

        self.max_trades = 3
        self.cooldown = 10
        self.last_trade_time = 0

    # ================= UPDATE SETTINGS FROM DASHBOARD =================

    def set_risk(self, volume, tp_points, sl_points):

        self.volume = float(volume)
        self.tp_points = float(tp_points)
        self.sl_points = float(sl_points)

        print("RISK UPDATED:",
              self.volume,
              self.tp_points,
              self.sl_points)

    # ================= CHECK TRADES =================

    def count_trades(self):

        positions = mt5.positions_get()
        if positions is None:
            return 0

        return sum(1 for p in positions if p.symbol == self.symbol)

    # ================= SAFETY =================

    def can_trade(self):

        if self.count_trades() >= self.max_trades:
            print("MAX TRADES REACHED")
            return False

        if time.time() - self.last_trade_time < self.cooldown:
            print("COOLDOWN ACTIVE")
            return False

        return True

    # ================= BUY =================

    def buy(self):

        if not self.can_trade():
            return "BLOCKED"

        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            return "NO TICK"

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": tick.ask,

            # USER CONTROLLED TP/SL
            "tp": tick.ask + self.tp_points * 0.01,
            "sl": tick.ask - self.sl_points * 0.01,

            "deviation": 20,
            "magic": 10001,
            "comment": "WEB BUY",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        self.last_trade_time = time.time()

        return result

    # ================= SELL =================

    def sell(self):

        if not self.can_trade():
            return "BLOCKED"

        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            return "NO TICK"

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": tick.bid,

            # USER CONTROLLED TP/SL
            "tp": tick.bid - self.tp_points * 0.01,
            "sl": tick.bid + self.sl_points * 0.01,

            "deviation": 20,
            "magic": 10001,
            "comment": "WEB SELL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        self.last_trade_time = time.time()

        return result