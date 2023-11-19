import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextBrowser, QHBoxLayout, QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class TravelChatbot(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.initUI()
        self.initialize_chatbot()
        self.add_chat_message("Chatbot: Hello! How can I assist you today?")
        self.response_buttons = self.create_response_buttons()
        self.show_response_buttons()

    def initUI(self):
        self.setGeometry(1920 // 5, 20, 1920 - 1920 // 5, 1080 // 2 - 40)

        self.layout = QVBoxLayout(self)

        self.chat_display = QTextBrowser()
        self.layout.addWidget(self.chat_display)

        self.user_input = QLineEdit()
        self.layout.addWidget(self.user_input)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.handle_user_input)
        self.layout.addWidget(self.send_button)

        self.responses = {
            "thanks": "You're welcome! If you have more questions, feel free to ask.",
            "about penang": "Penang is an island state located in Malaysia. It's known for its rich history, beautiful beaches, and delicious food. If you have specific questions about Penang, feel free to ask.",
            "help": " Please email us at penangislandtouristkiosk@gmail.com for additional help",
            "bye": "Goodbye! Have a great day!",
            # FAQ
            "what is penang known for": "Penang is renowned for its diverse culinary scene, historical sites, and vibrant street art.",
            "best time to visit penang": "The best time to visit Penang is generally from December to February when the weather is cooler and drier.",
            "how do i get to penang": "You can reach Penang by air, with Penang International Airport being the main entry point. Alternatively, you can take a bus or drive via the Penang Bridge from the mainland.",
            "how do i get to penang": "You can reach Penang by air, with Penang International Airport being the main entry point. Alternatively, you can take a bus or drive via the Penang Bridge from the mainland.",
            "is it safe to drink tap water in penang": "It is advisable to drink bottled or boiled water to avoid any health issues. Most hotels and restaurants provide bottled water.",
            "what is the local currency in penang": "The official currency is the Malaysian Ringgit (MYR). Money exchange services are available at the airport and various locations on the island.",
            "do i need a visa to visit penang": "Depending on your nationality, you may need a visa. Check with the Malaysian embassy or consulate in your country for specific requirements.",
            "what languages are spoken in penang": "The main languages spoken are Malay, English, Mandarin, and Tamil.",
            "how is public transportation in penang": "Penang has a well-developed public transportation system, including buses and taxis. Grab, a ride-sharing service, is also available.",
            "what are the must-try local dishes in penang": "Some must-try dishes include Char Kway Teow, Penang Laksa, Nasi Kandar, and Cendol.",
            "are there any cultural etiquette i should be aware of": "It is polite to remove your shoes when entering someone's home or a place of worship. Dress modestly when visiting religious sites.",
            "is there a specific dress code for the beaches in penang": "While there isn't a strict dress code, it's recommended to wear appropriate swimwear at the beaches.",
            "what are the popular tourist attractions in penang": "Popular attractions include George Town, Penang Hill, Kek Lok Si Temple, and Clan Jetties.",
            "are there any festivals or events in penang during my visit": "Check the local events calendar for festivals like Chinese New Year, Thaipusam, and the Penang International Food Festival.",
            "can i use credit cards in penang": "Credit cards are widely accepted in hotels, restaurants, and malls. However, it's advisable to carry some cash for small establishments and street vendors.",
            "is there a specific dress code for religious sites": "It's respectful to dress modestly when visiting temples or mosques. Ensure your shoulders and knees are covered.",
            "what is the tipping culture in penang": "Tipping is not mandatory, but it's appreciated. 10 percent is a common practice in restaurants, and rounding up taxi fares is customary.",
            "how do i get around george town": "George Town is easily navigable on foot, but you can also use bicycles, trishaws, or Grab services for longer distances.",
            "are there any health precautions i should take": "It's advisable to drink bottled water, use mosquito repellent, and be cautious about street food hygiene.",
            "can i rent a car in penang": "Yes, there are car rental services available for those who prefer self-driving. Ensure you have an international driving permit if required.",
            "are there any restrictions on photography": "Respect signage and locals' privacy, especially in cultural or religious areas. Always ask for permission before taking someone's photo.",
            "what are the opening hours of local businesses": "Most shops open from 10 am to 10 pm, but operating hours may vary. Some local markets start early in the morning.",
            "how is the internet connectivity in penang": "Penang has good internet connectivity, and most hotels, cafes, and shopping centers offer free Wi-Fi.",
            "what outdoor activities are available in penang": "Outdoor enthusiasts can explore Penang National Park, hike Penang Hill, or enjoy water activities at Batu Ferringhi Beach.",
            "are there any recommended day trips from penang": "Consider day trips to the mainland, visiting places like Kedah or Langkawi. Ferry services are available.",
            "is bargaining acceptable in penang markets": "Bargaining is common in markets. Start with a friendly negotiation, and don't be afraid to walk away if the price doesn't suit you.",
            "can i use my electrical appliances in penang": "The standard voltage is 230V, and the plug type is the British-style three-pin plug. Bring a suitable adapter if needed.",
            "what emergency numbers should i be aware of": "The emergency number for police, fire, and medical assistance is 999.",
            "are there any vegetarian or vegan options available": "Yes, many restaurants offer vegetarian and vegan options. Ask for 'sayur-sayuran' for vegetarian dishes.",
            "what is the time zone in penang": "Penang follows Malaysia Standard Time (MYT), which is UTC+8.",
            "are there any guided tours available in penang": "Yes, there are various guided tours for cultural, culinary, and historical experiences. Check with local tour operators for options.",
        }

        enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_shortcut.activated.connect(self.send_button.click)

    def initialize_chatbot(self):
        pass

    def handle_user_input(self):
        user_message = self.user_input.text()
        self.user_input.clear()
        self.hide_response_buttons()

        if user_message:
            self.add_chat_message("You: " + user_message)
            bot_response = self.generate_bot_response(user_message)
            self.add_chat_message("Chatbot: " + bot_response)
            self.show_response_buttons()

    def generate_bot_response(self, user_message):
        user_message = user_message.lower()

        if user_message in self.responses:
            return self.responses[user_message]

        # Check for specific FAQ questions
        if "penang" in user_message and "known for" in user_message:
            return self.responses["what is penang known for"]
        elif "best time to visit penang" in user_message:
            return self.responses["best time to visit penang"]
        elif "how do i get to penang" in user_message:
            return self.responses["how do i get to penang"] 
        elif "is it safe to drink tap water in penang" in user_message:
            return self.responses["is it safe to drink tap water in penang"]
        elif "what is the local currency in penang" in user_message:
            return self.responses["what is the local currency in penang"]
        elif "do i need a visa to visit penang" in user_message:
            return self.responses["do i need a visa to visit penang"]
        elif "what languages are spoken in penang" in user_message:
            return self.responses["what languages are spoken in penang"]
        elif "how is public transportation in penang" in user_message:
            return self.responses["how is public transportation in penang"]
        elif "what are the must-try local dishes in penang" in user_message:
            return self.responses["what are the must-try local dishes in penang"]
        elif "are there any cultural etiquette i should be aware of" in user_message:
            return self.responses["are there any cultural etiquette i should be aware of"]
        elif "what are the popular tourist attractions in penang" in user_message:
            return self.responses["what are the popular tourist attractions in penang"]
        elif "are there any festivals or events in penang during my visit" in user_message:
            return self.responses["are there any festivals or events in penang during my visit"] 
        elif "can i use credit cards in penang" in user_message:
            return self.responses["can i use credit cards in penang"]
        elif "is there a specific dress code for religious sites" in user_message:
            return self.responses["is there a specific dress code for religious sites"]
        elif "what is the tipping culture in penang" in user_message:
            return self.responses["what is the tipping culture in penang"]
        elif "how do i get around george town" in user_message:
            return self.responses["how do i get around george town"]
        elif "are there any health precautions i should take" in user_message:
            return self.responses["are there any health precautions i should take"]
        elif "can i rent a car in penang" in user_message:
            return self.responses["can i rent a car in penang"]
        elif "are there any restrictions on photography" in user_message:
            return self.responses["are there any restrictions on photography"]
        elif "what are the opening hours of local businesses" in user_message:
            return self.responses["what are the opening hours of local businesses"]
        elif "how is the internet connectivity in penang" in user_message:
            return self.responses["how is the internet connectivity in penang"]
        elif "what outdoor activities are available in penang" in user_message:
            return self.responses["what outdoor activities are available in penang"]
        elif "is bargaining acceptable in penang markets" in user_message:
            return self.responses["is bargaining acceptable in penang markets"]
        elif "can i use my electrical appliances in penang" in user_message:
            return self.responses["can i use my electrical appliances in penang"]
        elif "what emergency numbers should i be aware of" in user_message:
            return self.responses["what emergency numbers should i be aware of"]
        elif "are there any vegetarian or vegan options available" in user_message:
            return self.responses["are there any vegetarian or vegan options available"]
        elif "what is the time zone in penang" in user_message:
            return self.responses["what is the time zone in penang"]
        elif "are there any guided tours available in penang" in user_message:
            return self.responses["are there any guided tours available in penang"]
        # If no specific response, provide a generic message.
        return "I'm sorry, I didn't understand your question. Please ask something else."

    def add_chat_message(self, message):
        current_text = self.chat_display.toPlainText()
        self.chat_display.setPlainText(current_text + message + "\n")

    def create_response_buttons(self):
        response_buttons_layout = QHBoxLayout()
        response_buttons = []

        for response in self.responses:
            if ' ' not in response:
                button = QPushButton(response.capitalize())
                button.clicked.connect(lambda _, r=response: self.handle_response_button_click(r))
                response_buttons_layout.addWidget(button)
                response_buttons.append(button)

        self.layout.addLayout(response_buttons_layout)

        return response_buttons

    def show_response_buttons(self):
        for button in self.response_buttons:
            button.show()

    def hide_response_buttons(self):
        for button in self.response_buttons:
            button.hide()

    def handle_response_button_click(self, response):
        self.user_input.setText(response)

help