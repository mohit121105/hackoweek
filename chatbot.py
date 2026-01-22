import tkinter as tk

def send_message():
    user_input = entry.get().lower()
    chat.insert(tk.END, "You: " + user_input + "\n")

    if "fees" in user_input:
        response = "The annual fee is ₹1,20,000."

    elif "courses" in user_input:
        response = "We offer CSE, ECE, ME, and AI & DS."

    elif "hostel" in user_input:
        response = "Hostel facilities are available."

    elif "admission" in user_input:
        response = "Admissions start in June."

    elif "placement" in user_input:
        response = "Average placement package is ₹6 LPA."

    elif "timing" in user_input:
        response = "College timings are 9 AM to 4 PM."

    elif "location" in user_input:
        response = "The institute is located in Bangalore."

    elif "contact" in user_input:
        response = "Contact us at contact@abcinstitute.edu"

    elif "scholarship" in user_input:
        response = "Merit-based scholarships are available."

    elif "attendance" in user_input:
        response = "Minimum 75% attendance is required."

    else:
        response = "Sorry, I don't understand your question."

    chat.insert(tk.END, "Bot: " + response + "\n\n")
    chat.see(tk.END)
    entry.delete(0, tk.END)

# ---------------- GUI ----------------

window = tk.Tk()
window.title("Institute FAQ Chatbot")
window.geometry("420x500")
window.configure(bg="white")

# Title
title = tk.Label(
    window,
    text="Institute FAQ Chatbot",
    bg="white",
    fg="red",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

# Chat box
chat = tk.Text(
    window,
    height=18,
    width=48,
    bg="white",
    fg="black",
    font=("Arial", 10),
    borderwidth=2,
    relief="solid"
)
chat.pack(padx=10, pady=10)

# Input box
entry = tk.Entry(
    window,
    width=35,
    font=("Arial", 11),
    borderwidth=2,
    relief="solid"
)
entry.pack(pady=5)

# Send button
send_btn = tk.Button(
    window,
    text="SEND",
    bg="red",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    command=send_message
)
send_btn.pack(pady=10)

window.mainloop()
