from interface.util import *
import database_setup.student as student, database_setup.teacher as teacher

def registration_page(root: Tk):
    
    def formard_to_welcome_page():
        ans = conformation_box(root, message='Leave Registration Form?')
        if ans:
            registration_page_fr.destroy()
            root.update()
            return
    
    def check_input_validation() -> bool:
        if email_ent.get() == '':
            # email_ent.config(highlightcolor='red', highlightbackground='red')
            email_ent.focus()
            message_box(root, message='Email Required')
            return False
        if not check_email(email=email_ent.get().lower()):
            # email_ent.config(highlightcolor='red', highlightbackground='red')
            email_ent.focus()
            message_box(root, message='Enter a Valid Email')
            return False
        if password_ent.get() == '':
            # password_ent.config(highlightcolor='red', highlightbackground='red')
            password_ent.focus()
            message_box(root, message='Password Required')
            return
        if first_name_ent.get() == '':
            # first_name_ent.config(highlightcolor='red', highlightbackground='red')
            first_name_ent.focus()
            message_box(root, message='Name Required')
            return False
        if user_type_var.get() == '':
            # user_type_radio_button1.config(highlightcolor='red', highlightbackground='red')
            user_type_radio_button1.focus()
            message_box(root, message='Slecet User Type')
            return False
        return True
        
        
    def register():
        email = email_ent.get()
        password = password_ent.get()
        first_name = first_name_ent.get()
        last_name = last_name_ent.get()
        phone_number = phone_number_ent.get()
        user_type = user_type_var.get()
        user_message = ''
        
        if user_type == 'student':
            stud = student.StudentDB()
            user_message = stud.add_student(email, password, first_name, last_name, phone_number)
            message_box(root, user_message)
            stud.close_connection()
        
        if user_type == 'teacher':
            teac = teacher.TeacherDB()
            user_message = teac.add_teacher(email, password, first_name, last_name, phone_number)
            message_box(root, user_message)
            teac.close_connection()
        
        if 'added' in user_message.lower():
                registration_page_fr.destroy()
                root.update()
                return
    
    
    def execute():
        if check_input_validation():
            register()
    
        
    user_type_var = StringVar()
        
    registration_page_fr = Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = Label(registration_page_fr, text='Create Account', bg=bg_color, 
                    fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=454)
    
    back_btn = Button(registration_page_fr, text='back', bg=bg_color,
                      fg='white', font=('Bold', 18), command=formard_to_welcome_page)
    back_btn.place(x=10, y=40)
    
    ## student or teacher
    user_type_radio_button1 = Radiobutton(registration_page_fr, text='Student', font=('Bold', 12),
                                          variable=user_type_var, value='student')
    user_type_radio_button1.place(x = 100, y = 70)
    user_type_radio_button2 = Radiobutton(registration_page_fr, text='Teacher', font=('Bold', 12),
                                          variable=user_type_var, value='teacher')
    user_type_radio_button2.place(x = 200, y = 70)
    user_type_var.set('student')
  
    ent_gap = 30
    field_gap = 70
    start = 100
    
    email_lb = Label(registration_page_fr, text='Email', font=('Bold', 15), fg=bg_color)
    email_lb.place(x=100, y=start)
    email_ent = Entry(registration_page_fr, font=('Bold', 15),
                      highlightcolor=bg_color,
                      highlightbackground='grey', highlightthickness=2)
    email_ent.place(x=100, y=(start + ent_gap))

    password_lb = Label(registration_page_fr, text='Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=100, y=(start + field_gap))
    password_ent = Entry(registration_page_fr, font=('Bold', 15),
                         show='*', highlightcolor=bg_color,
                         highlightbackground='grey', highlightthickness=2)
    password_ent.place(x=100, y=(start + field_gap )+ ent_gap)

    first_name_lb = Label(registration_page_fr, text='First Name', font=('Bold', 15), fg=bg_color)
    first_name_lb.place(x=100, y=(start + field_gap * 2))
    first_name_ent = Entry(registration_page_fr, font=('Bold', 15),
                           highlightcolor=bg_color,
                           highlightbackground='grey', highlightthickness=2)
    first_name_ent.place(x=100, y=(start + field_gap*2 + ent_gap))

    last_name_lb = Label(registration_page_fr, text='Last Name', font=('Bold', 15), fg=bg_color)
    last_name_lb.place(x=100, y=(start + field_gap*3))
    last_name_ent = Entry(registration_page_fr, font=('Bold', 15),
                          highlightcolor=bg_color,
                          highlightbackground='grey', highlightthickness=2)
    last_name_ent.place(x=100, y=(start + field_gap*3 + ent_gap))

    phone_number_lb = Label(registration_page_fr, text='Phone Number', font=('Bold', 15), fg=bg_color)
    phone_number_lb.place(x=100, y=(start + field_gap*4))
    phone_number_ent = Entry(registration_page_fr, font=('Bold', 15),
                          highlightcolor=bg_color,
                          highlightbackground='grey', highlightthickness=2)
    phone_number_ent.place(x=100, y=(start + field_gap*4 + ent_gap))

    submit_btn = Button(registration_page_fr, text='Submit', font=('Bold', 15),
                    bg=bg_color, fg='white', command=execute)
    submit_btn.place(x=180, y=(start + field_gap*5), height=40)


    registration_page_fr.pack(pady=30)
    registration_page_fr.pack_propagate(False)
    registration_page_fr.configure(width=460, height=552)