import sys
from typing import Self
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from datetime import datetime
import sqlite3
conn = sqlite3.connect("Kiosk.db")   #Create SQLite database for attractions
cursor = conn.cursor()    #Cursor object to interact with database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TicketsPurchased (
        cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_name TEXT,
        attraction_name TEXT,
        attraction_description TEXT,
        no_of_adults INTEGER,
        no_of_children INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS attractions (
        name TEXT PRIMARY KEY,
        description TEXT
    )
""")

attractions = [
    ("Georgetown","The historic heart of Penang with its well-preserved colonial architecture."),
    ("Penang Hill","A hill station offering panoramic views of the island."),
    ("Kek Lok Si Temple","The largest Buddhist temple in Malaysia with a towering pagoda."),
    ("Penang National Park","Home to diverse flora and fauna, including the famous canopy walkway."),
    ("Penang Butterfly Farm","A tropical butterfly sanctuary with thousands of colourful butterflies."),
    ("Cheong Fatt Tze Mansion (The Blue Mansion)","A historic Chinese courtyard house."),
    ("Penang Street Art","Murals and street installations around Georgetown."),
    ("Penang Peranakan Mansion","A museum showcasing Peranakan culture and heritage."),
    ("Dharmikarama Burmese Temple","One of the oldest Burmese temples outside Myanmar."),
    ("Penang War Museum","A historical museum within a WWII fort."),
    ("Fort Cornwallis","A star-shaped fort with historical significance."),
    ("Arulmigu Balathandayuthapani Temple (Waterfall Hill Temple)","A Hindu temple with a scenic setting."),
    ("Penang Time Tunnel","A 3D museum showcasing the history of Penang."),
    ("Penang 3D Trick Art Museum","An interactive museum with 3D art installations."),
    ("Clan Jetties of Penang","Historic waterfront settlements with tradditional house on stilts."),
    ("Penang Islamic Museum","Showcasing the history of Islam in Penang."),
    ("Penang Avatar Secret Garden","Illuminated garden with lighted displays."),
    ("Penang Aquarium","Home to a variety of marine life."),
    ("Penang Toy Museum","Houses a vast collection of toys from different eras."),
    ("Penang Ghost Museum","A museum featuring exibits on ghosts and supernatural folklore."),
    ("Penang Floating Mosque (Masjid Terapung Tanjung Bungah)","A beautiful mosque located on the waterfront."),
    ("Penang Bird Park","Home to a wide variety of bird species"),
    ("Upside Down Museum","A quirky museum where everything is upside down."),
    ("Penang Batik Factory","Learn about the traditional art of batik making."),
    ("Penang Orchid Garden","Displays a stunning collection of orchids."),
    ("Penang Khoo Kongsi","A Chinese clanhouse with intricate architecture."),
    ("Penang Hill Funicular Railway","Q scenic train ride to the top of Penang Hill."),
    ("Penang Tropical Fruit Farm","Explore a variety of tropical fruits."),
    ("Penang Youth Centre","A place for recreational and sports activities."),
    ("Penang State Art Gallery","Exhibits contemporary and traditional art."),
    ("The Habitat Penang Hill","A nature oark with a canopy walk and wildlife."),
    ("Penang Municipal Park (Youth Park)","A large recreational park with various facilities."),
    ("Penang International Airport","Modern airport with international connections."),
    ("Penang Science Clusters","A hub for science and technology enthusiasts."),
    ("Penang Hill Railway Station"," historic train station with colonial architecture."),
    ("Penang Heritage Trust","Promoting the conservation of Penang's heritage."),
    ("Penang Permaculture Garden","A sustainable and educational garden."),
    ("Penang Golf Club","A popular gold course in a scenic settiing."),
    ("Penang Snake Temple","A temple with live snakes slithering around."),
    ("Penang Ghost Tour","Join a guided tour to explore the spooky side of Penang."),
    ("Penang Chocolate and Coffee Museum","Learn about the history of chovolate and coffee."),
    ("Penang Batu Feringghi Night Market","A bustling night market by the beach."),
    ("Penang Spice Garden","Explore a variety of spices and herbs."),
    ("Penang Arts District","A creative hub with art galleries, studios, and street art."),
    ("Penang Street Food","Explore the diverse and delicious local cuisine."),
    ("Penang State Forestry Department","Offers eco-tourism activities in Penang's lush forests."),
    ("Penang Camera Museum","Showcases the evolution of cameras and photography."),
    ("Penang Adventure Park","Features activities like ziplining and canopy walks."),
    ("Penang Hill Owl Museum","A museum with a collection of owl-related artifacts and art."),
    ("Penang Thaipusam Festival","A Hindu festival celebrated with grand processions."),
    ("Penang Hill Monkey Cup Garden","A garden specializing in pitcher plants and other carnivorous plants.")
]

cursor.executemany("INSERT INTO Attractions (name, description) VALUES (?, ?)", attractions)


#Commit changes and close database connection
conn.commit()
conn.close() 


class TicketSystem(QWidget):

    def __init__(self):
        super().__init__()
        self.tickets = []  # List to store ticket data
        self.attractions = attractions  # Define attractions to reference for class attribute


        self.setWindowTitle("Penang Island")
        self.setGeometry(100, 100, 400, 300)

        self.create_gui()


    def create_gui(self):
        print("Setting up GUI")  # Add this print statement to check if create_gui is called
        layout = QVBoxLayout()

        # Attraction selection using ComboBox
        label_attraction = QLabel("Attraction: ")
        self.combo_attraction = QComboBox()
        self.combo_attraction.addItems([attraction[0] for attraction in self.attractions])
        self.combo_attraction.activated.connect(self.update_description)
        print("Signal connected")  # Add this print statement to check if the signal connection is successful

        #Attraction description
        label_description=QLabel("Description: ")
        self.entry_description=QTextEdit()

        #Create attraction images

    #Create label + entry fields
        label_name = QLabel("Name: ")
        self.entry_name = QLineEdit()

    # Create increase and decrease buttons for ticket (Adult, Child)
        adult_label = QLabel("Adults: ")
        self.adult_count = 0
        self.adult_label = QLabel(str(self.adult_count))
        adult_increase_button = QPushButton("+")
        adult_decrease_button = QPushButton("-")
        adult_increase_button.clicked.connect(self.increase_adult)
        adult_decrease_button.clicked.connect(self.decrease_adult)

        child_label = QLabel("Children: ")
        self.child_count = 0
        self.child_label = QLabel(str(self.child_count))
        child_increase_button = QPushButton("+")
        child_decrease_button = QPushButton("-")
        child_increase_button.clicked.connect(self.increase_child)
        child_decrease_button.clicked.connect(self.decrease_child)


    # Create a button to create a new ticket and cancel
        create_button = QPushButton("Buy Tickets")
        create_button.clicked.connect(self.create_ticket)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close) #Close the current window

        #Create a text area to display existing tickets
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)

        layout.addWidget(label_attraction)
        layout.addWidget(self.combo_attraction)
        layout.addWidget(label_description)
        layout.addWidget(self.entry_description)

        layout.addWidget(label_name)
        layout.addWidget(self.entry_name)

        layout.addWidget(adult_label)
        layout.addWidget(self.adult_label)
        layout.addWidget(adult_increase_button)
        layout.addWidget(adult_decrease_button)
        layout.addWidget(child_label)
        layout.addWidget(self.child_label)
        layout.addWidget(child_increase_button)
        layout.addWidget(child_decrease_button)

        layout.addWidget(create_button)
        layout.addWidget(cancel_button)
        layout.addWidget(self.text_display)

        self.setLayout(layout)

    def increase_adult(self):
        self.adult_count+=1
        self.adult_label.setText(str(self.adult_count))

    def decrease_adult(self):
        if self.adult_count>0:
            self.adult_count-=1
            self.adult_label.setText(str(self.adult_count))

    def increase_child(self):
        self.child_count+=1
        self.child_label.setText(str(self.child_count))

    def decrease_child(self):
        if self.child_count>0:
            self.child_count-=1
            self.child_label.setText(str(self.child_count))

    def create_ticket(self):
        # Handle creating a new ticket and adding it to the list

        # Capture user input from the entry fields
        customer_name = self.entry_name.text()

        # Inform the user that the ticket has been created
        self.text_display.append("Success: Ticket information and details have been sent to your email.")

    def update_description(self):
        print("Updating description")  # Add this print statement to check if update_description is called
        selected_attraction_name = self.combo_attraction.currentText()
        selected_attraction_description = None

        db = sqlite3.connect("Kiosk.db")
        cursor = db.cursor()

        # Corrected SELECT statement
        cursor.execute("SELECT description FROM attractions WHERE name=?", (selected_attraction_name,))

        # Fetch all rows from the table
        rows = cursor.fetchall()

        if rows:
            selected_attraction_description = rows[0][0]

        print("Selected Attraction:", selected_attraction_name)  # Add this print statement to check the selected attraction name
        print("Description from Database:", selected_attraction_description)  # Add this print statement to check the selected attraction description

    # Set the description in the entry field
        self.entry_description.setPlainText(selected_attraction_description)


        adult_count = self.adult_count
        child_count = self.child_count

        # Create a new ticket (for simplicity, using a dictionary)
        new_ticket = {
            "Attraction": selected_attraction_name,
            "Attraction Descriptions": selected_attraction_description,
            "Adults": adult_count,
            "Children": child_count
        }

        # Insert ticket data in the database
        db = sqlite3.connect("Kiosk.db")
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TicketsPurchased (
                cust_id INTEGER PRIMARY KEY,
                cust_name string,
                attraction_name TEXT,
                attraction_description TEXT,
                no_of_adults INTEGER,
                no_of_children INTEGER
            )
        """)

        cust_id = 1
        cust_name = "Stacy"

        cursor.execute("""
            INSERT INTO TicketsPurchased (cust_name, attraction_name, attraction_description, no_of_adults, no_of_children)
            VALUES (?, ?, ?, ?, ?)
            """, (cust_name, selected_attraction_name, selected_attraction_description, adult_count, child_count))


        # Commit the changes and close the connection
        db.commit()
        cursor.close()
        db.close

        # Add the new ticket to the list of tickets
        self.tickets.append(new_ticket)

        # Optionally, clear the entry fields after creating a ticket
        self.entry_name.clear()

        self.adult_count = 0
        self.adult_label.setText(str(self.adult_count))
        self.child_count = 0
        self.child_label.setText(str(self.child_count))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicketSystem()
    window.show()
    sys.exit(app.exec_())


