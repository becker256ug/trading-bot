import MetaTrader5 as mt5
import pandas as pd


def get_signal(symbol):

    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_M1,
        0,
        100
    )

    df = pd.DataFrame(rates)

    df["ema20"] = df["close"].ewm(span=20).mean()
    df["ema50"] = df["close"].ewm(span=50).mean()

    if df["ema20"].iloc[-1] > df["ema50"].iloc[-1]:
        return "BUY"

    if df["ema20"].iloc[-1] < df["ema50"].iloc[-1]:
        return "SELL"

    return None