from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from trading_engine import TradingEngine
from strategy import get_signal


class Dashboard(QWidget):

    def __init__(self, account_data):
        super().__init__()

        self.account_data = account_data
        self.engine = TradingEngine()

        self.setWindowTitle("MT5 Trading Bot Dashboard")
        self.resize(500, 400)

        layout = QVBoxLayout()

        # ===== TITLE =====
        title = QLabel("MT5 Trading Bot Dashboard")
        layout.addWidget(title)

        # ===== ACCOUNT INFO =====
        layout.addWidget(
            QLabel(f"Account: {account_data.get('login', 'N/A')}")
        )

        layout.addWidget(
            QLabel(f"Server: {account_data.get('server', 'N/A')}")
        )

        layout.addWidget(
            QLabel(f"Trader: {account_data.get('name', 'N/A')}")
        )

        layout.addWidget(
            QLabel(
                f"Balance: ${account_data.get('balance', 0):.2f}"
            )
        )

        layout.addWidget(
            QLabel(
                f"Equity: ${account_data.get('equity', 0):.2f}"
            )
        )

        # ===== STATUS =====
        self.status_label = QLabel("Status: Connected")
        layout.addWidget(self.status_label)

        # ===== BUTTONS =====
        self.start_btn = QPushButton("Start Bot")
        self.stop_btn = QPushButton("Stop Bot")

        self.start_btn.clicked.connect(self.start_bot)
        self.stop_btn.clicked.connect(self.stop_bot)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_bot(self):

        try:
            signal = get_signal(self.engine.symbol)

            if signal == "BUY":

                result = self.engine.buy()

                QMessageBox.information(
                    self,
                    "BUY Signal",
                    f"BUY order sent\n\n{result}"
                )

            elif signal == "SELL":

                result = self.engine.sell()

                QMessageBox.information(
                    self,
                    "SELL Signal",
                    f"SELL order sent\n\n{result}"
                )

            else:

                QMessageBox.information(
                    self,
                    "No Signal",
                    "No valid trading signal found."
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def stop_bot(self):

        self.status_label.setText(
            "Status: Bot Stopped"
        )

        QMessageBox.information(
            self,
            "Bot",
            "Bot stopped."
        )