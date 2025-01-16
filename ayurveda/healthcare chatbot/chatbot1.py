import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import spacy

import random
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from fpdf import FPDF

# Define the generate_random_response function
def generate_random_response(responses):
    return random.choice(responses)

nlp = spacy.load('en_core_web_sm')

class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("730x620+0+0")
        self.root.bind('<Return>', self.enter_fun)

        main_frame = tk.Frame(self.root, bd=4, bg="powder blue", width=610)
        main_frame.pack()

        img_chat = Image.open("krishna.jpg")
        img_chat = img_chat.resize((190, 70), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img_chat)

        title_lbl = tk.Label(main_frame, bd=3, relief=tk.RAISED, anchor='center', width=730, compound=tk.LEFT,
                             image=self.photoimg, text="Dr. Maharishi Krishna", font=("arial", 30, "bold"),
                             bg="white", fg="green")
        title_lbl.pack(side=tk.TOP)

        self.scroll_y = ttk.Scrollbar(main_frame, orient=tk.VERTICAL)
        self.text = tk.Text(main_frame, width=65, height=20, bd=3, relief=tk.RAISED, font=('arial', 14),
                            yscrollcommand=self.scroll_y.set)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack()

        btn_frame = tk.Frame(self.root, bd=4, bg='white', width=730)
        btn_frame.pack()

        label_text = tk.Label(btn_frame, text="Type Something", font=('arial', '14', 'bold'), fg='green', bg='white')
        label_text.grid(row=0, column=0, padx=5, sticky=tk.W)

        self.entry = ttk.Entry(btn_frame, width=40, font=('arial', '14', 'bold'))
        self.entry.grid(row=0, column=1, padx=5, sticky=tk.W)

        self.send = tk.Button(btn_frame, text="SEND>>", command=self.send, font=('arial', '16', 'bold'), width=8,
                              bg='green')
        self.send.grid(row=0, column=2, padx=5, sticky=tk.W)

        self.clear = tk.Button(btn_frame, text="Clear", font=('arial', '16', 'bold'), width=8, bg='red', fg='white')
        self.clear.grid(row=1, column=0, padx=5, sticky=tk.W)
        
        self.report_btn = tk.Button(btn_frame, text="Get My Report", command=self.generate_report,
                                    font=('arial', '16', 'bold'), width=12, bg='blue', fg='white')
        self.report_btn.grid(row=1, column=1, padx=5, sticky=tk.W)
        
        self.save_report_btn = tk.Button(btn_frame, text="Save Report", command=self.save_report,
                                font=('arial', '16', 'bold'), width=12, bg='orange', fg='white')
        self.save_report_btn.grid(row=1, column=2, padx=5, sticky=tk.W)

        self.msg = ''
        self.label_11 = tk.Label(btn_frame, text=self.msg, font=('arial', '14', 'bold'), fg='red', bg='white')
        self.label_11.grid(row=1, column=1, padx=5, sticky=tk.W)

        # Initialize user information variables
        self.user_age = ''
        self.user_gender = ''
        self.user_name = ''
        self.user_build = ''
        self.user_skin_complexion = ''
        self.user_hair_type = ''
        self.user_energy_levels = ''
        self.user_activity_times = ''
        self.user_sleep_hours = ''
        self.user_sleep_trouble = ''
        self.user_appetite = ''
        self.user_food_cravings = ''

        
        # Initialize the PDF document
        self.pdf_report = None

    def enter_fun(self, event):
        self.send.invoke()

    def send(self):
        send = '\t\t\t' + 'You: ' + self.entry.get()
        self.text.insert(tk.END, '\n' + send)
        self.process_user_input()

    def process_user_input(self):
        user_input = self.entry.get().lower()

        greetings_responses = {
            'hello': 'Dr. Maharishi Krishna: Hello! How can I assist you with your health today?',
            'hi': 'Dr. Maharishi Krishna: Hi there! How can I assist you with your health today?',
            'hey': 'Dr. Maharishi Krishna: Hey! How can I assist you with your health today?',
            'good morning': 'Dr. Maharishi Krishna: Good morning! How can I assist you with your health today?',
            'good afternoon': 'Dr. Maharishi Krishna: Good afternoon! How can I assist you with your health today?',
            'good evening': 'Dr. Maharishi Krishna: Good evening! How can I assist you with your health today?',
            'how are you': 'Dr. Maharishi Krishna: I\'m just a computer program, but I\'m here to help you with your health questions!',
            'what can you do': 'Dr. Maharishi Krishna: I can provide information and assistance on various health topics. Just ask your question!',
            'thanks': 'Dr. Maharishi Krishna: You\'re welcome! If you have any more questions, feel free to ask.',
            'bye': 'Dr. Maharishi Krishna: Goodbye! Take care of your health.',
            'tell me about a healthy diet': 'Dr. Maharishi Krishna: A healthy diet should include a variety of fruits, vegetables, lean proteins, and whole grains. Avoid excessive sugar and processed foods.',
            'namaste': 'Dr. Maharishi Krishna: Namaste! Kaise aapki sehat ki sahayata kar sakta hoon?',
            'ram ram': 'Dr. Maharishi Krishna: Ram Ram! Kaise aapki sehat ki dekhbhal kar sakta hoon?',
            'jai shri krishna': 'Dr. Maharishi Krishna: Jai Shri Krishna! Aapki sehat ke liye kaise madad kar sakta hoon?',
            'kya aap Ayurvedic upchar bata sakte hain': 'Dr. Maharishi Krishna: Haan, main Ayurvedic upcharon ke baare mein salah de sakta hoon. Kripya apna sawal puchhein.',
            'dhanyavaad': 'Dr. Maharishi Krishna: Aapka dhanyavaad! Agar aapke paas aur sawalon ka jawab chahiye toh bataiye.',
            'alvida': 'Dr. Maharishi Krishna: Alvida! Apni sehat ka dhyan rakhiye.',
            'kaise hain aap': 'Dr. Maharishi Krishna: Main ek computer program hoon, lekin main aapki sehat ke sawalon mein madad karne ke liye yahan hoon.',
            'aap kaise hain': 'Dr. Maharishi Krishna: Main theek hoon! Aapka kaise khayal hai?',
            'shubh prabhat': 'Dr. Maharishi Krishna: Shubh prabhat! Kaise aapki sehat mein madad kar sakta hoon?',
            'aapko pranam': 'Dr. Maharishi Krishna: Aapko pranam! Kaise aapki sehat mein sahayata kar sakta hoon?',
            'kya aapke paas koi swasthya sujhav hai': 'Dr. Maharishi Krishna: Haan, main aapko swasthya sujhav de sakta hoon. Aapka sawal kya hai?',
            'aapka dhanyavaad': 'Dr. Maharishi Krishna: Aapka dhanyavaad! Kripya apna sawal puchhein, main madad karne ke liye yahan hoon.',
        }

        if user_input in greetings_responses:
            response = greetings_responses[user_input]
            self.text.insert(tk.END, '\n\n' + response)
        else:
            # Check for user's health condition description
            if 'suffering from' in user_input and any(keyword in user_input for keyword in ['pain', 'fever', 'illness']):
                ayurvedic_responses = [
                    "Dr. Maharishi Krishna: Greetings! I'm your Ayurvedic guide on the path to holistic well-being. Your Ayurvedic Prakriti, or Phenotype, is like your unique user manual for a balanced life. Are you excited to explore it?",
                    "Dr. Maharishi Krishna: Hello there! I'm here to help you uncover the mysteries of your Ayurvedic Prakriti, a key to understanding your body's needs. Ready to embark on this enlightening journey?",
                    "Dr. Maharishi Krishna: Namaste! Your Ayurvedic Prakriti is your blueprint for health. Together, we'll unlock its secrets and use them to enhance your lifestyle. Ready to get started?",
                    "Dr. Maharishi Krishna: Hi! Imagine your Ayurvedic Prakriti as your inner compass for well-being. I'm here to assist you in decoding it. Ready to explore your unique path?",
                    "Dr. Maharishi Krishna: Greetings, seeker of balance! Your Ayurvedic Prakriti holds the keys to a harmonious life. Shall we begin the journey of discovery together?",
                ]

                response = generate_random_response(ayurvedic_responses)
                self.text.insert(tk.END, '\n\n' + response)

                # Now, ask for basic information if it hasn't been collected yet
                if self.user_age == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: To assist you better, may I know your age?")
                elif self.user_gender == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: What is your gender?")
                elif self.user_name == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: What is your name?")
                
                elif self.user_build == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Describe your body build (slim, medium, heavy).")
                elif self.user_build == '':
                    self.user_build = user_input  # Store the user's body build
                    self.text.insert(tk.END, "\n\nAYURVEDA: What is your natural skin complexion? (Choose one option)\n"
                                  "1. Fair\n"
                                  "2. Medium\n"
                                  "3. Dark\n"
                                  "4. Other")
                elif self.user_skin_complexion == '':
                    self.user_skin_complexion = user_input  # Store the user's skin complexion
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Describe your hair type (thick, thin, wavy, curly, straight).")
                elif self.user_hair_type == '':
                    self.user_hair_type = user_input  # Store the user's hair type
                    self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: How would you describe your energy levels throughout the day (high, medium, low)?")
                    
                elif self.user_energy_levels == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: How would you describe your energy levels throughout the day (high, medium, low)?")
                elif self.user_activity_times == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Are you more active during specific times of the day?")

