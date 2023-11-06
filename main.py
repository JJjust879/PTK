import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QFont,QPixmap
import sqlite3


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Welcome to Penag Island")
        self.setGeometry(100, 100, 1920, 1080)

        # Create a central widget for the main content
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the "Hello, User" label
        from LoginPage import currentemail
        database = sqlite3.connect("ptk.db")  # Connect to the SQLite database
        cursor = database.cursor()
        cursor.execute("SELECT username FROM users WHERE email = ?", (currentemail,))
        user = cursor.fetchone()
        cursor.close()
        username = user[0]

        hello_label = QLabel("Hello, "+username, self)
        hello_label.setGeometry(20, 20, 1920 // 5, 1080 // 6)
        hello_label.setAlignment(Qt.AlignCenter)
        hello_label.setFont(QFont("Arial", 28, QFont.Bold))  # Set the font for the label

        # Create the sidebar buttons
        button_style = (
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

        button_height = 100  # Adjust the button height
        button_width = 1920 // 5 - 40  # Adjust the button width

        #quiz
        self.quiz_widget = QWidget(self)
        self.quiz_layout = QVBoxLayout()
        self.quiz_widget.setLayout(self.quiz_layout)
        self.quiz_widget.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 1080 - 40)
        self.quiz_widget.hide()

        self.question_label = QLabel("What are colours of the Penang flag", self)
        self.quiz_layout.addWidget(self.question_label)

        self.answer_a = QRadioButton("Red, Blue, White")
        self.answer_b = QRadioButton("Blue, White, Yellow")
        self.answer_c = QRadioButton("Black, Yellow, Red")
        self.answer_d = QRadioButton("Red, Red, Yellow")

        self.quiz_layout.addWidget(self.answer_a)
        self.quiz_layout.addWidget(self.answer_b)
        self.quiz_layout.addWidget(self.answer_c)
        self.quiz_layout.addWidget(self.answer_d)

        self.quiz_button = QPushButton("Submit Answer", self)
        self.quiz_layout.addWidget(self.quiz_button)
        self.quiz_button.clicked.connect(self.check_answer)

        attractions_button = QPushButton("Attractions", self)
        attractions_button.setGeometry(20, 1080 // 6 + 40, button_width, button_height)
        attractions_button.setStyleSheet(button_style)
        attractions_button.clicked.connect(self.show_attractions)

        map_button = QPushButton("Map", self)
        map_button.setGeometry(20, 1080 // 6 + 40 + button_height, button_width, button_height)
        map_button.setStyleSheet(button_style)
        map_button.clicked.connect(self.show_map)

        trivia_button = QPushButton("Trivia", self)
        trivia_button.setGeometry(20, 1080 // 6 + 40 + 2 * button_height, button_width, button_height)
        trivia_button.setStyleSheet(button_style)
        trivia_button.clicked.connect(self.show_trivia)

        grab_button = QPushButton("Grab", self)
        grab_button.setGeometry(20, 1080 // 6 + 40 + 3 * button_height, button_width, button_height)
        grab_button.setStyleSheet(button_style)
        grab_button.clicked.connect(self.show_grab)

        logout_button = QPushButton("Logout", self)
        logout_button.setGeometry(20, 1080 // 6 + 40 + 4 * button_height, button_width, button_height)
        logout_button.setStyleSheet(button_style)
        logout_button.clicked.connect(self.logout)

        # Create a QLabel to display the current page
        self.page_label = QLabel("Welcome to the Main Page", self)
        self.page_label.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 1080 - 40)
        self.page_label.setFont(QFont("Arial", 28, QFont.Bold))  # Set the font for the label
    
    def show_attractions(self):
        self.page_label.setText("Attractions Page") 
        self.quiz_widget.hide()
    
    def show_map(self):
        self.page_label.setText("Map Page")
        self.quiz_widget.hide()
    
    def show_trivia(self):
        self.page_label.setText("Trivia Page")
        self.quiz_widget.show()

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

    def load_question(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM quiz_questions WHERE id = ?', (1,))  # Load the first question for demonstration
        question_data = cursor.fetchone()
        cursor.close()

        if question_data:
            self.question_label.setText(question_data[1])
            self.answer_a.setText(question_data[2])
            self.answer_b.setText(question_data[3])
            self.answer_c.setText(question_data[4])
            self.answer_d.setText(question_data[5])
            self.correct_answer = question_data[6]

    def check_answer(self):
        selected_option = None
        if self.answer_a.isChecked():
            selected_option = "A"
        elif self.answer_b.isChecked():
            selected_option = "B"
        elif self.answer_c.isChecked():
            selected_option = "C"
        elif self.answer_d.isChecked():
            selected_option = "D"

        if selected_option == self.correct_answer:
            feedback = "Correct!"
        else:
            feedback = "Incorrect. The correct answer is " + self.correct_answer

        # Add logic here to display feedback to the user

    def check_answer(self):
        pass
    
    def show_grab(self):
        self.page_label.setText("Grab Page")
        self.quiz_widget.hide()
    
    def logout(self):
        from StartupWindow import PenangIslandTouristKiosk
        self.StartupWindow = PenangIslandTouristKiosk()
        self.StartupWindow.show()
        self.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())
