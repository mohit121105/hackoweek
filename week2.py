import tkinter as tk
from tkinter import messagebox
import nltk
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data (run once)
nltk.download('stopwords')
nltk.download('wordnet')

# NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# College info text (from web)
college_info = """
Symbiosis Institute of Technology, Nagpur (SIT Nagpur):
- Established: 2021
- Location: Nagpur, Maharashtra
- Affiliated to Symbiosis International University, Pune
- Offers B.Tech (UG engineering)
- Fee range approx ₹9.2L - ₹12.2L
- Admissions via JEE Main / SITEEE
- Good placement activities with companies visiting campus
Contact: Wathoda, Nagpur - 440008
Admissions Phone: +91-98233 56929 / 90493 37912
"""

def preprocess_text():
    query = input_text.get("1.0", tk.END).strip()
    
    if not query:
        messagebox.showwarning("Warning", "Please enter a query")
        return

    # 1. Lowercase
    query = query.lower()

    # 2. Remove punctuation
    query = query.translate(str.maketrans('', '', string.punctuation))

    # 3. Tokenize
    words = query.split()

    # 4. Remove stopwords & lemmatization
    processed_words = [
        lemmatizer.lemmatize(word) for word in words if word not in stop_words
    ]

    output = " ".join(processed_words)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

def show_info():
    messagebox.showinfo("SIT Nagpur Information", college_info)

# Create window
root = tk.Tk()
root.title("Student Query Preprocessing (Symbiosis Institute of Technology, Nagpur)")
root.geometry("700x550")

# Labels
tk.Label(root, text="Enter Student Query", font=("Arial", 12)).pack(pady=5)

# Input box
input_text = tk.Text(root, height=6, width=70)
input_text.pack(pady=5)

# Buttons
tk.Button(
    root, text="Preprocess Query",
    command=preprocess_text,
    bg="blue", fg="white", font=("Arial", 11)
).pack(pady=10)

tk.Button(
    root, text="Show SIT Nagpur Info",
    command=show_info,
    bg="green", fg="white", font=("Arial", 11)
).pack(pady=4)

# Output label
tk.Label(root, text="Processed Output", font=("Arial", 12)).pack(pady=5)

# Output box
output_text = tk.Text(root, height=6, width=70)
output_text.pack(pady=5)

root.mainloop()
