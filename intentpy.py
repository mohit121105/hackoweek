import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# -----------------------------
# Training Data (Intents)
# -----------------------------
training_sentences = [
    "hello", "hi", "hey",
    "bye", "goodbye", "see you",
    "how are you",
    "what is your name",
    "help me", "i need help",
    "thanks", "thank you"
]

labels = [
    "greeting", "greeting", "greeting",
    "goodbye", "goodbye", "goodbye",
    "status",
    "name",
    "help", "help",
    "thanks", "thanks"
]

# -----------------------------
# Train Model
# -----------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

model = MultinomialNB()
model.fit(X, labels)

# -----------------------------
# Response Dictionary
# -----------------------------
responses = {
    "greeting": "Hello! How can I assist you?",
    "goodbye": "Goodbye! Have a nice day!",
    "status": "I'm just a bot, but I'm doing great!",
    "name": "I am your AI chatbot.",
    "help": "Sure! Tell me what you need help with.",
    "thanks": "You're welcome!"
}

# -----------------------------
# Predict Intent Function
# -----------------------------
def get_response(user_input):
    user_vec = vectorizer.transform([user_input])
    intent = model.predict(user_vec)[0]
    return responses.get(intent, "Sorry, I didn't understand.")

# -----------------------------
# GUI Function
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
window.title("Intent Classification Chatbot")
window.geometry("500x500")

chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(window)
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(pady=5)

window.mainloop()