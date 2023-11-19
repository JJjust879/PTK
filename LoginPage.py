import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QLineEdit,QMessageBox
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFont,QPixmap
from PyQt5.QtCore import Qt
import sqlite3

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

class LoginPageStart(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Penang Island Tourist Kiosk (Login Page)")
        self.setGeometry(0, 0, 1920, 1080)
        title = QLabel("Login", self)
        title.setFont(QFont("Arial", 48, QFont.Bold))
        title.setGeometry(50, 10, 500, 100)

        image_label = QLabel(self)
        pixmap = QPixmap("C:/Users/justi/OneDrive - student.newinti.edu.my/ALL2/ptk design/PTKui/Penang-Road-Famous-Teochew-Chendul.jpg")
        image_label.setPixmap(pixmap)
        image_label.setGeometry(50, 300, 1000, 400)


        email_label = QLabel("Email:", self)
        email_label.setFont(QFont("Arial", 28, QFont.Bold))
        email_label.setGeometry(1000, 200, 500, 100)
        self.email_input = QLineEdit(self)
        self.email_input.setFont(QFont("Arial", 24))
        self.email_input.setGeometry(1000, 300, 900, 80)

        self.return_button = QPushButton("Return", self)
        self.styleButton(self.return_button)
        self.return_button.setGeometry(1000, 400, 400, 200)
        self.return_button.clicked.connect(self.openStartupWindow)

        self.login_button = QPushButton("Login", self)
        self.styleButton(self.login_button)
        self.login_button.setGeometry(1500, 400, 400, 200)
        self.login_button.clicked.connect(self.verify_email)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(0, 86, 168))  # Blue
        gradient.setColorAt(0.5, QColor(255, 255, 255))  # White
        gradient.setColorAt(1, QColor(255, 204, 0))  # Yellow
        painter.setBrush(gradient)
        painter.drawRect(0, 0, self.width(), self.height())

    def styleButton(self, button):
        button.setStyleSheet(
            "QPushButton {"
            "background: rgba(0, 0, 0, 50%);"
            "color: white;"
            "border: 2px solid white;"
            "border-radius: 10px;"
            "font-size: 36px;"
            "}"
            "QPushButton:hover {"
            "background: rgba(0, 0, 0, 70%);"
            "color: white;"
            "border: 2px solid white;"
            "}"
        )
    
    def verify_email(self):
        email = self.email_input.text()

        if email=="quiz":
            from adminquizcontrol import AdminApp
            self.Admin=AdminApp()
            self.Admin.show()
            self.hide()
        
        elif email=="feedback":
            from feedbackcontrol import ComplaintsViewer
            self.feed=ComplaintsViewer()
            self.feed.show()
            self.hide()

        # Check if the email exists in the database
        elif self.is_valid_email(email):
            # Email exists, perform login actions here
            # Perform login actions here, e.g., open the main application window
            from main import MainApp
            self.Main_app=MainApp(email)
            self.Main_app.show()
            self.hide()

        else:
            # Email does not exist
            QMessageBox.critical(self, "Error", "Invalid email. Please try again.")

    def is_valid_email(self, email):
        # Check if the email exists in the database
        database = sqlite3.connect("ptk.db")  # Connect to the SQLite database
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None        
    
    def openStartupWindow(self):
        import StartupWindow
        self.StartupWindow = StartupWindow.PenangIslandTouristKiosk()
        self.StartupWindow.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = LoginPageStart()

    mainWin.show()
    sys.exit(app.exec_())
