import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt

class PenangFlagWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(0, 86, 168))  # Blue
        gradient.setColorAt(0.5, QColor(255, 255, 255))  # White
        gradient.setColorAt(1, QColor(255, 204, 0))  # Yellow

        painter.setBrush(gradient)
        painter.drawRect(0, 0, self.width(), self.height())

class PenangIslandTouristKiosk(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Penang Island Tourist Kiosk (Start Up Page)")
        self.setGeometry(0, 0, 1920, 1080)

        # Set the central widget to a custom widget with the Penang flag colors
        penang_widget = PenangFlagWidget(self)
        self.setCentralWidget(penang_widget)

        self.title = QLabel("Welcome to the Penang Tourist Kiosk", self)
        self.title.setGeometry(10, 0, 1901, 141)
        font = QFont()
        font.setFamily("Arial")  # Set the font family
        font.setPointSize(60)
        font.setBold(True)  # Make the font bold
        self.title.setFont(font)

        image_label = QLabel(self)
        pixmap = QPixmap("C:/Users/justi/OneDrive - student.newinti.edu.my/ALL2/ptk design/PTKui/penang_bridge.jpg")
        image_label.setPixmap(pixmap)
        image_label.setGeometry(50, 300, 1000, 400)

        self.loginbutton = QPushButton("Login", self)
        self.loginbutton.setGeometry(890, 220, 851, 281)
        self.styleButton(self.loginbutton)
        self.loginbutton.clicked.connect(self.openLoginPage)  # Connect the button to open the login page

        self.registerbutton = QPushButton("Register", self)
        self.registerbutton.setGeometry(890, 600, 851, 281)
        self.styleButton(self.registerbutton)
        self.registerbutton.clicked.connect(self.openRegisterPage)  # Connect the button to open the register page

    def styleButton(self, button):
        button.setStyleSheet(
            "QPushButton {"
            "background: rgba(0, 0, 0, 50%);"  # Semi-transparent black background
            "color: white;"  # Text color
            "border: 2px solid white;"  # White border
            "border-radius: 10px;"  # Rounded corners
            "font-size: 36px;"  # Text size
            "}"
            "QPushButton:hover {"
            "background: rgba(0, 0, 0, 70%);"  # Slightly brighter when hovered
            "color: white;"  # Text color
            "border: 2px solid white;"  # White border
            "}"
        )

    def openLoginPage(self):
        # Import the Loginpage module and open the login page
        from LoginPage import LoginPageStart
        self.login_page = LoginPageStart()
        self.login_page.show()
        self.hide()  # Hide the main window

    def openRegisterPage(self):
        from RegisterPage import RegisterPageStart  # Import RegisterPage locally
        database = sqlite3.connect("ptk.db")
        self.register_page = RegisterPageStart(database)
        self.register_page.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    database = sqlite3.connect("ptk.db")  # Create or connect to the SQLite database

    # Create a users table if it doesn't exist
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, username TEXT)")
    cursor.close()

    mainWin = PenangIslandTouristKiosk()
    mainWin.show()
    sys.exit(app.exec_())
