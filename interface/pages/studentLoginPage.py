from interface.util import *
import database_setup.student as student
from interface.dashboard.studentDashoard import student_dashboard

def student_login_page(root: Tk):
    
    def formard_to_welcome_page():
        student_login_page_fr.destroy()
        root.update()
        return
    
    def login():
        identifier = id_number_ent.get()
        password = password_ent.get()
        stud = student.StudentDB()
        
        id_info = stud.roll_exists(rollNo=identifier)
        if not id_info:
            id_info = stud.email_exists(email=identifier)
        
        if not id_info:
            message_box(root, 'Incorrect Id!')
            return
        
        retrieved_password = stud.get_password(identifier=identifier)

        if retrieved_password != password:
            message_box(root, 'Incorrect Password!')
            return

        stud.close_connection()
        student_login_page_fr.destroy()
        student_dashboard(root, identifier)
        root.update()
        return
        
    student_login_page_fr = Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = Label(student_login_page_fr, text='Student Login', bg=bg_color, 
                    fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=454)
    
    back_btn = Button(student_login_page_fr, text='back', bg=bg_color,
                      fg='white', font=('Bold', 18), command=formard_to_welcome_page)
    back_btn.place(x=10, y=40)

    id_number_lb = Label(student_login_page_fr, text='Enter Roll No or Email Id', font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=100, y=140)
    id_number_ent = Entry(student_login_page_fr, font=('Bold', 15),
                        justify=CENTER, highlightcolor=bg_color,
                        highlightbackground='grey', highlightthickness=2)
    id_number_ent.place(x=100, y=180)

    password_lb = Label(student_login_page_fr, text='Enter Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=100, y=230)
    password_ent = Entry(student_login_page_fr, font=('Bold', 15),
                        justify=CENTER, highlightcolor=bg_color,
                        highlightbackground='grey', highlightthickness=2)
    password_ent.place(x=100, y=270)

    login_btn = Button(student_login_page_fr, text='Login', font=('Bold', 15),
                    bg=bg_color, fg='white', command=login)
    login_btn.place(x=180, y=320, height=40)


    student_login_page_fr.pack(pady=30)
    student_login_page_fr.pack_propagate(False)
    student_login_page_fr.configure(width=460, height=552)