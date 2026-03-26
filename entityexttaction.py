import tkinter as tk
from tkinter import scrolledtext
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Function to extract dates
# -----------------------------
def extract_dates(text):
    doc = nlp(text)
    dates = []

    for ent in doc.ents:
        if ent.label_ == "DATE":
            dates.append(ent.text)

    return dates

# -----------------------------
# Chatbot response logic
# -----------------------------
def get_response(user_input):
    dates = extract_dates(user_input)

    if dates:
        return "📅 Dates found: " + ", ".join(dates)
    else:
        return "❌ No date found in your input."

# -----------------------------
# GUI function
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
# GUI setup
# -----------------------------
window = tk.Tk()
window.title("Date Entity Extraction Chatbot")
window.geometry("500x500")

chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(window)
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(window, text="Extract Date", command=send_message)
send_button.pack(pady=5)

window.mainloop()