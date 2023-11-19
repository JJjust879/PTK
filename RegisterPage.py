import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QLineEdit,QMessageBox
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFont,QPixmap
from PyQt5.QtCore import Qt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

class RegisterPageStart(QWidget):
    def __init__(self,database):
        QWidget.__init__(self)
        self.database = database
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Penang Island Tourist Kiosk (Register Page)")
        self.setGeometry(0, 0, 1920, 1080)

        title = QLabel("Register", self)
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

        username_label = QLabel("Username:", self)
        username_label.setFont(QFont("Arial", 28, QFont.Bold))
        username_label.setGeometry(1000, 400, 500, 100)
        self.username_input = QLineEdit(self)
        self.username_input.setFont(QFont("Arial", 24))
        self.username_input.setGeometry(1000, 500, 900, 80)

        self.return_button = QPushButton("Return", self)
        self.styleButton(self.return_button)
        self.return_button.setGeometry(1000, 600, 400, 200)
        self.return_button.clicked.connect(self.openStartupWindow)

        register_button = QPushButton("Register", self)
        self.styleButton(register_button)
        register_button.setGeometry(1500, 600, 400, 200)
        register_button.clicked.connect(self.register)  # Connect the button to the register method

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

    def openStartupWindow(self):
        from StartupWindow import PenangIslandTouristKiosk
        self.StartupWindow = PenangIslandTouristKiosk()
        self.StartupWindow.show()
        self.hide()
    
    def register(self):
        email = self.email_input.text()
        username = self.username_input.text()

        # Validate email and username here (add your own validation logic)
        if not email or not username:
            QMessageBox.critical(self, "Error", "Please fill in all the fields.")
            return

        # Check if the email already exists in the database
        if self.email_exists(email):
            QMessageBox.critical(self, "Error", "An account with this email already exists.")
            return

        # Save data to the database
        try:
            cursor = self.database.cursor()
            cursor.execute("INSERT INTO users (email, username) VALUES (?, ?)", (email, username))
            self.database.commit()
            cursor.close()
            self.send_registration_email(email)

            self.hide()
            # Create and show the StartupWindow after closing the current window
            from StartupWindow import PenangIslandTouristKiosk
            self.StartupWindow = PenangIslandTouristKiosk()
            self.StartupWindow.show()

        except sqlite3.Error as e:
            print("SQLite error:", e)
            QMessageBox.critical(self, "Error", "Registration failed. Please try again.")

    def email_exists(self, email):
        # Check if the email already exists in the database
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None
        
    def send_registration_email(self, email):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Use the appropriate port
        sender_email = 'penangislandtouristkiosk@gmail.com'  # Your email address
        sender_password = 'ibju zied jzjl xsiw'  # Your email password

        # Create the email message
        subject = "Registration Confirmation"
        body = "Thank you for registering on the Penang Island Tourist Kiosk."
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, email, text)

            # Close the connection
            server.quit()

            QMessageBox.information(self, "Success", "Registration successful! An email has been sent to your registered email address.")
        except Exception as e:
            print("Email error:", e)
            QMessageBox.warning(self, "Warning", "Registration successful, but email sending failed. Please check your email settings.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    database = sqlite3.connect("ptk.db")  # Create or connect to the SQLite database

    # Create a users table if it doesn't exist
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, username TEXT)")
    cursor.close()

    mainWin = RegisterPageStart(database)

    mainWin.show()
    sys.exit(app.exec_())