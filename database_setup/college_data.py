import sys
sys.path.append("../marks-management-system")

from database_setup.college import AdminDB, SubjectDB, GradeDB

admin = AdminDB()
subject = SubjectDB()
grade = GradeDB()

admin.add_admin("admin1", "1234")
admin.add_admin("admin2", "1234")


subjects = ["OOS", "SE", "GGM", "Math", "CN", "GT"]
for sub in subjects:
    subject.add_subject(sub)


grades = {'S': (90, 100), 'A': (80, 89), 'B': (70, 79), 'C': (60, 69), 'D': (50, 59), 'E': (40, 49), 'F' : (0, 39)}
for g, (lower_bound, upper_bound) in grades.items():
    grade.add_grade(g, lower_bound, upper_bound)


grade.close_connection()
admin.close_connection()
subject.close_connection()
