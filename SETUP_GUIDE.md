# Departmental Result Management System - Setup Guide

## 📋 Project Overview

This is a **Flask-based Result Management System** for managing student academic records in a university department. The system handles:

- Student enrollment and marks management
- Multiple assessment types (CATs, Assignments, Practicals, Exams)
- Role-based access control (Admin, Lecturer, Student)
- Automated grade calculation and recommendations
- Consolidated reports and transcripts

---

## 🏗️ System Architecture

### **Tech Stack**
- **Backend**: Flask 3.0.2, Python 3.13
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0.25
- **Authentication**: Flask-Login with bcrypt password hashing
- **Frontend**: Jinja2 templates, TailwindCSS, Bootstrap
- **Migrations**: Flask-Migrate (Alembic)

### **Key Features**
1. **Lecturer Interface**: Update marks for assigned units (CAT, Assignment, Practical, Exam)
2. **Student Portal**: View transcripts, grades, and academic progress
3. **Admin Dashboard**: Enroll students, assign units, generate reports
4. **Automated Grading**: Calculate overall marks and assign grades (A-E)
5. **Status Tracking**: Pass/Fail/Supplementary/Repeat recommendations
6. **Consolidated Reports**: Pass lists, supplementary lists, discontinuation lists

---

## 🎯 User Roles & Permissions

### **1. ADMIN (Role ID: 3)**
**Permissions**: VIEW, COMMENT, WRITE, EDIT, ADMIN (Full Access)

**Capabilities**:
- Enroll students in modules
- Assign units to lecturers
- Edit marks for any student
- Generate consolidated reports
- Add new units to the system
- Create new user accounts
- View pass/fail statistics

**Routes**:
- `/admin/dashboard` - Admin dashboard
- `/enroll_student` - Enroll students
- `/assign_unit` - Assign units to lecturers
- `/admin/editmarks` - Edit student marks
- `/consolidated_stylesheet/<acyear>/<yos>/<type>` - Generate reports

### **2. Lecturer (Role ID: 2)**
**Permissions**: VIEW, COMMENT, WRITE

**Capabilities**:
- View assigned units
- Update marks for enrolled students
- View student lists for assigned units
- Calculate overall marks automatically

**Routes**:
- `/lecturerdashboard` - View assigned units
- `/update_marks` - Update student marks

### **3. User/Student (Role ID: 1)**
**Permissions**: VIEW, COMMENT

**Capabilities**:
- View personal transcript
- View marks by academic year and module
- View grades and recommendations
- Update profile information

**Routes**:
- `/student/dashboard` - Student dashboard
- `/studentYears` - View enrolled academic years
- `/results/<student_id>/<academic_year>` - View transcript
- `/getmarks/<student_id>/<academic_year>/<module_id>` - Detailed marks
- `/profile` - View/edit profile

---

## 🗄️ Database Models

### **Core Tables**:

1. **users** - User accounts (students, lecturers, admins)
2. **roles** - User roles with permissions
3. **modules** - Academic modules (Year 1 Sem 1, Year 2 Sem 2, etc.)
4. **units** - Course units (24 predefined units)
5. **student_enrollment** - Student enrollment in modules
6. **enrollment_units** - Junction table for student-unit enrollment
7. **marks** - Student marks (CAT, Assignment, Practical, Exam)
8. **lecturer_assignment** - Unit assignments to lecturers
9. **status** - Status recommendations lookup

