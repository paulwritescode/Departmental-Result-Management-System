# 🚀 Quick Start Guide

## ✅ System Status

Your Result Management System is **READY TO USE**!

- ✓ Database initialized
- ✓ 3 user roles created (ADMIN, Lecturer, User)
- ✓ 24 course units loaded
- ✓ 3 test user accounts created

---

## 🔐 Login Credentials

### **Admin Account** (Full Access)
```
Email:    admin@rms.com
Username: admin
Password: admin123
```

### **Lecturer Account** (Update Marks)
```
Email:    lecturer@rms.com
Username: lecturer
Password: lecturer123
```

### **Student Account** (View Transcript)
```
Email:    student@rms.com
Username: student
Password: student123
```

---

## ▶️ Start the Application

Run this command:
```bash
flask run
```

Or:
```bash
python3 rms.py
```

Then open your browser to: **http://127.0.0.1:5000**

---

## 📖 What to Do Next

1. **Login as Admin** (`admin@rms.com` / `admin123`)
   - Explore the admin dashboard
   - Try enrolling the student in a module
   - Assign a unit to the lecturer

2. **Login as Lecturer** (`lecturer@rms.com` / `lecturer123`)
   - View assigned units (none yet - admin needs to assign)
   - Once assigned, update student marks

3. **Login as Student** (`student@rms.com` / `student123`)
   - View your dashboard
   - Check your transcript (empty until enrolled)

---

## 📚 Full Documentation

For complete details, see **SETUP_GUIDE.md** which includes:
- Detailed system architecture
- All user roles and permissions
- Database schema
- Common workflows
- Troubleshooting guide
- Security considerations

---

## 🎯 Quick Workflow Example

### Enroll a Student and Add Marks

1. **Login as Admin**
   - Go to "Enroll Student"
   - Select student: `student@rms.com`
   - Select module: Year 1 Semester 1
   - Academic year: 2024
   - Submit

2. **Assign Unit to Lecturer**
   - Go to "Assign Unit"
   - Select lecturer: `lecturer@rms.com`
   - Select unit: "Calculus 1"
   - Academic year: 2024
   - Submit

3. **Login as Lecturer**
   - View "Calculus 1" on dashboard
   - Click to view enrolled students
   - Enter marks (CAT, Assignment, Practical, Exam)
   - System auto-calculates overall mark and grade

4. **Login as Student**
   - View academic years
   - Select 2024
   - View transcript with grades

---

## 🛠️ Need Help?

- **Can't login?** Check credentials above
- **Database issues?** Run `python3 setup_users.py`
- **Missing packages?** Run `pip3 install Flask Flask-Login Flask-SQLAlchemy Flask-Migrate Flask-WTF Flask-Bootstrap bcrypt email-validator python-dotenv`
- **More help?** See SETUP_GUIDE.md

---

**Ready to go! Run `flask run` and start exploring.**
