import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget

class ComplaintsViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Complaints Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.treewidget = QTreeWidget()
        self.treewidget.setHeaderLabels(['Complaints'])

        self.layout.addWidget(self.treewidget)

        self.bottom_layout = QVBoxLayout()
        
        self.return_button = QPushButton("Return")
        self.return_button.clicked.connect(self.openStartupWindow)
        self.bottom_layout.addWidget(self.return_button)

        self.layout.addLayout(self.bottom_layout)

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('ptk.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM complaints")
        data = cursor.fetchall()

        for row in data:
            parent_item = QTreeWidgetItem(self.treewidget, [f"ID: {row[0]}"])

            delete_button = QPushButton("Resolved")
            delete_button.clicked.connect(lambda _, item=parent_item: self.delete_complaint(item))

            self.treewidget.setItemWidget(parent_item, 0, delete_button)

            for idx, field in enumerate(row[1:]):
                child_item = QTreeWidgetItem(parent_item, [f"{cursor.description[idx + 1][0]}: {field}"])
                parent_item.addChild(child_item)

        connection.close()

    def delete_complaint(self, item):
        complaint_id = int(item.text(0).split(": ")[1])

        connection = sqlite3.connect('ptk.db')
        cursor = connection.cursor()

        cursor.execute("DELETE FROM complaints WHERE ID = ?", (complaint_id,))
        connection.commit()

        self.treewidget.takeTopLevelItem(self.treewidget.indexOfTopLevelItem(item))

        connection.close()

    def openStartupWindow(self):
        import StartupWindow
        self.StartupWindow = StartupWindow.PenangIslandTouristKiosk()
        self.StartupWindow.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComplaintsViewer()
    window.show()
    sys.exit(app.exec_())
