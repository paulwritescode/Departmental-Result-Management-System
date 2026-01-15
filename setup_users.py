"""
Script to create initial test users for the Result Management System
Run this after running 'flask deploy'
"""
from app import create_app, db
from app.models import User, Role
from werkzeug.security import generate_password_hash

app = create_app('default')

with app.app_context():
    # Check if users already exist
    if User.query.count() > 0:
        print("Users already exist in the database!")
        print("\nExisting users:")
        users = User.query.all()
        for user in users:
            print(f"  - {user.username} ({user.email}) - Role: {user.role.name if user.role else 'None'}")
        response = input("\nDo you want to add more users? (y/n): ")
        if response.lower() != 'y':
            exit()
    
    # Get roles
    admin_role = Role.query.filter_by(name='ADMIN').first()
    lecturer_role = Role.query.filter_by(name='Lecturer').first()
    student_role = Role.query.filter_by(name='User').first()
    
    print("\n=== Creating Test Users ===\n")
    
    # Create Admin User
    admin = User(
        fname='Admin',
        lname='User',
        email='admin@rms.com',
        username='admin',
        password=generate_password_hash('admin123'),
        role_id=admin_role.id,
        status=1
    )
    db.session.add(admin)
    print("✓ Admin user created:")
    print("  Email: admin@rms.com")
    print("  Username: admin")
    print("  Password: admin123")
    
    # Create Lecturer User
    lecturer = User(
        fname='John',
        lname='Doe',
        email='lecturer@rms.com',
        username='lecturer',
        password=generate_password_hash('lecturer123'),
        role_id=lecturer_role.id,
        status=1
    )
    db.session.add(lecturer)
    print("\n✓ Lecturer user created:")
    print("  Email: lecturer@rms.com")
    print("  Username: lecturer")
    print("  Password: lecturer123")
    
    # Create Student User
    student = User(
        fname='Jane',
        lname='Smith',
        email='student@rms.com',
        username='student',
        password=generate_password_hash('student123'),
        role_id=student_role.id,
        Reg_no='CS001/2023',
        Year_of_Registration=2023,
        status=1
    )
    db.session.add(student)
    print("\n✓ Student user created:")
    print("  Email: student@rms.com")
    print("  Username: student")
    print("  Password: student123")
    print("  Reg No: CS001/2023")
    
    # Commit all users
    db.session.commit()
    
    print("\n" + "="*50)
    print("✓ All test users created successfully!")
    print("="*50)
    print("\nYou can now login with any of the above credentials.")
    print("Run the application with: flask run")