# Check if we are collecting additional information about sleep patterns
                elif self.user_sleep_hours == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: How many hours of sleep do you typically get each night?")
                elif self.user_sleep_trouble == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Do you have trouble falling asleep or staying asleep?")

# Check if we are collecting additional information about appetite
                elif self.user_appetite == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: How would you describe your appetite (strong, moderate, weak)?")
                elif self.user_food_cravings == '':
                    self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Do you have specific cravings for certain types of foods?")
                # Clear the input field
                self.entry.delete(0, 'end')
                return  # Exit the function to avoid further processing

            # Check if we are collecting user information
            if self.user_age == '':
                # Store the user's age
                self.user_age = user_input
                # Clear the input field
                self.entry.delete(0, 'end')
                # Ask for gender
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: What is your gender?")
            elif self.user_gender == '':
                # Store the user's gender
                self.user_gender = user_input
                # Clear the input field
                self.entry.delete(0, 'end')
                # Ask for name
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: What is your name?")
            elif self.user_name == '':
                # Store the user's name
                self.user_name = user_input
                # Clear the input field
                self.entry.delete(0, 'end')
                # Now you have collected user information, and you can use it as needed
                self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: Describe your body build (slim, medium, heavy).")
            elif self.user_build == '':
                # Store the user's body build
                self.user_build = user_input
                # Clear the input field
                self.entry.delete(0, 'end')
                # Ask about skin complexion
                self.text.insert(tk.END, "\n\nAYURVEDA: What is your natural skin complexion? (Choose one option)\n"
                                  "1. Fair\n"
                                  "2. Medium\n"
                                  "3. Dark\n"
                                  "4. Other")
            
            elif self.user_skin_complexion == '':
                    # Store the user's skin complexion
                self.user_skin_complexion = user_input
                    # Clear the input field
                self.entry.delete(0, 'end')
                    # Ask about hair type
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Describe your hair type (thick, thin, wavy, curly, straight).")
            elif self.user_hair_type == '':
                    # Store the user's hair type
                self.user_hair_type = user_input
                    # Clear the input field
                self.entry.delete(0, 'end')
                    # Now you have collected all the required information
                self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: How would you describe your energy levels throughout the day (high, medium, low)?")
                
            elif self.user_energy_levels == '':
            # Store the user's energy levels
                self.user_energy_levels = user_input
            # Clear the input field
                self.entry.delete(0, 'end')
            # Ask about activity times
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Are you more active during specific times of the day?")
        # Check if we are collecting additional information about activity times
            elif self.user_activity_times == '':
            # Store the user's activity times
                self.user_activity_times = user_input
            # Clear the input field
                self.entry.delete(0, 'end')
            # Ask about sleep hours
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: How many hours of sleep do you typically get each night?")
        # Check if we are collecting additional information about sleep patterns
            elif self.user_sleep_hours == '':
            # Store the user's sleep hours
                self.user_sleep_hours = user_input
            # Clear the input field
                self.entry.delete(0, 'end')
            # Ask about sleep trouble
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Do you have trouble falling asleep or staying asleep?")
            elif self.user_sleep_trouble == '':
            # Store the user's sleep trouble
                self.user_sleep_trouble = user_input
            # Clear the input field
                self.entry.delete(0, 'end')
            # Ask about appetite
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: How would you describe your appetite (strong, moderate, weak)?")
            elif self.user_appetite == '':
            # Store the user's appetite
                self.user_appetite = user_input
            # Clear the input field
                self.entry.delete(0, 'end')
            # Ask about food cravings
                self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Do you have specific cravings for certain types of foods?")
            elif self.user_food_cravings == '':
            # Store the user's food cravings
                self.user_food_cravings = user_input
            # Clear the input field
                self.entry.delete(0, 'end')
            # Now you have collected all the required information
                self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: Thank you for providing your information, {self.user_name}! "
                                      "How can I assist you further?")
                # Define dosha images (replace with actual image paths)
                vata_image_path = "vata.png"
                pitta_image_path = "pitta.png"
                kapha_image_path = "khapa.jpg"

