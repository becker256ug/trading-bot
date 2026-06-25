import MetaTrader5 as mt5


def connect():

    if not mt5.initialize():
        return False, f"Initialization Failed: {mt5.last_error()}"

    info = mt5.account_info()

    if info is None:
        return False, "No account connected"

    return True, "Connected"


def get_account_info():

    info = mt5.account_info()

    if info is None:
        return None

    return {
        "login": info.login,
        "name": info.name,
        "server": info.server,
        "balance": info.balance,
        "equity": info.equity
    }