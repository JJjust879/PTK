import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

class ComplaintWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Complaints Widget')
        self.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 800 - 40)

        self.label = QLabel('Enter your feedback:')
        self.label.setStyleSheet("font-weight: bold; font-size: 36px;")

        self.complaint_input = QLineEdit()
        self.complaint_input.setStyleSheet("font-size: 16px;")
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet("font-size: 18px;")
        self.submit_button.clicked.connect(self.submit_complaint)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.complaint_input)
        self.complaint_input.setMinimumHeight(500)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Connect to SQLite database
        self.connection = sqlite3.connect('ptk.db')
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint TEXT
            )
        ''')
        self.connection.commit()

    def submit_complaint(self):
        complaint_text = self.complaint_input.text()
        if complaint_text:
            cursor = self.connection.cursor()
            cursor.execute('INSERT INTO complaints (complaint) VALUES (?)', (complaint_text,))

            self.connection.commit()
            self.complaint_input.clear()
            self.show_popup("Feedback Submitted", "Thank you for your feedback!")

    def show_popup(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ComplaintWidget()
    widget.show()
    sys.exit(app.exec_())
