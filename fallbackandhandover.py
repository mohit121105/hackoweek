from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

faqs = [
    ("What courses are offered in the college?", "The college offers undergraduate and postgraduate courses in various fields."),
    ("Where is the college located?", "The college is located in a well-connected urban area."),
    ("Is the college affiliated with a university?", "Yes, the college is affiliated with a recognized university."),
    ("What is the ranking of the college?", "The college has a good academic reputation and ranking."),
    ("Is the college government or private?", "The college may be either government or private depending on the institution."),
    ("What are the college timings?", "College timings are usually from 9 AM to 5 PM."),
    ("Does the college have hostel facilities?", "Yes, hostel facilities are available for students."),
    ("What is the campus size?", "The campus is spacious with academic and recreational facilities."),
    ("Is there Wi-Fi available on campus?", "Yes, Wi-Fi is available across the campus."),
    ("Does the college have a library?", "Yes, the college has a well-equipped library."),

    ("What is the admission process?", "Admissions are based on merit or entrance exams depending on the course."),
    ("How can I apply for admission?", "You can apply online through the college website."),
    ("What are the eligibility criteria?", "Eligibility depends on the course requirements and qualifications."),
    ("Is there an entrance exam?", "Some courses require entrance exams."),
    ("What documents are required for admission?", "You need mark sheets, ID proof, photos, and certificates."),
    ("When does the admission start?", "Admissions usually start in May or June."),
    ("What is the last date to apply?", "The last date varies; check the official website."),
    ("Is there a management quota?", "Yes, some colleges offer management quota seats."),
    ("Can I apply online?", "Yes, online applications are available."),
    ("What is the application fee?", "The application fee varies by course."),

    ("What is the fee structure?", "Fees depend on the course and program."),
    ("Are there any scholarships available?", "Yes, scholarships are available for eligible students."),
    ("How can I apply for a scholarship?", "You can apply through the college or government portals."),
    ("Is there a fee concession for reserved categories?", "Yes, concessions are available as per government rules."),
    ("What payment methods are accepted?", "Online payment, cards, and bank transfers are accepted."),
    ("Is the fee refundable?", "Fees are refundable as per college policy."),
    ("Are there installment options?", "Yes, fees can be paid in installments."),
    ("What is the hostel fee?", "Hostel fees vary depending on room type."),
    ("Are there any hidden charges?", "No, all charges are transparent."),
    ("Do you provide financial aid?", "Yes, financial aid is available for needy students."),

    ("What subjects are included in the course?", "Subjects depend on the selected course."),
    ("What is the syllabus?", "The syllabus follows university guidelines."),
    ("How are exams conducted?", "Exams are conducted semester-wise."),
    ("Is there continuous assessment?", "Yes, internal assessments are included."),
    ("Are assignments mandatory?", "Yes, assignments are compulsory."),
    ("What is the attendance requirement?", "Minimum 75% attendance is required."),
    ("Can I change my course later?", "Course changes are allowed under certain conditions."),
    ("Are there practical labs?", "Yes, labs are available for practical subjects."),
    ("How many semesters are there?", "Courses usually have 6 to 8 semesters."),
    ("Are there online classes available?", "Yes, online classes may be provided."),

    ("Are the faculty members experienced?", "Yes, faculty members are qualified and experienced."),
    ("What is the student-teacher ratio?", "The ratio is maintained for effective learning."),
    ("Are guest lectures conducted?", "Yes, guest lectures are regularly conducted."),
    ("Can I contact professors outside class?", "Yes, faculty are approachable outside class."),
    ("Do teachers provide notes?", "Yes, study materials and notes are provided."),

    ("Does the college have a hostel?", "Yes, hostel facilities are available."),
    ("Is there a cafeteria?", "Yes, a cafeteria is available on campus."),
    ("Are sports facilities available?", "Yes, various sports facilities are provided."),
    ("Is there a gym?", "Yes, a gym is available for students."),
    ("Does the college provide transport?", "Yes, transport facilities are available."),
    ("Is there medical support on campus?", "Yes, medical facilities are provided."),
    ("Are there computer labs?", "Yes, modern computer labs are available."),
    ("Is there a reading room?", "Yes, a reading room is available in the library."),
    ("Are classrooms air-conditioned?", "Some classrooms are air-conditioned."),
    ("Is there parking available?", "Yes, parking facilities are available."),

    ("What are the hostel rules?", "Hostel rules must be followed strictly."),
    ("Is hostel compulsory?", "No, hostel is optional."),
    ("Are rooms shared or single?", "Both shared and single rooms are available."),
    ("What are the hostel timings?", "Hostel timings are fixed by administration."),
    ("Is food provided in the hostel?", "Yes, meals are provided."),
    ("What is the quality of hostel food?", "Food quality is good and hygienic."),
    ("Are there separate hostels for boys and girls?", "Yes, separate hostels are provided."),
    ("Is Wi-Fi available in the hostel?", "Yes, Wi-Fi is available in hostels."),
    ("What is the hostel fee?", "Hostel fees depend on accommodation type."),
    ("Are visitors allowed?", "Visitors are allowed during specified hours."),

    ("Does the college provide placements?", "Yes, placement assistance is provided."),
    ("What companies visit the campus?", "Various reputed companies visit the campus."),
    ("What is the highest package offered?", "The highest package varies each year."),
    ("What is the average salary?", "The average salary depends on the course."),
    ("Are internships provided?", "Yes, internship opportunities are available."),
    ("Is placement training available?", "Yes, training sessions are conducted."),
    ("What is the placement percentage?", "Placement rates are generally high."),
    ("Are there industry collaborations?", "Yes, the college has industry tie-ups."),
    ("Does the college have a placement cell?", "Yes, there is a dedicated placement cell."),
    ("Are there resume-building workshops?", "Yes, workshops are conducted regularly."),

    ("Are there student clubs?", "Yes, various student clubs are available."),
    ("What cultural activities are conducted?", "Cultural events and fests are organized."),
    ("Are there technical fests?", "Yes, technical fests are conducted."),
    ("Is participation mandatory?", "Participation is optional but encouraged."),
    ("Are there sports competitions?", "Yes, sports competitions are held."),
    ("Can I start my own club?", "Yes, with approval from administration."),
    ("Are there music or dance clubs?", "Yes, creative clubs are available."),
    ("Is there a student council?", "Yes, there is a student council."),
    ("Are events held annually?", "Yes, major events are held annually."),
    ("Are certificates provided for participation?", "Yes, certificates are awarded."),

    ("When are exams conducted?", "Exams are held at the end of each semester."),
    ("How can I check my results?", "Results can be checked online on the portal."),
    ("What is the passing criteria?", "Minimum passing marks are required."),
    ("Are re-exams allowed?", "Yes, re-exams are allowed."),
    ("What happens if I fail a subject?", "You can reappear for the exam."),
    ("Can I apply for revaluation?", "Yes, revaluation is allowed."),
    ("When are results declared?", "Results are declared after evaluation."),
    ("Is there grading or percentage system?", "Both grading and percentage systems may be used."),
    ("How many attempts are allowed?", "Multiple attempts are allowed."),
    ("Are internal marks included?", "Yes, internal marks are included."),

    ("How can I get my degree certificate?", "Degree certificates are issued after course completion."),
    ("How to apply for transcripts?", "Apply through the administration office."),
    ("When will I receive my marksheet?", "Marksheet is provided after results."),
    ("Can I get duplicate certificates?", "Yes, duplicates can be issued on request."),
    ("How to apply for migration certificate?", "Apply through the university office."),

    ("Does the college provide bus service?", "Yes, bus services are available."),
    ("What are the transport charges?", "Charges depend on distance."),
    ("What routes are available?", "Multiple routes cover nearby areas."),
    ("Is transport compulsory?", "No, transport is optional."),
    ("Are buses safe?", "Yes, safety measures are in place."),

    ("Is there a student portal?", "Yes, a student portal is available."),
    ("How to login to the portal?", "Use your student ID and password."),
    ("Can I pay fees online?", "Yes, online payment is available."),
    ("Are classes available online?", "Yes, online classes may be provided."),
    ("How to reset my password?", "Use the forgot password option."),

    ("Is ragging allowed?", "No, ragging is strictly prohibited."),
    ("What are the anti-ragging rules?", "Strict anti-ragging policies are enforced."),
    ("Is there a dress code?", "Yes, a dress code may be applicable."),
    ("Can I take leave?", "Yes, leave can be taken with permission."),
    ("What are the college rules?", "Students must follow college rules and discipline."),
    ("Is attendance compulsory?", "Yes, attendance is mandatory."),
    ("Are part-time jobs allowed?", "Yes, but academics should not be affected."),
    ("Can I bring a laptop?", "Yes, laptops are allowed."),
    ("Is there a grievance cell?", "Yes, a grievance cell is available."),
    ("How can I contact administration?", "You can contact via email or office visit.")
]


def preprocess(text):
    return text.lower()

questions = [preprocess(q) for q, a in faqs]
answers = [a for q, a in faqs]

vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf_matrix = vectorizer.fit_transform(questions)

def get_response(user_query):
    processed_query = preprocess(user_query)
    query_vec = vectorizer.transform([processed_query])

    similarity = cosine_similarity(query_vec, tfidf_matrix)
    best_match_index = similarity.argmax()
    score = similarity[0][best_match_index]

    if score < 0.15:
        return ("I'm not sure about that.\n"
                "Please contact:\n"
                "Email: admin@college.edu\n"
                "Help Desk: College Office")

    elif score < 0.30:
        top_indices = similarity[0].argsort()[-3:][::-1]
        suggestions = "\n".join([f"- {faqs[i][0]}" for i in top_indices])

        return f"I didn't fully understand your question.\nDid you mean:\n{suggestions}"

    else:
        return answers[best_match_index]

print("Chatbot ready! Type 'exit' to quit")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    print("Bot:", get_response(user_input))