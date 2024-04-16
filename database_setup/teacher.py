import re
import sqlite3

class TeacherDB:    
    def __init__(self, db_path = './database/teachers.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS
            teachers
            (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT,
                phoneNo TEXT,
                subject_id INT
            )
            """)
        self.connection.commit()
    
    def add_teacher(self, email: str, password: str, first_name: str, last_name: str = None, phoneNo: str = None, subject_id: int = None) -> str:
        if (not email) or (not password) or (not first_name):
            return "One or more fields, entered are blanks."
        try:
            self.cursor.execute("INSERT INTO teachers (email, password, first_name, last_name, phoneNo, subject_id) VALUES (?, ?, ?, ?, ?, ?)",
                                (email, password, first_name, last_name, phoneNo, subject_id))
            self.connection.commit()
            return "Teacher added successfully.\nLogin with Email."
        except sqlite3.IntegrityError:
            return "Email already exists.\nPlease provide unique details."

    def update_teacher(self, id: int, new_email: str = None, new_password: str = None, new_first_name: str = None, new_last_name: str = None, new_phoneNo: str = None, subject_id: str = None) -> str:
        try:
            query = "UPDATE teachers SET "
            params = []
            
            if new_email is not None:
                query += "email=?, "
                params.append(new_email)
            
            if new_password is not None:
                query += "password=?, "
                params.append(new_password)
            
            if new_first_name is not None:
                query += "first_name=?, "
                params.append(new_first_name)
            
            if new_last_name is not None:
                query += "last_name=?, "
                params.append(new_last_name)
                
            if new_phoneNo is not None:
                query += "phoneNo=?, "
                params.append(new_phoneNo)
                
            if subject_id is not None:
                query += "subject_id=?, "
                params.append(subject_id)
            
            query = query.rstrip(", ")
            
            query += " WHERE id=?"
            params.append(id)
            
            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            
            return "Updated successfully."
        
        except sqlite3.Error as e:
            print("Error occurred:", e)
            return "Error occurred while updating student."

    def remove_teacher(self, id: int) -> str:
        try:
            self.cursor.execute("DELETE FROM teachers WHERE id=?", (id,))
            self.connection.commit()
            return "Teacher removed successfully."
        except sqlite3.Error as e:
            print("Error occurred:", e)
            
    def email_exists(self, email: str) -> bool:
        self.cursor.execute("SELECT * FROM teachers WHERE email=?", (email,))
        if self.cursor.fetchone():
            return True
        else:
            return False

    def id_exists(self, id: int) -> bool:
        self.cursor.execute("SELECT * FROM teachers WHERE id=?", (id,))
        if self.cursor.fetchone():
            return True
        else:
            return False
        
    def get_password(self, identifier: str) -> str:
        query = "SELECT password FROM teachers WHERE email = ? OR id = ?"
        self.cursor.execute(query, (identifier, identifier))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def get_details(self, identifier):
        query = "SELECT id, email, password, first_name, last_name, phoneNo, subject_id FROM teachers WHERE email = ? OR id = ?"
        self.cursor.execute(query, (identifier, identifier))
        
        user = self.cursor.fetchone()
        if user:
            return user
        return []
    
    def get_details_by_id(self, id: int):
        query = f"SELECT id, email, first_name, last_name, phoneNo, subject_id FROM teachers WHERE CAST(id AS TEXT) LIKE '%{str(id)}%' "
        self.cursor.execute(query)
        
        users = self.cursor.fetchall()
        return users
    
    def get_details_by_name(self, name: str):
        name_parts = re.split(r'\s+', name.strip())
        
        if len(name_parts) == 1:
            first_name = name
            last_name = name
        else:
            first_name = name_parts[0]
            last_name = name_parts[1]
        
        query = f"SELECT id, email, first_name, last_name, phoneNo, subject_id FROM teachers WHERE first_name LIKE '%{first_name}%' OR last_name LIKE '%{last_name}%' "
        self.cursor.execute(query)
        
        users = self.cursor.fetchall()
        return users
    
    def drop_table(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS teachers")
            self.connection.commit()
            print("Table 'marks' dropped successfully.")
        except sqlite3.Error as e:
            print("Error occurred while dropping table 'teachers':", e)

    def close_connection(self):
        self.connection.close()