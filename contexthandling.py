import tkinter as tk
from tkinter import scrolledtext
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# -----------------------------
# Load NLP model
# -----------------------------
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Intent Training Data
# -----------------------------
training_sentences = [
    "hello", "hi", "hey",
    "bye", "goodbye",
    "help me", "i need help",
    "thanks", "thank you",
    "what date", "remember date"
]

labels = [
    "greeting", "greeting", "greeting",
    "goodbye", "goodbye",
    "help", "help",
    "thanks", "thanks",
    "memory", "memory"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

model = MultinomialNB()
model.fit(X, labels)

# -----------------------------
# Responses
# -----------------------------
responses = {
    "greeting": "Hello! How can I help you?",
    "goodbye": "Goodbye!",
    "help": "I can detect dates and remember them.",
    "thanks": "You're welcome!",
}

# -----------------------------
# Context Memory
# -----------------------------
context = {
    "last_dates": []
}

# -----------------------------
# Extract Dates
# -----------------------------
def extract_dates(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "DATE"]

# -----------------------------
# Predict Intent
# -----------------------------
def predict_intent(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# -----------------------------
# Chatbot Logic
# -----------------------------
def get_response(user_input):
    global context

    dates = extract_dates(user_input)
    intent = predict_intent(user_input)

    # 1. If date found → store it
    if dates:
        context["last_dates"] = dates
        return "📅 Noted date: " + ", ".join(dates)

    # 2. Context handling
    if any(word in user_input.lower() for word in ["tomorrow", "next", "that", "it"]):
        if context["last_dates"]:
            return "📌 Referring to previous date: " + ", ".join(context["last_dates"])

    # 3. Memory query
    if intent == "memory":
        if context["last_dates"]:
            return "🧠 I remember: " + ", ".join(context["last_dates"])
        else:
            return "❌ No date stored."

    # 4. General intents
    if intent in responses:
        return responses[intent]

    return "🤖 I can help with dates. Try mentioning one!"

# -----------------------------
# GUI
# -----------------------------
def send_message():
    user_msg = entry.get()
    if user_msg.strip() == "":
        return

    chat_window.insert(tk.END, "You: " + user_msg + "\n")

    bot_reply = get_response(user_msg)
    chat_window.insert(tk.END, "Bot: " + bot_reply + "\n\n")

    entry.delete(0, tk.END)

# -----------------------------
# GUI Setup
# -----------------------------
window = tk.Tk()
window.title("General Context-Aware Chatbot")
window.geometry("500x500")

chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(window)
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(pady=5)

window.mainloop()