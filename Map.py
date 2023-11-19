from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys

class MapWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.map_layout = QVBoxLayout()
        self.setLayout(self.map_layout)

        # Set the geometry to match the original values
        self.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 1080 - 100)

        # Create a QWebEngineView to display the map
        self.map_view = QWebEngineView(self)
        self.map_view.setUrl(QUrl("https://maps.google.com"))
        self.map_layout.addWidget(self.map_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    map_widget = MapWidget(main_window)
    main_window.setCentralWidget(map_widget)

    # Set the same window title and size as in the original code
    main_window.setWindowTitle('Penang Maps')
    main_window.resize(1920, 1080)  # Adjust the size to match the original dimensions
    main_window.show()

    sys.exit(app.exec_())
