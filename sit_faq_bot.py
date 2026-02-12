import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import nltk
from nltk.corpus import wordnet
import string
import os

# ---------------------------
# FAQ DATA - SIT NAGPUR
# ---------------------------

faq_data = {
    "about_sit":
        "Symbiosis Institute of Technology Nagpur is a private engineering institute under Symbiosis International (Deemed University).",

    "location":
        "SIT Nagpur is located in Nagpur, Maharashtra, India.",

    "courses":
        "SIT Nagpur offers B.Tech programs in Computer Science, Artificial Intelligence, Robotics, Mechanical Engineering and related fields.",

    "admission":
        "Admission to SIT Nagpur is through the SITEEE entrance examination conducted by Symbiosis International University.",

    "hostel":
        "Yes, SIT Nagpur provides separate hostel facilities for boys and girls within the campus.",

    "fees":
        "The fee structure varies by program. Please visit the official SIT Nagpur website for updated fee details.",

    "facilities":
        "The campus includes modern labs, library, sports complex, cafeteria, innovation labs, and smart classrooms."
}

# ---------------------------
# INTENT KEYWORDS
# ---------------------------

intent_keywords = {
    "about_sit": ["about", "symbiosis", "technology"],
    "location": ["where", "location", "situated", "city", "address"],
    "courses": ["course", "courses", "program", "branch", "stream"],
    "admission": ["admission", "apply", "entrance", "selection"],
    "hostel": ["hostel", "accommodation", "residence", "stay", "dormitory"],
    "fees": ["fee", "fees", "cost", "charges", "tuition"],
    "facilities": ["facility", "facilities", "lab", "library", "campus"]
}

# ---------------------------
# TEXT PROCESSING
# ---------------------------

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " "))
    return synonyms

def detect_intent(user_input):
    words = preprocess(user_input)

    expanded_words = set(words)

    # Expand with WordNet synonyms
    for word in words:
        expanded_words.update(get_synonyms(word))

    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in expanded_words:
                return intent

    return None

# ---------------------------
# GUI FUNCTION
# ---------------------------

def send_message(event=None):
    user_input = entry.get()

    if user_input.strip() == "":
        return

    chat_area.insert(tk.END, "You: " + user_input + "\n\n")

    intent = detect_intent(user_input)

    if intent and intent in faq_data:
        response = faq_data[intent]
    else:
        response = "Sorry, I couldn't understand your question about SIT Nagpur."

    chat_area.insert(tk.END, "Bot: " + response + "\n\n")
    chat_area.see(tk.END)

    entry.delete(0, tk.END)

# ---------------------------
# GUI SETUP
# ---------------------------

root = tk.Tk()
root.title("SIT Nagpur FAQ Bot")
root.geometry("700x650")
root.configure(bg="white")

# -------- LOGO --------

try:
    current_path = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_path, "logo.png")

    img = Image.open(logo_path)

    width = 240
    ratio = width / img.width
    height = int(img.height * ratio)

    img = img.resize((width, height), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=logo, bg="white")
    logo_label.pack(pady=5)

except:
    print("Logo not found. Make sure 'logo.png' is in same folder.")

# -------- TITLE --------

title_label = tk.Label(
    root,
    text="Symbiosis Institute of Technology\nNagpur FAQ Bot",
    font=("Arial", 16, "bold"),
    fg="#C8102E",
    bg="white"
)
title_label.pack(pady=10)

# -------- CHAT AREA --------

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=80,
    height=20,
    bg="white",
    fg="black",
    font=("Arial", 11)
)
chat_area.pack(pady=10)

# -------- ENTRY --------

entry = tk.Entry(
    root,
    width=60,
    font=("Arial", 12),
    bg="#F5F5F5"
)
entry.pack(pady=10)

entry.bind("<Return>", send_message)

# -------- BUTTON --------

send_button = tk.Button(
    root,
    text="Send",
    command=send_message,
    bg="#C8102E",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12
)
send_button.pack(pady=5)

root.mainloop()