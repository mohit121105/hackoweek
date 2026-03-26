import tkinter as tk
from tkinter import scrolledtext
import spacy
import re
from datetime import datetime, timedelta
import dateparser

# ML + NLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# LOAD MODELS
# -----------------------------
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# INTENT MODEL
# -----------------------------
training_sentences = [
    "hello", "hi", "hey",
    "bye", "goodbye",
    "help me", "i need help",
    "thanks", "thank you",
    "what is my name", "what is my age"
]

labels = [
    "greeting", "greeting", "greeting",
    "goodbye", "goodbye",
    "help", "help",
    "thanks", "thanks",
    "ask_name", "ask_age"
]

vectorizer_intent = TfidfVectorizer()
X = vectorizer_intent.fit_transform(training_sentences)

model = MultinomialNB()
model.fit(X, labels)

# -----------------------------
# FAQ DATA (from your files)
# -----------------------------
faqs = [
    ("fees", "The annual fee is ₹1,20,000."),
    ("courses", "We offer CSE, ECE, ME, AI & DS."),
    ("hostel", "Hostel facilities are available."),
    ("placement", "Average package is ₹6 LPA."),
    ("timing", "9 AM to 4 PM."),
]

questions = [q for q, a in faqs]
answers = [a for q, a in faqs]

vectorizer_faq = TfidfVectorizer()
faq_matrix = vectorizer_faq.fit_transform(questions)

# -----------------------------
# CONTEXT MEMORY
# -----------------------------
context = {
    "name": None,
    "age": None,
    "gender": None,
    "last_date": None
}

# -----------------------------
# ENTITY EXTRACTION
# -----------------------------
def extract_name(text):
    match = re.search(r"(my name is|i am)\s+([A-Za-z]+)", text.lower())
    return match.group(2).capitalize() if match else None

def extract_age(text):
    match = re.search(r"(\d{1,3})\s*(years old|yrs)", text.lower())
    return match.group(1) if match else None

def extract_gender(text):
    if "male" in text.lower():
        return "Male"
    if "female" in text.lower():
        return "Female"
    return None

def extract_date(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed = dateparser.parse(ent.text)
            if parsed:
                return parsed
    return None

# -----------------------------
# DATE CALCULATION
# -----------------------------
def calculate_date(user_input):
    base = context["last_date"] or datetime.now()

    if "tomorrow" in user_input.lower():
        return base + timedelta(days=1)

    if "next week" in user_input.lower():
        return base + timedelta(weeks=1)

    match = re.search(r"after (\d+) days", user_input.lower())
    if match:
        return base + timedelta(days=int(match.group(1)))

    return None

# -----------------------------
# INTENT
# -----------------------------
def predict_intent(text):
    vec = vectorizer_intent.transform([text])
    return model.predict(vec)[0]

# -----------------------------
# FAQ MATCHING
# -----------------------------
def get_faq_response(text):
    vec = vectorizer_faq.transform([text])
    sim = cosine_similarity(vec, faq_matrix)
    idx = sim.argmax()
    score = sim[0][idx]

    if score > 0.3:
        return answers[idx]
    return None

# -----------------------------
# MAIN LOGIC
# -----------------------------
def get_response(user_input):
    global context

    # 1. Profile extraction
    name = extract_name(user_input)
    if name:
        context["name"] = name
        return f"Hello {name}!"

    age = extract_age(user_input)
    if age:
        context["age"] = age
        return f"Age saved: {age}"

    gender = extract_gender(user_input)
    if gender:
        context["gender"] = gender
        return f"Gender: {gender}"

    # 2. Date extraction
    d = extract_date(user_input)
    if d:
        context["last_date"] = d
        return f"Date stored: {d.strftime('%Y-%m-%d')}"

    # 3. Date calculation
    next_d = calculate_date(user_input)
    if next_d:
        context["last_date"] = next_d
        return f"Next date: {next_d.strftime('%Y-%m-%d')}"

    # 4. FAQ
    faq = get_faq_response(user_input)
    if faq:
        return faq

    # 5. Intent
    intent = predict_intent(user_input)

    if intent == "ask_name":
        return f"Your name is {context['name']}" if context["name"] else "I don't know your name."

    if intent == "ask_age":
        return f"Your age is {context['age']}" if context["age"] else "I don't know your age."

    if intent == "greeting":
        return f"Hello {context['name'] or ''}!"

    if intent == "goodbye":
        return "Goodbye!"

    if intent == "help":
        return "I can answer FAQs, remember your info, and calculate dates."

    if intent == "thanks":
        return "You're welcome!"

    # 6. Fallback (from your fallback system :contentReference[oaicite:1]{index=1})
    return "I'm not sure. Please contact admin@college.edu"

# -----------------------------
# GUI
# -----------------------------
def send_message():
    user_msg = entry.get()
    if not user_msg.strip():
        return

    chat.insert(tk.END, "You: " + user_msg + "\n")

    reply = get_response(user_msg)
    chat.insert(tk.END, "Bot: " + reply + "\n\n")

    entry.delete(0, tk.END)

# -----------------------------
# GUI SETUP
# -----------------------------
window = tk.Tk()
window.title("FINAL AI CHATBOT")
window.geometry("520x550")

chat = scrolledtext.ScrolledText(window)
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(window)
entry.pack(fill=tk.X, padx=10, pady=5)

btn = tk.Button(window, text="Send", command=send_message)
btn.pack(pady=5)

window.mainloop()