# chatbot_logic.py

import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data (safe)
nltk.download('punkt')
nltk.download('stopwords')

# ---------------- LOAD ONCE (IMPORTANT FIX) ----------------
stop_words = set(stopwords.words('english'))

# ---------------- FAQ DATA ----------------
faq = {
    "timings": "College is open from 9 AM to 5 PM.",
    "fees": "Fees can be paid online via the student portal.",
    "contact": "You can contact the college at 9876543210.",
    "hostel": "Hostel facilities are available for students.",
    "admissions": "Admissions are currently open. Visit the official website.",
    "scholarship": "Scholarships are available based on merit and eligibility.",
    "about": "This is a reputed college offering engineering and management programs."
}

# ---------------- PREPROCESSING ----------------
def preprocess(text):
    text = text.lower()

    text = text.replace("fee", "fees")
    text = text.replace("hostal", "hostel")

    tokens = text.split()

    tokens = [w for w in tokens if w not in stop_words]
    tokens = [w for w in tokens if w not in string.punctuation]

    return tokens

# ---------------- SYNONYMS ----------------
synonyms = {
    "fees": ["fees", "tuition", "payment", "cost"],
    "timings": ["time", "timing", "hours", "schedule"],
    "contact": ["contact", "phone", "call", "email"],
    "hostel": ["hostel", "accommodation", "stay"],
    "admissions": ["admission", "apply", "enroll"],
    "scholarship": ["scholarship", "aid", "financial"],
    "about": ["about", "college", "info", "information"]
}

# ---------------- TF-IDF ----------------
questions = [
    "What are college timings?",
    "How to pay fees?",
    "What is contact number?",
    "Is hostel available?",
    "How to apply for admission?",
    "Are scholarships available?",
    "Tell me about the college"
]

answers = [
    faq["timings"],
    faq["fees"],
    faq["contact"],
    faq["hostel"],
    faq["admissions"],
    faq["scholarship"],
    faq["about"]
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

def tfidf_response(query):
    q_vec = vectorizer.transform([query])
    similarity = cosine_similarity(q_vec, X)

    max_score = similarity.max()
    index = similarity.argmax()

    if max_score < 0.3:
        return None

    return answers[index]

# ---------------- INTENT ----------------
intents = {
    "admissions": ["admission", "apply"],
    "exams": ["exam", "test"],
    "timetable": ["timetable", "schedule"],
    "hostel": ["hostel", "accommodation"],
    "scholarship": ["scholarship", "financial"]
}

def detect_intent(query):
    tokens = preprocess(query)

    for intent, words in intents.items():
        if any(word in tokens for word in words):
            return intent

    return "unknown"

# ---------------- ENTITY ----------------
def extract_entities(query):
    semester = re.findall(r'\b\d+\b', query)
    return {"semester": semester}

# ---------------- CONTEXT ----------------
context = {}

# ---------------- MAIN FUNCTION ----------------
def chatbot_response(query):
    global context

    query_lower = query.lower()

    # Small talk
    if query_lower in ["hi", "hello", "hey"]:
        return "Hello! How can I help you?"

    if "how are you" in query_lower:
        return "I'm working perfectly! 😊"

    # Context
    if context.get("topic") == "exam":
        entities = extract_entities(query)
        if entities["semester"]:
            context.clear()
            return f"Exam schedule for semester {entities['semester'][0]} will be announced soon."
        return "Please specify semester."

    if "exam" in query_lower:
        context["topic"] = "exam"
        return "Which semester?"

    # Synonym match
    tokens = preprocess(query)
    for key, words in synonyms.items():
        if any(word in tokens for word in words):
            return faq[key]

    # Intent
    intent = detect_intent(query)
    if intent == "admissions":
        return faq["admissions"]
    elif intent == "hostel":
        return faq["hostel"]
    elif intent == "scholarship":
        return faq["scholarship"]
    elif intent == "timetable":
        return faq["timings"]

    # TF-IDF
    response = tfidf_response(query)
    if response:
        return response

    # Fallback
    return (
        "I'm not sure about that 🤔\n"
        "Try asking about:\n"
        "Fees, Timings, Hostel, Admissions, Exams"
    )