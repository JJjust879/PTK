from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
import sqlite3
from PyQt5.QtGui import QFont

class QuizWidget(QWidget):
    answer_checked = pyqtSignal(str)

    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.quiz_layout = QVBoxLayout()
        self.setLayout(self.quiz_layout)

        # Increase the widget height and set the font size
        self.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 1080 // 2 - 40)
        
        # Create a label for "Trivia" at the top with a larger font size
        trivia_label = QLabel("Trivia", self)
        trivia_label.setFont(QFont("Arial", 36, QFont.Bold))  # Adjust the font size and style
        self.quiz_layout.addWidget(trivia_label)

        # Create a label for the question with word wrap, increase the font size
        self.question_label = QLabel("", self)
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Arial", 16))  # Adjust the font size
        self.quiz_layout.addWidget(self.question_label)

        # Create radio buttons for answer options
        self.answer_a = QRadioButton("", self)
        self.answer_b = QRadioButton("", self)
        self.answer_c = QRadioButton("", self)
        self.answer_d = QRadioButton("", self)

        # Adjust the font size for the answer options (radio buttons)
        font = QFont("Arial", 24)  # Set the font size for answer options
        self.answer_a.setFont(font)
        self.answer_b.setFont(font)
        self.answer_c.setFont(font)
        self.answer_d.setFont(font)

        self.quiz_layout.addWidget(self.answer_a)
        self.quiz_layout.addWidget(self.answer_b)
        self.quiz_layout.addWidget(self.answer_c)
        self.quiz_layout.addWidget(self.answer_d)

        # Create the "Submit Answer" button, increase the font size
        self.quiz_button = QPushButton("Submit Answer", self)
        self.quiz_button.setFont(QFont("Arial", 36))  # Adjust the font size
        self.quiz_layout.addWidget(self.quiz_button)
        self.quiz_button.clicked.connect(self.on_quiz_button_click)

        self.load_question()

    def load_question(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM quiz_questions ORDER BY RANDOM() LIMIT 1')
        question_data = cursor.fetchone()
        cursor.close()

        if question_data:
            self.question_label.setText(question_data[1])
            self.answer_a.setText(question_data[2])
            self.answer_b.setText(question_data[3])
            self.answer_c.setText(question_data[4])
            self.answer_d.setText(question_data[5])
            self.correct_answer = question_data[6]

    def on_quiz_button_click(self):
        selected_option = None

        if self.answer_a.isChecked():
            selected_option = self.answer_a.text()
        elif self.answer_b.isChecked():
            selected_option = self.answer_b.text()
        elif self.answer_c.isChecked():
            selected_option = self.answer_c.text()
        elif self.answer_d.isChecked():
            selected_option = self.answer_d.text()

        if selected_option == self.correct_answer:
            feedback = "Correct!"
        else:
            feedback = "Incorrect. The correct answer is " + self.correct_answer

        # Show feedback in a QMessageBox
        QMessageBox.information(self, "Quiz Feedback", feedback)

        # Refresh the quiz
        self.load_question()