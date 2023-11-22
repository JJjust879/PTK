from typing import Self
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem,QSizePolicy,QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from datetime import datetime
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


print("Current Working Directory: ", os.getcwd())

conn = sqlite3.connect("ptk.db")   #Create SQLite database for attractions
cursor = conn.cursor()    #Cursor object to interact with database
cursor.execute("""
            CREATE TABLE IF NOT EXISTS TicketsPurchased (
                cust_id INTEGER PRIMARY KEY,
                name string,
                email string,
                attraction_name TEXT,
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
    ("Penang Science Clusters","A hub for science and technology enthusiasts."),
    ("Penang Heritage Trust","Promoting the conservation of Penang's heritage."),
    ("Penang Permaculture Garden","A sustainable and educational garden located in Penang Digital Library."),
    ("Penang Golf Club","A popular gold course in a scenic settiing."),
    ("Penang Snake Temple","A temple with live snakes slithering around."),
    ("Penang Ghost Tour","Join a guided tour to explore the spooky side of Penang."),
    ("Penang Chocolate and Coffee Museum","Learn about the history of chovolate and coffee."),
    ("Penang Spice Garden","Explore a variety of spices and herbs."),
    ("The Top","Have a breathtaking 360 degree view of Penang"),
    ("Penang State Forestry Department","Offers eco-tourism activities in Penang's lush forests."),
    ("Penang Camera Museum","Showcases the evolution of cameras and photography."),
    ("Penang Adventure Park","Features activities like ziplining and canopy walks."),
    ("Penang Hill Owl Museum","A museum with a collection of owl-related artifacts and art."),
    ("Balik Pulau Mangrove Tour","A tour specializing in exploring the outbacks of Balik Pulau.")
]

#cursor.executemany("INSERT INTO Attractions (name, description) VALUES (?, ?)", attractions)


#Commit changes and close database connection
conn.commit()
conn.close() 


class TicketSystem(QWidget):

    def __init__(self,parent,email):
        super().__init__(parent)
        self.email=email
        self.tickets = []  # List to store ticket data
        self.attractions = attractions  # Define attractions to reference for class attribute
        self.current_scale = 1.0  # Initial scale factor

        self.setGeometry(1920 // 5, 20, 800, 960 - 40)
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
        self.entry_description.setMinimumHeight(100)
    
        #Create label + entry fields
        label_name = QLabel("Name: ")
        self.entry_name = QLineEdit()
        
        label_image = QLabel("Image: ")
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200) #set fixed size for images

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


        #Create a text area to display existing tickets
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setMinimumHeight(150)

        layout.addWidget(label_attraction)
        layout.addWidget(self.combo_attraction)
        layout.addWidget(label_description)
        layout.addWidget(self.entry_description)
        
        spacer = QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        layout.addWidget(label_image)
        layout.addWidget(self.image_label)

        spacer = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
    

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
        layout.addWidget(self.text_display)

        # Create a QLabel to display the current time
        self.time_label = QLabel()
        layout.addWidget(self.time_label)

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

        # Check if there are no tickets purchased
        if not (self.adult_count or self.child_count):
            self.text_display.append("Error: No tickets purchased.")
            return
        

        # Capture user input from the entry fields
        name = self.entry_name.text()
        adult_count = self.adult_count
        child_count = self.child_count
        selected_attraction_name = self.combo_attraction.currentText()

        # Insert ticket data in the database
        db = sqlite3.connect("ptk.db")
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO TicketsPurchased (name,email,attraction_name, no_of_adults, no_of_children)
            VALUES (?, ?, ?, ?, ?)
            """, (name,self.email ,selected_attraction_name, adult_count, child_count))


        # Commit the changes and close the connection
        db.commit()
        cursor.close()
        db.close

        # Add the new ticket to the list of tickets
        self.send_ticket_email(self.email,name,adult_count,child_count, selected_attraction_name)

        # Inform the user that the ticket has been created
        self.text_display.append("Success: Ticket information and details have been sent to your email.")


        # Optionally, clear the entry fields after creating a ticket
        self.entry_name.clear()

        self.adult_count = 0
        self.adult_label.setText(str(self.adult_count))
        self.child_count = 0
        self.child_label.setText(str(self.child_count))

        # Display the current time in the bottom box
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"Transaction Time: {current_time}")

    def send_ticket_email(self, email, name,adult_count,child_count, selected_attraction_name):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Use the appropriate port
        sender_email = 'penangislandtouristkiosk@gmail.com'  # Your email address
        sender_password = 'ibju zied jzjl xsiw'  # Your email password

        # Create the email message
        subject = "Your Ticket"
        body = "Thank you, "+ str(name) +", for purchasing a ticket/s on the Penang Island Tourist Kiosk.:" +str(selected_attraction_name)+ " No of Adults: "+str(adult_count)+" No of Child: " +str(child_count)
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
        except Exception as e:
            print("Email error:", e)
            QMessageBox.warning(self, "Warning", "Ticket purchased, but email sending failed. Please check your email settings or contact us at penangislandtouristkiosk@gmail.com.")

    def update_description(self):
        selected_attraction_name = self.combo_attraction.currentText()
        selected_attraction_description = None

        db = sqlite3.connect("ptk.db")
        cursor = db.cursor()

        # Corrected SELECT statement
        cursor.execute("SELECT description FROM attractions WHERE name=?", (selected_attraction_name,))

        # Fetch all rows from the table
        rows = cursor.fetchall()

        if rows:
            selected_attraction_description = rows[0][0]

            # Fetch the image file path from the attractions list
            selected_attraction_index = self.combo_attraction.currentIndex()
            selected_attraction_image_path = fr"C:/Users/justi/OneDrive - student.newinti.edu.my/ALL2/ptk design/PTKui/Images/{selected_attraction_name.replace(' ', '_')}.jpg" #retrieve images 
            

            #check if image exists
            if os.path.exists(selected_attraction_image_path):
                print("Image file exists.")
            else:
                print("Image file does not exist.")


            # Load and display the image in the QLabel
            pixmap = QPixmap(selected_attraction_image_path)

            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)
                print("Image loaded successfully")
            else:
                print(f"Failed to load image: {selected_attraction_image_path}")
                print(pixmap.toImage().isNull())  # Print additional information about the pixmap

        # Set the description in the entry field
        self.entry_description.setPlainText(selected_attraction_description)