# Determine the predominant dosha
                predominant_dosha = max(dosha_scores, key=dosha_scores.get)

# Define dosha descriptions and recommendations
                dosha_descriptions = {
                    "Vata": {
                    "description": "Your predominant dosha is Vata. Vata individuals are often creative, enthusiastic, and prone to change. They may have a slim build, fair skin, and thin hair.",
                    "recommendations": [
                            "Maintain a regular daily routine to balance Vata.",
                            "Stay warm and avoid exposure to cold and windy conditions.",
                            "Include warm, nourishing foods in your diet.",
                            "Practice relaxation techniques like yoga and meditation."
                     ]
                    },
                    "Pitta": {
                    "description": "Your predominant dosha is Pitta. Pitta individuals are known for their intelligence, ambition, and strong digestion. They often have a medium build, medium skin complexion, and medium-thick hair.",
                    "recommendations": [
                            "Keep cool and avoid overheating.",
                            "Consume cooling foods and herbs to balance Pitta.",
                            "Engage in activities that promote relaxation and stress reduction.",
                            "Maintain a regular meal schedule."
                        ]
                    },
                    "Kapha": {
                    "description": "Your predominant dosha is Kapha. Kapha individuals are characterized by stability, patience, and strong endurance. They typically have a heavy build, dark skin, and thick hair.",
                    "recommendations": [
                        "Stay active and engage in regular exercise to prevent stagnation.",
                        "Consume warm, light foods and spices to balance Kapha.",
                        "Practice invigorating and stimulating activities.",
                        "Keep your environment well-ventilated and dry."
                        ]
                    },
                    "Mixed Prakriti": {
                    "description": "Your Prakriti appears to be a combination of doshas. This means that you have a unique blend of characteristics from different doshas. It's important to balance all aspects of your Prakriti to maintain overall well-being.",
                    "recommendations": [
                        "Pay attention to how different doshas manifest in different aspects of your life and adjust your lifestyle accordingly.",
                        "Seek guidance from an Ayurvedic practitioner for personalized recommendations."
                        ]
                    }
                }

