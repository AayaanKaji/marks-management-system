from interface.util import *
import database_setup.teacher as teacher
from interface.dashboard.teacherDashboard import teacher_dashboard

def teacher_login_page(root: Tk):
    
    def formard_to_welcome_page():
        teacher_login_page_fr.destroy()
        root.update()
        return
    
    def login():
        identifier = id_number_ent.get()
        password = password_ent.get()
        teach = teacher.TeacherDB()
        
        id_info = teach.id_exists(id=identifier)
        if not id_info:
            id_info = teach.email_exists(email=identifier)
        
        if not id_info:
            message_box(root, 'Incorrect Id')
            return
        
        retrieved_password = teach.get_password(identifier=identifier)

        if retrieved_password != password:
            message_box(root, 'Incorrect Password!')
            return

        teach.close_connection()
        teacher_login_page_fr.destroy()
        root.update()
        teacher_dashboard(root, identifier)
        root.update()
        return

    teacher_login_page_fr = Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = Label(teacher_login_page_fr, text='Teacher Login', bg=bg_color, 
                    fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=454)
    
    back_btn = Button(teacher_login_page_fr, text='back', bg=bg_color,
                      fg='white', font=('Bold', 18), command=formard_to_welcome_page)
    back_btn.place(x=10, y=40)

    id_number_lb = Label(teacher_login_page_fr, text='Enter Id or Email', font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=100, y=140)
    id_number_ent = Entry(teacher_login_page_fr, font=('Bold', 15),
                        justify=CENTER, highlightcolor=bg_color,
                        highlightbackground='grey', highlightthickness=2)
    id_number_ent.place(x=100, y=180)

    password_lb = Label(teacher_login_page_fr, text='Enter Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=100, y=230)
    password_ent = Entry(teacher_login_page_fr, font=('Bold', 15),
                        justify=CENTER, highlightcolor=bg_color,
                        highlightbackground='grey', highlightthickness=2)
    password_ent.place(x=100, y=270)

    login_btn = Button(teacher_login_page_fr, text='Login', font=('Bold', 15),
                    bg=bg_color, fg='white', command=login)
    login_btn.place(x=180, y=320, height=40)


    teacher_login_page_fr.pack(pady=30)
    teacher_login_page_fr.pack_propagate(False)
    teacher_login_page_fr.configure(width=460, height=552)