### **Predefined Units** (24 total):
- **Year 1 Sem 1**: Calculus 1, Electricity & Magnetism, Computing Math
- **Year 1 Sem 2**: Calculus 2, Probability & Statistics 1, Intro to CS
- **Year 2 Sem 1**: Probability & Statistics 2, Database Systems, System Design
- **Year 2 Sem 2**: Intro to Programming, Programming Concepts, Vectors
- **Year 3 Sem 1**: Theory of Computing, Computer Graphics, Operating Systems
- **Year 3 Sem 2**: Compiler Construction, Multimedia Systems, Networking
- **Year 4 Sem 1**: Computer Security, Machine Learning, HCI
- **Year 4 Sem 2**: Embedded Systems, Entrepreneurship, Professional Ethics

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.13+
- pip (Python package manager)
- SQLite (included with Python)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/paulwritescode/Departmental-Result-Management-System.git
cd Departmental-Result-Management-System
```

### **Step 2: Install Dependencies**
```bash
pip3 install Flask Flask-Login Flask-SQLAlchemy Flask-Migrate Flask-WTF Flask-Bootstrap bcrypt email-validator python-dotenv
```

Or install from requirements.txt (note: some packages may have compatibility issues with Python 3.13):
```bash
pip3 install -r requirements.txt
```

### **Step 3: Configure Environment**
The `.env` file has been created with default settings. You can modify it if needed:

```bash
# Flask Configuration
FLASK_APP=rms.py
FLASK_ENV=development
SECRET_KEY=mysecret_key

