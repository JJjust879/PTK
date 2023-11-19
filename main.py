import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3
from quiz import QuizWidget
from Map import MapWidget
from Ticketing import TicketSystem
from chatbot3 import TravelChatbot
from FEEDBACK import ComplaintWidget

class MainApp(QMainWindow):
    def __init__(self,email):
        super().__init__()
        self.currentemail=email
        self.initUI()
        self.initialize_database()
        self.QuizWidget = QuizWidget(self, self.db_connection)
        self.QuizWidget.hide()
        self.MapWidget = MapWidget(self)
        self.QuizWidget.show()
        self.Ticket= TicketSystem(self,self.currentemail)
        self.Ticket.hide()
        self.chatbot=TravelChatbot(self)
        self.chatbot.hide()
        self.feedback= ComplaintWidget(self)
        self.feedback.hide()
        

    def initUI(self):
        self.setWindowTitle("Welcome to Penang Island")
        self.setGeometry(100, 100, 1920, 1080)

        # Create a central widget for the main content
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a frame for the sidebar
        self.sidebar_frame = QWidget(self.central_widget)
        self.sidebar_frame.setGeometry(0, 0, 1920 // 5, 1080)
        self.sidebar_frame.setStyleSheet("background: rgba(0, 0, 0, 50%);")

        # Create the "Hello, User" label within the sidebar
        email=self.currentemail
        database = sqlite3.connect("ptk.db")  # Connect to the SQLite database
        cursor = database.cursor()
        cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        cursor.close()
        user=user[0]
        self.hello_label = QLabel("Hello, "+user, self.sidebar_frame)
        self.hello_label.setGeometry(20, 20, 1920 // 5 - 40, 1080 // 6)
        self.hello_label.setAlignment(Qt.AlignCenter)
        self.hello_label.setFont(QFont("Arial", 16, QFont.Bold))

        self.grab_label = QLabel(self)
        pixmap = QPixmap("C:/Users/justi/OneDrive - student.newinti.edu.my/ALL2/ptk design/PTKui/grab.png")
        self.grab_label.setPixmap(pixmap)
        self.grab_label.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 1080 - 100)
        self.grab_label.hide()

        # Create the sidebar buttons
        button_style = (
            "QPushButton {"
            "background: transparent;"
            "color: white;"
            "border: none;"
            "font-size: 36px;"
            "}"
            "QPushButton:hover {"
            "background: rgba(0, 0, 0, 70%);"
            "color: white;"
            "border: none;"
            "}"
        )

        button_height = 100
        button_width = 1920 // 5 - 40

        attractions_button = QPushButton("Attractions", self.sidebar_frame)
        attractions_button.setGeometry(20, 1080 // 6 + 40, button_width, button_height)
        attractions_button.setStyleSheet(button_style)
        attractions_button.clicked.connect(self.show_attractions)

        map_button = QPushButton("Map", self.sidebar_frame)
        map_button.setGeometry(20, 1080 // 6 + 40 + button_height, button_width, button_height)
        map_button.setStyleSheet(button_style)
        map_button.clicked.connect(self.show_map)

        trivia_button = QPushButton("Trivia", self.sidebar_frame)
        trivia_button.setGeometry(20, 1080 // 6 + 40 + 2 * button_height, button_width, button_height)
        trivia_button.setStyleSheet(button_style)
        trivia_button.clicked.connect(self.show_trivia)

        grab_button = QPushButton("Grab", self.sidebar_frame)
        grab_button.setGeometry(20, 1080 // 6 + 40 + 3 * button_height, button_width, button_height)
        grab_button.setStyleSheet(button_style)
        grab_button.clicked.connect(self.show_grab)

        chatbot_button = QPushButton("Chatbot", self.sidebar_frame)
        chatbot_button.setGeometry(20, 1080 // 6 + 40 + 4 * button_height, button_width, button_height)
        chatbot_button.setStyleSheet(button_style)
        chatbot_button.clicked.connect(self.show_chatbot)

        feedback_button = QPushButton("Feedback", self.sidebar_frame)
        feedback_button.setGeometry(20, 1080 // 6 + 40 + 5 * button_height, button_width, button_height)
        feedback_button.setStyleSheet(button_style)
        feedback_button.clicked.connect(self.show_feedback)

        logout_button = QPushButton("Logout", self.sidebar_frame)
        logout_button.setGeometry(20, 1080 // 6 + 40 + 6 * button_height, button_width, button_height)
        logout_button.setStyleSheet(button_style)
        logout_button.clicked.connect(self.logout)

        # Create a line to separate the sidebar and content
        line = QFrame(self.central_widget)
        line.setGeometry(1920 // 5, 0, 2, 1080)
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("background: white;")

    def show_attractions(self):
        self.QuizWidget.hide()
        self.MapWidget.hide()
        self.grab_label.hide()
        self.Ticket.show()
        self.chatbot.hide()
        self.feedback.hide()

    def show_map(self):
        self.QuizWidget.hide()
        # Show the map window
        self.MapWidget.show()
        self.grab_label.hide()
        self.Ticket.hide()
        self.chatbot.hide()
        self.feedback.hide()
        
    def show_trivia(self):
        self.QuizWidget.show()
        self.MapWidget.hide()
        self.Ticket.hide()
        self.chatbot.hide()
        self.grab_label.hide()
        self.feedback.hide()

    def show_grab(self):
        self.QuizWidget.hide()
        self.MapWidget.hide()
        self.grab_label.show()
        self.Ticket.hide()
        self.chatbot.hide()
        self.feedback.hide()
    
    def show_chatbot(self):
        self.QuizWidget.hide()
        self.MapWidget.hide()
        self.grab_label.hide()
        self.Ticket.hide()
        self.chatbot.show()
        self.feedback.hide()

    def show_feedback(self):
        self.QuizWidget.hide()
        self.MapWidget.hide()
        self.grab_label.hide()
        self.Ticket.hide()
        self.chatbot.hide()
        self.feedback.show()

    def logout(self):
        from StartupWindow import PenangIslandTouristKiosk
        self.StartupWindow = PenangIslandTouristKiosk()
        self.StartupWindow.show()
        self.hide()

    def initialize_database(self):
        self.db_connection = sqlite3.connect("ptk.db")
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                option_a TEXT,
                option_b TEXT,
                option_c TEXT,
                option_d TEXT,
                correct_answer TEXT
            )
        ''')
        self.db_connection.commit()
        cursor.close()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp("aaa")
    mainApp.show()
    sys.exit(app.exec_())
