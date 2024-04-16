import sys
sys.path.append("../marks-management-system")

from database_setup.student import StudentDB, MarkDB, ResultDB
import random

student_db = StudentDB()
marks = MarkDB()
result = ResultDB()

student_details = [
    ("s1@e.com", "1234", "John", "Doe", "1234567890"),
    ("s2@e.com", "1234", "Jane", "Smith", "9876543210"),
    ("s3@e.com", "1234", "Alice", "Johnson", "5551234567"),
    ("s4@e.com", "1234", "Bob", "Williams", "9871234567"),
    ("s5@e.com", "1234", "Charlie", "Brown", "1239876543"),
    ("s6@e.com", "1234", "Emma", "Garcia", "9876541230"),
    ("s7@e.com", "1234", "David", "Martinez", "4567890123"),
    ("s8@e.com", "1234", "Michael", "Taylor", "9876543210"),
    ("s9@e.com", "1234", "Sophia", "Anderson", "1234567890"),
    ("s10@e.com", "1234", "Olivia", "Thomas", "5551234567"),
    ("s11@e.com", "1234", "James", "Hernandez", "9871234567"),
    ("s12@e.com", "1234", "William", "Young", "1239876543"),
    ("s13@e.com", "1234", "Daniel", "King", "9876541230"),
    ("s14@e.com", "1234", "Emily", "Wright", "4567890123"),
    ("s15@e.com", "1234", "Sarah", "Lopez", "9876543210"),
    ("s16@e.com", "1234", "Ashley", "Scott", "1234567890"),
    ("s17@e.com", "1234", "Madison", "Green", "5551234567"),
    ("s18@e.com", "1234", "Joseph", "Adams", "9871234567"),
    ("s19@e.com", "1234", "David", "Baker", "1239876543"),
    ("s20@e.com", "1234", "Robert", "Collins", "9876541230")
]

for details in student_details:
    email, password, first_name, last_name, phoneNo = details
    student_db.add_student(email, password, first_name, last_name, phoneNo)


rolls = student_db.get_rolls()

for roll in rolls:
    for subject_id in range(1, 7):
        if marks.get_grade(1, 1) is not None or not marks.get_grade(1, 1):
            break
        mark = random.randint(60, 100)
        marks.update_mark(roll[0], subject_id, mark)

        
student_db.close_connection()
marks.close_connection()
result.close_connection()