# Display the dosha description and recommendations
                dosha_description = dosha_descriptions.get(predominant_dosha, {}).get("description", "Unable to determine dosha description.")
                dosha_recommendations = dosha_descriptions.get(predominant_dosha, {}).get("recommendations", [])

                self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: Based on the information you provided, your predominant dosha is {predominant_dosha}.")
                self.text.insert(tk.END, f"\n\n{dosha_description}")

# Display dosha-specific images (replace 'dosha_image.png' with actual images)
                if predominant_dosha == "Vata":
                    dosha_image_path =  "vata.png"
                elif predominant_dosha == "Pitta":
                    dosha_image_path = "pitta.png"
                elif predominant_dosha == "Kapha":
                    dosha_image_path = "khapa.jpg"

                dosha_image = Image.open(dosha_image_path)
                dosha_image = dosha_image.resize((300, 300), Image.LANCZOS)  # Resize the image
                dosha_image = ImageTk.PhotoImage(dosha_image)
                # Insert the dosha image into the chat interface
                self.text.image_create(tk.END, image=dosha_image)
                self.text.insert(tk.END, '\n')  # Add a newline after the image
                self.text.yview(tk.END)  # 
                dosha_image_label = tk.Label(self, image=dosha_image)
                dosha_image_label.image = dosha_image  # Keep a reference to the image
                dosha_image_label.pack()

