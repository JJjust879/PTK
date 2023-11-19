import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QRadioButton, QFormLayout, QTextEdit, QTreeWidget, QTreeWidgetItem, QMessageBox, QHBoxLayout, QDialog, QFormLayout, QCheckBox, QSpacerItem
import sqlite3

class EditDialog(QDialog):
    def __init__(self, question_id, parent=None):
        super().__init__(parent)
        self.question_id = question_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit Question")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()

        cursor = adminApp.db_connection.cursor()
        cursor.execute('SELECT * FROM quiz_questions WHERE id = ?', (self.question_id,))
        question = cursor.fetchone()
        cursor.close()

        self.question_text = QTextEdit(self)
        self.question_text.setPlainText(question[1])

        self.option_a = QLineEdit(self)
        self.option_a.setText(question[2])

        self.option_b = QLineEdit(self)
        self.option_b.setText(question[3])

        self.option_c = QLineEdit(self)
        self.option_c.setText(question[4])

        self.option_d = QLineEdit(self)
        self.option_d.setText(question[5])

        self.correct_answer = QFormLayout()
        self.correct_answer.addRow(QCheckBox("Option A", checked=question[6] == question[2]))
        self.correct_answer.addRow(QCheckBox("Option B", checked=question[6] == question[3]))
        self.correct_answer.addRow(QCheckBox("Option C", checked=question[6] == question[4]))
        self.correct_answer.addRow(QCheckBox("Option D", checked=question[6] == question[5]))

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_changes)

        layout.addWidget(QLabel("Edit Question:"))
        layout.addWidget(self.question_text)
        layout.addWidget(QLabel("Answer Options:"))
        layout.addWidget(self.option_a)
        layout.addWidget(self.option_b)
        layout.addWidget(self.option_c)
        layout.addWidget(self.option_d)
        layout.addWidget(QLabel("Correct Answer:"))
        layout.addLayout(self.correct_answer)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_changes(self):
        question = self.question_text.toPlainText()
        option_a = self.option_a.text()
        option_b = self.option_b.text()
        option_c = self.option_c.text()
        option_d = self.option_d.text()

        if not (question and option_a and option_b and option_c and option_d):
            QMessageBox.warning(self, 'Validation Error', 'Please fill out all fields.')
            return

        correct_answer = None
        for i in range(self.correct_answer.rowCount()):
            radio_button = self.correct_answer.itemAt(i, QFormLayout.FieldRole).widget()
            if radio_button.isChecked():
                if i == 0:
                    correct_answer = option_a
                elif i == 1:
                    correct_answer = option_b
                elif i == 2:
                    correct_answer = option_c
                elif i == 3:
                    correct_answer = option_d
                break


        if not correct_answer:
            QMessageBox.warning(self, 'Validation Error', 'Please select the correct answer.')
            return

        cursor = adminApp.db_connection.cursor()
        cursor.execute('''
            UPDATE quiz_questions
            SET question=?, option_a=?, option_b=?, option_c=?, option_d=?, correct_answer=?
            WHERE id=?
        ''', (question, option_a, option_b, option_c, option_d, correct_answer, self.question_id))
        adminApp.db_connection.commit()
        cursor.close()
        QMessageBox.information(self, 'Question Saved', 'The question has been updated successfully.')
        self.accept()

class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_questions()
    
    def initUI(self):
        self.setWindowTitle("Admin Page")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.question_text = QTextEdit(self)
        self.option_a = QLineEdit(self)
        self.option_b = QLineEdit(self)
        self.option_c = QLineEdit(self)
        self.option_d = QLineEdit(self)

        self.correct_answer = QFormLayout()
        self.correct_answer.addRow(QRadioButton("A"))
        self.correct_answer.addRow(QRadioButton("B"))
        self.correct_answer.addRow(QRadioButton("C"))
        self.correct_answer.addRow(QRadioButton("D"))

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_question)

        self.return_button = QPushButton("Return", self)
        self.return_button.clicked.connect(self.openStartupWindow)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["ID", "Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer"])

        # Create a horizontal layout for the Delete, Edit, and Return buttons
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_question)

        self.edit_button = QPushButton("Edit", self)
        self.edit_button.clicked.connect(self.edit_question)
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.return_button)  # Move the return button to the same row

        layout.addWidget(QLabel("Add Question:"))
        layout.addWidget(self.question_text)
        layout.addWidget(QLabel("Answer Options:"))
        layout.addWidget(self.option_a)
        layout.addWidget(self.option_b)
        layout.addWidget(self.option_c)
        layout.addWidget(self.option_d)
        layout.addWidget(QLabel("Correct Answer:"))
        layout.addLayout(self.correct_answer)
        layout.addWidget(self.save_button)
        layout.addWidget(self.tree_widget)
        layout.addLayout(button_layout)  # Add the horizontal button layout
        layout.addStretch()
        layout.addWidget(self.return_button)  # Add the return button to the layout

        self.central_widget.setLayout(layout)

        self.db_connection = sqlite3.connect("ptk.db")
        self.create_table()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    def save_question(self):
        question = self.question_text.toPlainText()
        option_a = self.option_a.text()
        option_b = self.option_b.text()
        option_c = self.option_c.text()
        option_d = self.option_d.text()

        if not (question and option_a and option_b and option_c and option_d):
            QMessageBox.warning(self, 'Validation Error', 'Please fill out all fields.')
            return

        correct_answer = None
        for i in range(self.correct_answer.rowCount()):
            if self.correct_answer.itemAt(i, QFormLayout.FieldRole).widget().isChecked():
                correct_answer = [option_a, option_b, option_c, option_d][i]
                break

        if not correct_answer:
            QMessageBox.warning(self, 'Validation Error', 'Please select the correct answer.')
            return

        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO quiz_questions (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (question, option_a, option_b, option_c, option_d, correct_answer))
        self.db_connection.commit()
        cursor.close()
        QMessageBox.information(self, 'Question Saved', 'The question has been saved successfully.')

        self.question_text.clear()
        self.option_a.clear()
        self.option_b.clear()
        self.option_c.clear()
        self.option_d.clear()
        for i in range(self.correct_answer.rowCount()):
            self.correct_answer.itemAt(i, QFormLayout.FieldRole).widget().setChecked(False)

        self.load_questions()


    def load_questions(self):
        self.tree_widget.clear()
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM quiz_questions')
        questions = cursor.fetchall()
        for question in questions:
            item = QTreeWidgetItem(self.tree_widget, [str(question[0]), question[1], question[2], question[3], question[4], question[5], question[6]])
        cursor.close()

    def delete_question(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            question_id = int(selected_item.text(0))
            cursor = self.db_connection.cursor()
            cursor.execute('DELETE FROM quiz_questions WHERE id = ?', (question_id,))
            self.db_connection.commit()
            cursor.close()
            self.load_questions()
        else:
            QMessageBox.warning(self, 'No Selection', 'Please select a question to delete.')

    def edit_question(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            question_id = int(selected_item.text(0))
            dialog = EditDialog(question_id, self)
            if dialog.exec_() == QDialog.Accepted:
                self.load_questions()
        else:
            QMessageBox.warning(self, 'No Selection', 'Please select a question to edit.')

    def openStartupWindow(self):
        import StartupWindow
        self.StartupWindow = StartupWindow.PenangIslandTouristKiosk()
        self.StartupWindow.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    adminApp = AdminApp()
    adminApp.show()
    sys.exit(app.exec_())
