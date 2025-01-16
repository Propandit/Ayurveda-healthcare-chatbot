import spacy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

nlp = spacy.load('en_core_web_sm')


class ChatbotApp(App):
    def build(self):
        self.title = "Chatbot"
        self.layout = BoxLayout(orientation='vertical')
        self.chat_history = TextInput(readonly=True, font_size=16, padding=(10, 10), size_hint=(1, 0.9))
        self.message_input = TextInput(font_size=16, padding=(10, 10), size_hint=(0.8, 0.1))
        self.send_button = Button(text="Send", size_hint=(0.2, 0.1))
        self.send_button.bind(on_press=self.send_message)
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(BoxLayout(size_hint=(1, 0.01)))  # Spacer
        self.layout.add_widget(BoxLayout(orientation='horizontal', size_hint=(1, 0.1)))
        self.layout.children[2].add_widget(self.message_input)
        self.layout.children[2].add_widget(self.send_button)
        return self.layout

    def send_message(self, instance):
        user_message = self.message_input.text
        if user_message.strip() == "":
            return

        chat_history_text = self.chat_history.text
        user_message_display = "You: " + user_message + "\n"
        self.chat_history.text = chat_history_text + user_message_display
        self.message_input.text = ""

        doc = nlp(user_message.lower())

    # Initialize the bot response
        bot_response = "Dr. Sophia: I'm sorry, I don't understand. Please try again or ask a different question."

    # Add your logic here to generate bot responses based on user input
        if "hello" in user_message.lower():
            bot_response = "Dr. Sophia: Hello! How can I assist you with your health today?"

        elif "side effects of" in user_message.lower():
            medication_name = user_message.lower().replace('side effects of', '').strip('?')
        # Replace this with actual side effects information for the medication
            medication_side_effects = get_medication_side_effects(medication_name)
            if medication_side_effects:
                bot_response = f"Dr. Sophia: The most common side effects of {medication_name} include {', '.join(medication_side_effects)}. However, it's important to speak with your doctor or pharmacist about any concerns you have regarding your medication."
            else:
                bot_response = f"Dr. Sophia: I couldn't find information about the side effects of {medication_name}. Please consult with a healthcare professional for more details."

        elif "corona" in user_message.lower() or "covid" in user_message.lower():
        # Provide information about COVID-19
            bot_response = "Dr. Sophia: COVID-19 is a viral respiratory illness caused by the SARS-CoV-2 virus. Common symptoms include fever, cough, shortness of breath, fatigue, body aches, and loss of taste or smell."

        self.chat_history.text += bot_response + "\n"


if __name__ == '__main__':
    ChatbotApp().run()