# Display dosha-specific recommendations
                if dosha_recommendations:
                    self.text.insert(tk.END, "\n\nHere are some recommendations for balancing your dosha:")
                    for recommendation in dosha_recommendations:
                        self.text.insert(tk.END, f"\n- {recommendation}")

# Add a closing message
                self.text.insert(tk.END, "\n\nIf you have any questions or need further assistance, please feel free to ask.")
                
                

            
            
            elif 'get my report' in user_input:
                self.generate_report()
                # Clear the input field
                self.entry.delete(0, 'end')

    def save_report(self):
        if self.pdf_report is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file_path:
                try:
                # Create a PDF document
                    doc = SimpleDocTemplate(file_path, pagesize=letter)
                    styles = getSampleStyleSheet()
                    Story = []

                # Add user information to the report
                    user_info = f"Name: {self.user_name}\nAge: {self.user_age}\nGender: {self.user_gender}"
                    user_info_para = Paragraph(user_info, styles["Normal"])
                    Story.append(user_info_para)
                    Story.append(Spacer(1, 12))

                # Build the PDF document
                    doc.build(Story)

                    self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: Your report has been saved as {file_path}.")
                except Exception as e:
                    print(f"Error saving PDF report: {str(e)}")
        else:
            self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Please generate the report first.")
    # Define Ayurvedic recommendations
        

    def generate_report(self):
        if self.user_age == '' or self.user_gender == '' or self.user_name == '':
            self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: I need more information to generate the report. "
                                  "Please provide your age, gender, and name.")
        else:
            # Define Ayurvedic recommendations
            ayurvedic_recommendations = {
            "Vata": {
            "dietary_recommendations": [
            "Include warm, nourishing foods in your diet.",
            "Limit cold and raw foods.",
            # Add more recommendations specific to Vata dosha
            ]   ,
            "ayurvedic_remedies": [
                "Ashwagandha and Brahmi can help balance Vata dosha.",
            # Add more remedies specific to Vata dosha
            ],
            "herbs": [
                "Triphala is beneficial for Vata constitution.",
            # Add more herbs specific to Vata dosha
            ],
            "exercises": [
            "Yoga and Tai Chi are suitable exercises for Vata individuals.",
            # Add more exercises specific to Vata dosha
            ],
            },
                "Pitta": {
        "dietary_recommendations": [
            "Favor cooling foods like cucumbers and mint.",
            "Avoid spicy and hot foods.",
            "Stay hydrated with cool drinks.",
            # Add more recommendations specific to Pitta dosha
        ],
        "ayurvedic_remedies": [
            "Aloe vera and coriander can help balance Pitta dosha.",
            # Add more remedies specific to Pitta dosha
        ],
        "herbs": [
            "Neem is beneficial for Pitta constitution.",
            # Add more herbs specific to Pitta dosha
        ],
        "exercises": [
            "Swimming and walking are suitable exercises for Pitta individuals.",
            # Add more exercises specific to Pitta dosha
        ],
    },
        "Kapha": {
        "dietary_recommendations": [
            "Consume warm, light foods.",
            "Limit heavy and oily foods.",
            # Add more recommendations specific to Kapha dosha
        ],
        "ayurvedic_remedies": [
            "Ginger and cinnamon can help balance Kapha dosha.",
            # Add more remedies specific to Kapha dosha
        ],
        "herbs": [
            "Trikatu is beneficial for Kapha constitution.",
            # Add more herbs specific to Kapha dosha
        ],
        "exercises": [
            "Aerobic exercises like jogging and cycling are suitable for Kapha individuals.",
            # Add more exercises specific to Kapha dosha
        ],
    },
}

        # Create a PDF report
            self.pdf_report = self.create_pdf_report()

        # Determine the predominant dosha
            predominant_dosha = max(dosha_scores, key=dosha_scores.get)

        # Display dosha-specific recommendations
            if predominant_dosha in ayurvedic_recommendations:
                recommendations = ayurvedic_recommendations[predominant_dosha]
                self.text.insert(tk.END, f"\n\nDr. Maharishi Krishna: Your predominant dosha is {predominant_dosha}.")
                self.text.insert(tk.END, "\n\nDietary Recommendations:")
                for recommendation in recommendations["dietary_recommendations"]:
                    self.text.insert(tk.END, f"\n- {recommendation}")

                self.text.insert(tk.END, "\n\nAyurvedic Remedies:")
                for remedy in recommendations["ayurvedic_remedies"]:
                    self.text.insert(tk.END, f"\n- {remedy}")

                self.text.insert(tk.END, "\n\nHerbs:")
                for herb in recommendations["herbs"]:
                    self.text.insert(tk.END, f"\n- {herb}")

                self.text.insert(tk.END, "\n\nExercises:")
                for exercise in recommendations["exercises"]:
                    self.text.insert(tk.END, f"\n- {exercise}")

        # Display a message to the user
            self.text.insert(tk.END, "\n\nDr. Maharishi Krishna: Your report has been generated. "
                                  "You can download it using the 'Save Report' button.")

    def create_pdf_report(self):
        try:
        # Create a PDF document
            doc = SimpleDocTemplate("health_report.pdf", pagesize=letter)
            styles = getSampleStyleSheet()
            Story = []

        # Add user information to the report
            user_info = f"Name: {self.user_name}\nAge: {self.user_age}\nGender: {self.user_gender}"
            user_info_para = Paragraph(user_info, styles["Normal"])
            Story.append(user_info_para)
            Story.append(Spacer(1, 12))

        # Add more content to the report if needed
        # ...

        # Build the PDF document
            doc.build(Story)
            return doc  # Return the generated document
        except Exception as e:
            print(f"Error creating PDF report: {str(e)}")
            return None  # Return None in case of an error
        
    # Define a function to calculate dosha scores
