from interface.util import *
import database_setup.college as college
from interface.dashboard.adminDashboard import admin_dashboard

def admin_login_page(root: Tk):
    
    def formard_to_welcome_page():
        admin_login_page_fr.destroy()
        root.update()
        return
    
    def login():
        identifier = id_number_ent.get()
        password = password_ent.get()
        admin = college.AdminDB()
        
        id_info = admin.id_exists(id=identifier)
        if not id_info:
            id_info = admin.username_exists(username=identifier)
        
        if not id_info:
            message_box(root, 'Incorrect Id')
            return
        
        retrieved_password = admin.get_password(identifier=identifier)

        if retrieved_password != password:
            message_box(root, 'Incorrect Password!')
            return
    
        admin.close_connection()
        admin_login_page_fr.destroy()
        admin_dashboard(root, identifier)
        root.update()
        # redirect

    admin_login_page_fr = Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = Label(admin_login_page_fr, text='Admin Login', bg=bg_color, 
                    fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=454)
    
    back_btn = Button(admin_login_page_fr, text='back', bg=bg_color,
                      fg='white', font=('Bold', 18), command=formard_to_welcome_page)
    back_btn.place(x=10, y=40)

    id_number_lb = Label(admin_login_page_fr, text='Enter Id or Username', font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=100, y=140)
    id_number_ent = Entry(admin_login_page_fr, font=('Bold', 15),
                        justify=CENTER, highlightcolor=bg_color,
                        highlightbackground='grey', highlightthickness=2)
    id_number_ent.place(x=100, y=180)

    password_lb = Label(admin_login_page_fr, text='Enter Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=100, y=230)
    password_ent = Entry(admin_login_page_fr, font=('Bold', 15),
                        justify=CENTER, highlightcolor=bg_color,
                        highlightbackground='grey', highlightthickness=2)
    password_ent.place(x=100, y=270)

    login_btn = Button(admin_login_page_fr, text='Login', font=('Bold', 15),
                    bg=bg_color, fg='white', command=login)
    login_btn.place(x=180, y=320, height=40)


    admin_login_page_fr.pack(pady=30)
    admin_login_page_fr.pack_propagate(False)
    admin_login_page_fr.configure(width=460, height=552)