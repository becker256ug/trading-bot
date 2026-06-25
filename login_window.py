from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QLabel
)

from mt5_connector import connect, get_account_info
from dashboard import Dashboard


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MT5 Trading Bot")
        self.resize(300, 150)

        title = QLabel("MT5 Trading Bot")
        status = QLabel("Ensure MetaTrader 5 is running and logged in.")

        self.connectBtn = QPushButton("Connect to MT5")
        self.connectBtn.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(status)
        layout.addWidget(self.connectBtn)

        self.setLayout(layout)

    def login(self):

        success, message = connect()

        if success:

            info = get_account_info()

            QMessageBox.information(
                self,
                "Success",
                "Connected to MT5"
            )

            self.dashboard = Dashboard(info)
            self.dashboard.show()

            self.close()

        else:

            QMessageBox.critical(
                self,
                "Connection Error",
                str(message)
            )