class DoshaCalculator:
    def __init__(self):
        self.user_age = ''
        self.user_gender = ''
        self.user_name = ''
        self.user_build = ''
        self.user_skin_complexion = ''
        self.user_hair_type = ''
        self.user_energy_levels = ''
        self.user_activity_times = ''
        self.user_sleep_hours = ''
        self.user_sleep_trouble = ''
        self.user_appetite = ''
        self.user_food_cravings = ''

    def calculate_dosha_scores(self):
        dosha_scores = {
            "Vata": 0,
            "Pitta": 0,
            "Kapha": 0
        }

        # Assign scores based on user responses
        vata_attributes = [
            self.user_build, self.user_skin_complexion, self.user_hair_type, 
            self.user_energy_levels, self.user_activity_times, 
            self.user_sleep_hours, self.user_sleep_trouble, self.user_appetite, 
            self.user_food_cravings
        ]
        
        pitta_attributes = [
            self.user_build, self.user_skin_complexion, self.user_hair_type, 
            self.user_energy_levels, self.user_activity_times, 
            self.user_sleep_hours, self.user_sleep_trouble, self.user_appetite, 
            self.user_food_cravings
        ]
        
        kapha_attributes = [
            self.user_build, self.user_skin_complexion, self.user_hair_type, 
            self.user_energy_levels, self.user_activity_times, 
            self.user_sleep_hours, self.user_sleep_trouble, self.user_appetite, 
            self.user_food_cravings
        ]

        for dosha, attributes in [("Vata", vata_attributes), ("Pitta", pitta_attributes), ("Kapha", kapha_attributes)]:
            for attribute in attributes:
                response = attribute.lower()
                if dosha == "Vata":
                    dosha_scores[dosha] += vata_scores.get(response, 0)
                elif dosha == "Pitta":
                    dosha_scores[dosha] += pitta_scores.get(response, 0)
                elif dosha == "Kapha":
                    dosha_scores[dosha] += kapha_scores.get(response, 0)

        return dosha_scores

