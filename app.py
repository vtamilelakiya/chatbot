import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "rvce_complete_final_system_2026"

# --- DATABASE CONFIG ---
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'admissions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AdmissionEnquiry(db.Model):
    __tablename__ = 'admission_enquiry'
    id = db.Column(db.Integer, primary_key=True)
    your_name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        u_mobile = request.form.get('u_mobile')
        if u_name and u_mobile:
            try:
                new_enquiry = AdmissionEnquiry(your_name=u_name, mobile=u_mobile)
                db.session.add(new_enquiry)
                db.session.commit()
                session['user_name'] = u_name
                return redirect(url_for('chat'))
            except Exception as e:
                db.session.rollback()
                return f"Error: {e}"
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user_name' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', name=session['user_name'])

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    msg = data.get('message', '').lower().strip()
    
    contact_res = "<b>Contact details:</b><br>📞 04562-234500, 88258 15087"
    
    # 1. ABOUT COLLEGE / RVCE
    if "about college" in msg or "about rvce" in msg:
        res = ("RVCE was established in 2011, and our institution has steadily progressed as a center of academic distinction and professional excellence. We offer five undergraduate programs - Artificial Intelligence & Data Science (AI&DS), Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), Electrical and Electronics Engineering (EEE), and Mechanical Engineering (MECH). The college has consistently maintained high academic standards and is proud to be ranked among the top 25 institutions affiliated with Anna University (Out of 251 Engineering Colleges in Tamil Nadu (Including Government Colleges)), with more than 40 of our students having secured University Ranks to date.<br><br>"
               "Beyond academics, we place strong emphasis on high-quality research, publications in reputed high-impact journals, patented innovations, authored books, and meaningful industry collaboration, while fostering holistic student development through technical forums, professional bodies, value-added programs, and entrepreneurial initiatives.")

    # 2. FACILITIES (Moved here to ensure it triggers correctly)
    elif "facilit" in msg:
        res = ("<b>Our Facilities:</b><br>"
               "1. Highly qualified and experienced faculty members<br>2. Training and Placement Cell<br>3. Career guidance and higher education support<br>4. Entrepreneurship and innovation cell<br>5. Central library with books, journals, e-resources<br>6. Research and innovation support facilities<br>7. High-speed Wi-Fi enabled campus (24x7)<br>8. Cultural clubs and outdoor sports facilities<br>9. Advanced computer labs<br>10. Separate hostels for boys and girls<br>11. Hygienic and spacious dining facilities<br>12. College bus facility covering major routes<br>13. 24x7 security and CCTV surveillance<br>14. RO drinking water facilities across campus<br>15. Eco-friendly practices and green initiatives")

    # 3. LAB DETAILS
    elif "lab" in msg:
        res = ("<b>DEPARTMENT LAB DETAILS:</b><br><br>"
               "<b>AI&DS:</b><br>1.Data Exploration, 2.Machine Learning<br><br>"
               "<b>CSE:</b><br>1.DBMS Lab, 2.Networking Lab, 3.Data structure Lab, 4.Advanced Computing Lab, 5.Python Lab(common lab), 6.Language Lab(English lab)<br><br>"
               "<b>ECE:</b><br>1.Electronics Machine Lab, 2.DSP Lab, 3.Power Electronic Lab, 4.Simulation Lab<br><br>"
               "<b>EEE:</b><br>1.Power Electronic Lab, 2.Electrical Machines lab, 3.Power System Simulation Lab, 4.Linear Integrated Lab<br><br>"
               "<b>MECH:</b><br>1.Strength of Materials, 2.Manufacturing Lab, 3.Thermal Lab, 4.Dynamic Lab, 5.Metrology Measurement Lab, 6.CAD/CAM Lab, 7.Engineering Practice lab")

    # 4. FOOD MENU
    elif "food" in msg or "menu" in msg:
        res = ("<b>Food Menu:</b><br>You can view our college food menu here: "
               "<a href='https://drive.google.com/file/d/1qGLi6f4hhITU39vPS3x4AbDfXf0NVrVG/view?usp=drivesdk' target='_blank'>Click to View Menu</a>")

    # 5. CERTIFIED / SPORTS
    elif "certified" in msg or "institution" in msg:
        res = "Approved by AICTE, New Delhi | Affiliated to Anna University, Chennai<br>An ISO 21001:2018 Certified Institution"
    elif "sports" in msg:
        res = "<b>Sports facilities:</b><br>Indoor and outdoor sports facilities for holistic development."

    # 6. ACADEMIC UNITS
    elif "unit" in msg or "academic" in msg or "club" in msg:
        res = ("<b>Academic units:</b><br>"
               "1. INSTITUTION INNOVATION (IIC)<br>2. INSTITUTION INDUSTRY INTERACTION CELL (IIIC)<br>3. ENTREPRENEURSHIP DEVELOPMENT CELL (EDC)<br>4. SWAYAM - NPTEL<br>5. ALUMNI ASSOCIATION<br>6. WOMEN EMPOWERMENT CELL<br>7. ECO NATURAL CLUB<br>8. NATIONAL SERVICE SCHEME (NSS)<br>9. UNNAT BHARAT ABHIYAN (UBA)<br>10. FINE ART AND LITERATURE CLUB<br>11. ROTARACT CLUB<br>12. NAAN MUDHALVAN(TNSDC)")

    # 7. BUS, HOSTEL, CONTACT, LINK
    elif "hostel" in msg:
        res = "<b>Hostel details:</b> Separate hostels for boys (capacity-250) and girls (capacity-150) with shared rooms and hygienic dining."
    elif "bus" in msg or "transport" in msg:
        res = "<b>Bus facility:</b> College bus facility covering major routes for students convenience."
    elif "contact" in msg or "phone" in msg:
        res = contact_res
    elif "link" in msg or "admission" in msg:
        res = "<b>Admission link:</b> ✉ admissions@rvce.ac.in"

    # 8. SPECIFIC COURSES
    elif "cse" in msg or "computer science" in msg:
        res = ("<b>B.E Computer Science and Engineering:</b><br>"
               "One of the most popular branches with strong industry demand. Available seats-120.<br>"
               "<b>Cut-off:</b> OS:147, BC:85.5, BCM:82, SC:120.5, SCA:118.5, ST:119")
    elif "ai&ds" in msg or "artificial intelligence" in msg:
        res = ("<b>B.TECH Artificial Intelligence and Data Science:</b><br>"
               "A cutting-edge program focused on AI and data science skills. Available seats-60.<br>"
               "<b>Cut-off:</b> OS:148, BC:117, BCM:110, SC:118")
    elif "ece" in msg or "electronics" in msg:
        res = ("<b>B.E Electronics and Communication Engineering:</b><br>"
               "A popular branch with strong industry demand. Available seats-60.<br>"
               "<b>Cut-off:</b> OC:132, BC:102, MBC:113.5, SCA:100.5, SC:90")
    elif "eee" in msg or "electrical" in msg:
        res = ("<b>B.E Electrical and Electronics Engineering:</b><br>"
               "A popular branch with strong industry demand. Available seats-60.<br>"
               "<b>Cut-off:</b> OC:106.5, MBC:100.5")
    elif "mech" in msg or "mechanical" in msg:
        res = ("<b>B.E Mechanical Engineering:</b><br>"
               "A popular branch with strong industry demand. Available seats-60.<br>"
               "<b>Cut-off:</b> OC:116, BC:106.5, MBC:85")
    elif "it" in msg or "information technology" in msg:
        res = ("<b>B.TECH Information Technology:</b><br>"
               "A comprehensive program covering various IT domains. Available seats-60. Maximum Cutoff-190.5")
    elif "csbs" in msg or "business systems" in msg:
        res = ("<b>B.TECH Computer Science and Business Systems:</b><br>"
               "A unique program combining computer science with business systems. Available seats-60. Maximum Cutoff-190.5")

    # 9. GENERAL INFO
    elif "course" in msg or "dept" in msg:
        res = ("<b>B.TECH PROGRAMS:</b><br>"
               "1. Artificial Intelligence and Data Science<br>"
               "2. Information Technology<br>"
               "3. Computer Science and Business Systems<br><br>"
               "<b>B.E. PROGRAMS:</b><br>"
               "1. Computer Science and Engineering<br>"
               "2. Electronics and Communication Engineering<br>"
               "3. Electrical and Electronics Engineering<br>"
               "4. Mechanical Engineering")
    elif "placement" in msg:
        res = ("<b>Placement Excellence</b><br>2023–2024 – 84%<br>2024–2025 – 92%<br>2025–2026 – 100%<br><br>"
               "<b>Placement details</b><br>• 12 Lakhs – Highest Salary<br>• 4 Lakhs – Average Salary<br>• 56+ – Companies Visited<br>• 600+ – Placement Offers")
    elif "location" in msg:
        res = "<b>Location:</b> Salvarpatti, Sivakasi – Sattur Main Road, Virudhunagar District – 626 128"
    elif "counselling code" in msg or "tnea" in msg:
        res = "<b>Counselling code:</b> TNEA CODE: 4676"
    elif "college code" in msg:
        res = "<b>College code:</b> 9525"
    else:
        res = "I don't have that information. Please contact our office:<br>" + contact_res

    return jsonify({"response": res})

if __name__ == '__main__':
    app.run(debug=True)