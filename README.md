# Departmental Result Management System

A Flask application designed to track and manage student results within a university department. The system categorizes results into different segments such as CATs, labs, practicals, and exams, providing a comprehensive overview and detailed management capabilities for lecturers, students, and administrators.

## Features

- **Lecturer Interface**: Update and manage marks for different categories including CATs, labs, practicals, and exams.
- **Discrepancy Highlighting**: Automatic identification and highlighting of discrepancies within the system.
- **Administrative Dashboard**: Tabulated information for admins and heads of departments to view summaries, pass marks, number of passes, fails, etc.
- **Student Portal**: Students can log in to view their individual transcripts and identify any issues or areas that require attention.
- **User Roles and Authorization**: Clear separation and specific functionalities for different user roles (Lecturer, Student, Admin).

## Tech Stack

- **Flask**: Web framework used for developing the application.
- **Python**: Programming language used for the backend logic.
- **SQLite**: Database used for storing application data.
- **Jinja Templating**: Templating engine for rendering HTML templates.
- **TailwindCSS**: CSS framework for styling the application.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/paulwritescode/Departmental-Result-Management-System.git
   cd Departmental-Result-Management-System