# Define scores for each dosha attribute
vata_scores = {
    "slim": -1, "medium": 0, "heavy": 1,
    "fair": -1, "medium": 0, "dark": 1,
    "thin": -1, "medium": 0, "thick": 1,
    "low": -1, "medium": 0, "high": 1,
    "more active in the evening": -1, "no specific pattern": 0, "more active in the morning": 1,
    "trouble falling asleep/staying asleep": -1, "normal sleep": 0, "sound sleeper": 1,
    "variable": -1, "moderate": 0, "strong": 1,
    "craving warm, spicy foods": -1, "no specific cravings": 0, "craving sweet, cold foods": 1
}

# Define scores for Pitta attributes
pitta_scores = {
    "slim": 0, "medium": 0, "heavy": -1,  # Body build
    "fair": 0, "medium": 0, "dark": -1,  # Skin complexion
    "thin": 0, "medium": 0, "thick": -1,  # Hair type
    "low": 0, "medium": 0, "high": 1,  # Energy levels
    "more active in the evening": -1, "no specific pattern": 0, "more active in the morning": 1,  # Activity times
    "trouble falling asleep/staying asleep": 1, "normal sleep": 0, "sound sleeper": -1,  # Sleep patterns
    "variable": 0, "moderate": 0, "strong": 1,  # Appetite
    "craving warm, spicy foods": 1, "no specific cravings": 0, "craving sweet, cold foods": -1  # Food cravings
}

# Define scores for Kapha attributes
kapha_scores = {
    "slim": -1, "medium": 0, "heavy": 1,  # Body build
    "fair": -1, "medium": 0, "dark": 1,  # Skin complexion
    "thin": -1, "medium": 0, "thick": 1,  # Hair type
    "low": -1, "medium": 0, "high": 1,  # Energy levels
    "more active in the evening": -1, "no specific pattern": 0, "more active in the morning": 1,  # Activity times
    "trouble falling asleep/staying asleep": 1, "normal sleep": 0, "sound sleeper": -1,  # Sleep patterns
    "variable": -1, "moderate": 0, "strong": 1,  # Appetite
    "craving warm, spicy foods": 1, "no specific cravings": 0, "craving sweet, cold foods": -1  # Food cravings
}

# Create an instance of DoshaCalculator
calculator = DoshaCalculator()

# Set user responses
calculator.user_build = "slim"
calculator.user_skin_complexion = "fair"
calculator.user_hair_type = "thin"
calculator.user_energy_levels = "low"
calculator.user_activity_times = "more active in the evening"
calculator.user_sleep_hours = "normal sleep"
calculator.user_sleep_trouble = "trouble falling asleep/staying asleep"
calculator.user_appetite = "strong"
calculator.user_food_cravings = "craving warm, spicy foods"

# Calculate dosha scores based on user responses
dosha_scores = calculator.calculate_dosha_scores()

# Determine the predominant dosha
predominant_dosha = max(dosha_scores, key=dosha_scores.get)

# Print the result
print(f"Predominant Dosha: {predominant_dosha}")




if __name__ == "__main__":
    root = tk.Tk()
    obj = Chatbot(root)
    root.mainloop()
