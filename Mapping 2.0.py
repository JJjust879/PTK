#AIzaSyCppAqEniqc-vFiJWTLLbv-81Or3PWmskM Google API Key

import sys
import io
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium import plugins
from folium.plugins import MarkerCluster
import requests


api_key = "AIzaSyCppAqEniqc-vFiJWTLLbv-81Or3PWmskM"

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Maps')  
        self.window_width, self.window_height = 1080, 1200
        self.setMinimumSize(self.window_width, self.window_height)  

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a search box and display results 
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter a place to search")
        self.search_box.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.search_box)

        self.result_div = QLabel()
        self.result_div.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_div)

        # Create a search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        coordinate = (5.354251704738007, 100.36121667588378)
        m = folium.Map(
            zoom_start=13,
            location=coordinate,
            tiles=None,  # no initial tile layer
            search_box_position='topleft'
        )

    def perform_search(self):
        search_string = self.search_box.text()
        search_and_display_results(search_string, self.result_div)

        self.search_box.clear()

def search_and_display_results(search_string, result_div):
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_string}&key={api_key}"

    search_results = requests.get(search_url).json()['results']

    for result in search_results:
        name = result['name']
        location = result['geometry']['location']

        popup_text = f"<b>{name}</b><br>{result['formatted_address']}"

        folium.Marker(
                location=location,
                popup=popup_text,
                icon=folium.Icon(color='blue')
            ).add_to(marker_cluster)

    result_div.setText(f"Found {len(search_results)} results.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
            QWidget {font-size: 35px;}
    ''')

    my_app = MyApp()
    my_app.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
