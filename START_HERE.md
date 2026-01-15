# 🚀 Quick Start Guide

## ✅ System Status

Your Result Management System is **READY TO USE**!

- ✓ Database initialized
- ✓ 3 user roles created (ADMIN, Lecturer, User)
- ✓ 24 course units loaded
- ✓ 3 test user accounts created

---

## 🔐 Login Credentials

**⚠️ For security reasons, default credentials have been moved to `CREDENTIALS.md`**

This file is excluded from version control. If you need the default test credentials:
- Check `CREDENTIALS.md` in your local directory
- Or run `python3 setup_users.py` to see the credentials printed during user creation

**Default test accounts:**
- Admin account (full access)
- Lecturer account (update marks)
- Student account (view transcript)

See `CREDENTIALS.md` for login details.

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

1. **Login as Admin** (see `CREDENTIALS.md` for login details)
   - Explore the admin dashboard
   - Try enrolling the student in a module
   - Assign a unit to the lecturer

2. **Login as Lecturer** (see `CREDENTIALS.md` for login details)
   - View assigned units (none yet - admin needs to assign)
   - Once assigned, update student marks

3. **Login as Student** (see `CREDENTIALS.md` for login details)
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
   - Select the student account
   - Select module: Year 1 Semester 1
   - Academic year: 2024
   - Submit

2. **Assign Unit to Lecturer**
   - Go to "Assign Unit"
   - Select the lecturer account
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
