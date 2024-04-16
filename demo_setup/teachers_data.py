import sys
sys.path.append("../marks-management-system")

from database_setup.teacher import TeacherDB
 
teacher_db = TeacherDB()

teacher_details = [
    ("john@e.com", "1234", "Johnny", "Doe", "1234567890", 1),
    ("jane@e.com", "1234", "Janice", "Smith", "9876543210", 2),
    ("alice@e.com", "1234", "Ally", "Johnson", "5551234567", 3),
    ("bob@e.com", "1234", "Bobby", "Williams", "9871234567", 4),
    ("charlie@e.com", "1234", "Charlotte", "Brown", "1239876543", 5),
    ("emma@e.com", "1234", "Emilia", "Garcia", "9876541230", 6),
    ("david@e.com", "1234", "Daniel", "Martinez", "4567890123", None)
]

for details in teacher_details:
    password, first_name, last_name, email, phoneNo, subject_id = details
    teacher_db.add_teacher(password, first_name, last_name, email, phoneNo, subject_id)

teacher_db.close_connection()