# Admin Email (optional)
FLASKY_ADMIN=admin@example.com
```

### **Step 4: Initialize Database**
The database has already been initialized with:
- 3 user roles (ADMIN, Lecturer, User)
- 24 course units
- 3 test user accounts

To reinitialize from scratch:
```bash
rm results.db
python3 -c "from app import create_app, db; from app.models import Role, Units; app = create_app('default'); app.app_context().push(); db.create_all(); Role.insert_roles(); Units.insert_units(); print('✓ Database initialized!')"
python3 setup_users.py
```

---

## 🔐 Default User Credentials

### **Admin Account**
- **Email**: `admin@rms.com`
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: ADMIN
- **Access**: Full system access

### **Lecturer Account**
- **Email**: `lecturer@rms.com`
- **Username**: `lecturer`
- **Password**: `lecturer123`
- **Role**: Lecturer
- **Access**: View assigned units, update marks

### **Student Account**
- **Email**: `student@rms.com`
- **Username**: `student`
- **Password**: `student123`
- **Role**: User (Student)
- **Reg No**: CS001/2023
- **Access**: View personal transcript and marks

---

## ▶️ Running the Application

### **Development Server**
```bash
export FLASK_APP=rms.py
flask run
```

Or simply:
```bash
python3 rms.py
```

The application will be available at: **http://127.0.0.1:5000**

### **Production Deployment**
For production, use Gunicorn:
```bash
gunicorn -c gunicorn.config.py rms:app
```

Configure Nginx as reverse proxy (see `nginx.txt` for configuration).

---

## 📊 Grading System

### **Mark Calculation**
- **Overall Mark** = 0.2×CAT + 0.1×Assignment + 0.1×Practical + 0.6×Exam

### **Grade Scale**
- **A**: > 70 (Excellent)
- **B**: 60-70 (Good)
- **C**: 50-60 (Satisfactory)
- **D**: 40-50 (Pass)
- **E**: < 40 (Fail)

### **Status Codes**
- **-1**: Incomplete (missing marks)
- **1**: Pass (overall > 39)
- **2+**: Supplementary/Repeat (overall < 40)

### **Recommendations**
- **Excellent**: Score > 70
- **Good**: Score 60-70
- **Satisfactory**: Score 50-60
- **Pass**: Score 40-50
- **Fail**: Score < 40
- **Pending**: Incomplete marks

---

## 🔄 Common Workflows

### **Admin: Enroll a Student**
1. Login as admin
2. Navigate to `/enroll_student`
3. Select student, module, and academic year
4. System automatically enrolls student in all units for that module
5. Mark records are created automatically

### **Admin: Assign Unit to Lecturer**
1. Login as admin
2. Navigate to `/assign_unit`
3. Select lecturer, unit, and academic year
4. Lecturer can now view and update marks for that unit

### **Lecturer: Update Marks**
1. Login as lecturer
2. View assigned units on dashboard
3. Select unit and academic year
4. Enter marks for CAT, Assignment, Practical, Exam
5. System auto-calculates overall marks and status

### **Student: View Transcript**
1. Login as student
2. Select academic year
3. Select module/semester
4. View detailed marks and grades
5. View overall recommendation

### **Admin: Generate Reports**
1. Login as admin
2. Navigate to consolidated stylesheet
3. Select academic year and year of study
4. Choose report type:
   - `consosheet`: All students with marks
   - `passlist`: Students who passed
   - `supplementary`: Students needing supplementary exams
   - `repeatyear`: Students repeating year
   - `discontinuation`: Students discontinuing

---

## 🛠️ Database Management

### **View Database Tables**
```bash
sqlite3 results.db ".tables"
```

### **View Users**
```bash
sqlite3 results.db "SELECT u.id, u.username, u.email, r.name as role FROM users u JOIN roles r ON u.role_id = r.id;"
```

### **View Units**
```bash
sqlite3 results.db "SELECT id, name, code FROM units;"
```

### **Add More Users**
```bash
python3 setup_users.py
```

### **Reset Database**
```bash
rm results.db
flask deploy
python3 setup_users.py
```

---

## 📁 Project Structure

```
Departmental-Result-Management-System/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models
│   ├── decorators.py            # Permission decorators
│   ├── admin/                   # Admin blueprint
│   │   ├── views.py
│   │   └── forms.py
│   ├── authentication/          # Auth blueprint
│   │   ├── views.py
│   │   └── forms.py
│   ├── lecturer/                # Lecturer blueprint
│   │   ├── views.py
│   │   └── forms.py
│   ├── main/                    # Main/Student blueprint
│   │   ├── views.py
│   │   └── forms.py
│   ├── static/                  # Static files (images, CSS)
│   └── templates/               # Jinja2 templates
├── migrations/                  # Database migrations
├── config.py                    # Configuration
├── rms.py                       # Application entry point
├── setup_users.py               # User creation script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── results.db                   # SQLite database
```

---

## 🐛 Troubleshooting

### **Issue: ModuleNotFoundError**
```bash
pip3 install Flask Flask-Login Flask-SQLAlchemy Flask-Migrate Flask-WTF Flask-Bootstrap bcrypt email-validator python-dotenv
```

### **Issue: Database not found**
```bash
python3 -c "from app import create_app, db; from app.models import Role, Units; app = create_app('default'); app.app_context().push(); db.create_all(); Role.insert_roles(); Units.insert_units()"
```

### **Issue: Cannot login**
Verify users exist:
```bash
sqlite3 results.db "SELECT username, email FROM users;"
```

If no users, run:
```bash
python3 setup_users.py
```

### **Issue: Permission denied**
Check user role and status:
```bash
sqlite3 results.db "SELECT u.username, r.name, u.status FROM users u JOIN roles r ON u.role_id = r.id;"
```

Status should be `1` (active). Update if needed:
```bash
sqlite3 results.db "UPDATE users SET status=1 WHERE username='admin';"
```

---

## 📝 Notes

- **Academic Year Format**: Stored as integer (e.g., 20222023 for 2022-2023)
- **Module Structure**: Organized by year of study (1-4) and semester (1-2)
- **Mark Validation**: System checks for incomplete marks and highlights discrepancies
- **Auto-Promotion**: Admin can promote passing students to next module
- **Password Security**: All passwords are hashed with bcrypt
- **Session Management**: Flask-Login handles user sessions

---

## 🔒 Security Considerations

1. **Change default passwords** in production
2. **Update SECRET_KEY** in config.py
3. **Use PostgreSQL** for production (not SQLite)
4. **Enable HTTPS** with SSL certificates
5. **Set up proper firewall rules**
6. **Regular database backups**
7. **Implement rate limiting** for login attempts

---

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the code in `app/` directory
- Check Flask documentation: https://flask.palletsprojects.com/

---

## ✅ Quick Start Checklist

- [x] Python 3.13+ installed
- [x] Dependencies installed
- [x] Database initialized
- [x] Test users created
- [ ] Login with admin credentials
- [ ] Explore admin dashboard
- [ ] Test lecturer functionality
- [ ] Test student portal
- [ ] Enroll a student in a module
- [ ] Assign a unit to lecturer
- [ ] Update marks as lecturer
- [ ] View transcript as student

---

**You're all set! Start the application with `flask run` and login with the credentials above.**
