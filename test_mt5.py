import MetaTrader5 as mt5

if not mt5.initialize():
    print("Initialize Failed:", mt5.last_error())
    quit()

print("Terminal Info:")
print(mt5.terminal_info())

print("\nAccount Info:")
print(mt5.account_info())

mt5.shutdown()