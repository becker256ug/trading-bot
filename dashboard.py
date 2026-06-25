from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QComboBox,
    QTextEdit,
    QHBoxLayout
)

from PyQt6.QtCore import QTimer

from trading_engine import TradingEngine
from strategy import get_signal


class Dashboard(QWidget):

    def __init__(self, account_data):
        super().__init__()

        self.setWindowTitle("MT5 Trading Bot")
        self.resize(600, 400)

        self.engine = TradingEngine()
        self.running = False

        self.init_ui(account_data)

        # Bot loop (every 3 seconds)
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_bot)

    # ================= UI =================

    def init_ui(self, account_data):

        layout = QVBoxLayout()

        title = QLabel("MT5 Trading Bot Dashboard")
        layout.addWidget(title)

        login = QLabel(f"Account: {account_data['login']}")
        server = QLabel(f"Server: {account_data['server']}")
        name = QLabel(f"Trader: {account_data['name']}")
        balance = QLabel(f"Balance: ${account_data['balance']:.2f}")
        equity = QLabel(f"Equity: ${account_data['equity']:.2f}")

        layout.addWidget(login)
        layout.addWidget(server)
        layout.addWidget(name)
        layout.addWidget(balance)
        layout.addWidget(equity)

        # ================= SYMBOL SELECTOR =================
        symbol_row = QHBoxLayout()

        self.symbol_box = QComboBox()
        self.symbol_box.addItems(["BTCUSD", "EURUSD", "XAUUSD"])
        symbol_row.addWidget(QLabel("Symbol:"))
        symbol_row.addWidget(self.symbol_box)

        layout.addLayout(symbol_row)

        # ================= BUTTONS =================
        self.startBtn = QPushButton("Start Bot")
        self.stopBtn = QPushButton("Stop Bot")

        self.startBtn.clicked.connect(self.start_bot)
        self.stopBtn.clicked.connect(self.stop_bot)

        layout.addWidget(self.startBtn)
        layout.addWidget(self.stopBtn)

        # ================= LOG BOX =================
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

    # ================= BOT CONTROL =================

    def start_bot(self):

        self.engine.symbol = self.symbol_box.currentText()
        self.running = True
        self.timer.start(3000)

        self.log(f"Bot started on {self.engine.symbol}")

        QMessageBox.information(
            self,
            "Bot Started",
            f"Trading started on {self.engine.symbol}"
        )

    def stop_bot(self):

        self.running = False
        self.timer.stop()

        self.log("Bot stopped")

        QMessageBox.information(
            self,
            "Bot",
            "Bot Stopped"
        )

    # ================= BOT LOOP =================

    def run_bot(self):

        if not self.running:
            return

        # Always sync symbol (important if user changes dropdown later)
        self.engine.symbol = self.symbol_box.currentText()

        symbol = self.engine.symbol
        signal = get_signal(symbol)

        self.log(f"Signal: {signal} | Symbol: {symbol}")

        if signal == "BUY":

            result = self.engine.buy()
            self.log(f"BUY executed → {result}")

        elif signal == "SELL":

            result = self.engine.sell()
            self.log(f"SELL executed → {result}")

        else:
            self.log("No trade signal")

    # ================= LOGGING =================

    def log(self, message):
        self.log_box.append(message)