from interface.util import *
from database_setup.student import StudentDB, MarkDB
from database_setup.college import SubjectDB

bg_color_option='#c3c3c3'

def student_dashboard(root: Tk, identifier: str):
    global user
    
    stud = StudentDB()
    user = stud.get_details(identifier)
    print(user)
    stud.close_connection()
    
    def update_user():
        global user
        stud = StudentDB()
        user = stud.get_details(identifier)
        print(user)
        stud.close_connection()
    
    global prev_btn
    prev_btn = None
    
    def on_click_option(btn: Frame, page):
        global prev_btn
        if prev_btn is not None:
            prev_btn.config(highlightthickness=0)
        else:
            home_btn.config(highlightthickness=0)
        prev_btn = btn
        btn.config(highlightbackground=bg_color, highlightthickness=1)
        
        if btn != logout_btn:
            for child in pages_fr.winfo_children():
                child.destroy()
                root.update()
        page()
        return
        
            
    dashboard_fr = Frame(root, highlightbackground=bg_color, highlightthickness=3)
    
    
    
    pages_fr = Frame(dashboard_fr)
    pages_fr.place(x=122, y=5, width=350, height=550)
    
    def home_page():
        home_page_fr = Frame(pages_fr)
        
        hi_lb = Label(home_page_fr, text='Hi, {}'.format(user[3]), font=('Bold', 15))
        hi_lb.place(x=130, y=50)
        
        details_lb = Label(home_page_fr,
                           text='''Email : {}\n\nRoll No. : {}\n\nName : {}\n\nPhone No. : {}'''.format(user[1], user[0], user[3] + " " + user[4], user[5]),
                           font=('Bold', 13), justify=LEFT)
        details_lb.place(x=20, y=130)
        
        home_page_fr.pack(fill=BOTH, expand=True)
        
    def marks_page():
        marks_page_fr = Frame(pages_fr)
        
        
        marks_title_lb = Label(marks_page_fr, text='Mark Sheet', font=('Bold', 20), justify=CENTER)
        marks_title_lb.place(x=100, y=30)
        
        subject_name_lb = Label(marks_page_fr, text='Subjects', font=('Bold', 17))
        subject_name_lb.place(x=5, y=100)
        
        subject_marks_lb = Label(marks_page_fr, text='Score', font=('Bold', 17))
        subject_marks_lb.place(x=150, y=100)
        
        subject_grade_lb = Label(marks_page_fr, text='Grade', font=('Bold', 17))
        subject_grade_lb.place(x=270, y=100)
        
        marks = MarkDB()
        subs = SubjectDB()
        
        gap = 60
        
        for i in range(1, 7):
            subject = subs.get_subject_name(i)
            mark = marks.get_mark(user[0], i)
            if not mark:
                mark = '-'
            grade = marks.get_grade(user[0], i)
            if not grade:
                grade = '-'
            
            subject_name_lb_i = Label(marks_page_fr, text=f'{subject}', font=('Bold', 15))
            subject_name_lb_i.place(x=20, y=100+gap)
            
            subject_marks_lb_i = Label(marks_page_fr, text=f'{mark}', font=('Bold', 15))
            subject_marks_lb_i.place(x=165, y=100+gap)
            
            subject_grade_lb_i = Label(marks_page_fr, text=f'{grade}', font=('Bold', 15))
            subject_grade_lb_i.place(x=290, y=100+gap)
            
            gap += 40
        
        marks_page_fr.pack(fill=BOTH, expand=True)
        
    def security_page():
        
        def submit_em():
            new_email = new_email_ent.get()
            stud1 = StudentDB()
            
            if new_email == '':
                new_email = None
                message_box(root, 'Email can\'t be empty!')
                return
            if not check_email(new_email):
                message_box(root, 'Wrong Email Format!')
                return
                
            msg = stud1.update_student(user[0], new_email, None)
            message_box(root, msg)
            update_user()
            stud1.close_connection()
                
                
        def submit_pw():
            old_pw = current_pw_ent.get()
            new_pw = new_pw_ent.get()
            stud1 = StudentDB()
            
            if old_pw != user[2]:
                message_box(root, 'Wrong Password!')
            else:
                if new_pw == '':
                    new_pw = None
                    message_box(root, 'Password can\'t be empty!')
                    return
                    
                msg = stud1.update_student(user[0], None, new_pw)
                message_box(root, msg)
                update_user()
            stud1.close_connection()
                
                
        security_page_fr = Frame(pages_fr)
        
        
        new_email_lb = Label(security_page_fr, text='Enter New Email', font=('Bold', 12))
        new_email_lb.place(x=50, y=30)
        
        new_email_ent = Entry(security_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        new_email_ent.place(x=50, y=60)
        new_email_ent.insert(END, user[1])
        
        submit_em_btn = Button(security_page_fr, text='Submit', font=('Bold', 15),
                    bg=bg_color, fg='white', command=submit_em)
        submit_em_btn.place(x=100, y=110, height=40)
        
        
        current_pw_lb = Label(security_page_fr, text='Enter Current Password', font=('Bold', 12))
        current_pw_lb.place(x=50, y=200)
        
        current_pw_ent = Entry(security_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        current_pw_ent.place(x=50, y=230)
        
        new_pw_lb = Label(security_page_fr, text='Enter New Password', font=('Bold', 12))
        new_pw_lb.place(x=50, y=290)
        
        new_pw_ent = Entry(security_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        new_pw_ent.place(x=50, y=320)
        
        submit_btn = Button(security_page_fr, text='Submit', font=('Bold', 15),
                    bg=bg_color, fg='white', command=submit_pw)
        submit_btn.place(x=100, y=370, height=40)
        
        
        security_page_fr.pack(fill=BOTH, expand=True)
        
    def edit_page():
        
        def update():
            stud1 = StudentDB()
            new_fn = first_name_ent.get()
            new_ln = last_name_ent.get()
            new_ph = phone_ent.get()
            print(new_fn)
            
            if new_fn == '':
                message_box(root, 'First Name can\'t be empty!')
                return
            
            if not conformation_box(root, 'Update?'):
                return
            msg = stud1.update_student(user[0], None, None, new_fn, new_ln, new_ph)
            message_box(root, msg)
            update_user()
            stud1.close_connection()
            
        edit_page_fr = Frame(pages_fr)
        
        
        first_name_lb = Label(edit_page_fr, text='Change First Name', font=('Bold', 12))
        first_name_lb.place(x=50, y=30)
        
        first_name_ent = Entry(edit_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        first_name_ent.place(x=50, y=60)
        first_name_ent.insert(END, user[3])

        
        last_name_lb = Label(edit_page_fr, text='Change Last Name', font=('Bold', 12))
        last_name_lb.place(x=50, y=120)
        
        last_name_ent = Entry(edit_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        last_name_ent.place(x=50, y=150)
        last_name_ent.insert(END, user[4])
        
        phone_lb = Label(edit_page_fr, text='Change Phone Number', font=('Bold', 12))
        phone_lb.place(x=50, y=210)
        
        phone_ent = Entry(edit_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        phone_ent.place(x=50, y=240)
        phone_ent.insert(END, user[5])
        
        update_btn = Button(edit_page_fr, text='Update', font=('Bold', 15),
                    bg=bg_color, fg='white', command=update)
        update_btn.place(x=100, y=310, height=40)
        
        edit_page_fr.pack(fill=BOTH, expand=True)
    
    def logout_page():
        answer = conformation_box(root, message='Log Out?')
        if answer == True:
            dashboard_fr.destroy()
            root.update()
        return
    
    
    
    options_fr = Frame(dashboard_fr, bg=bg_color_option, highlightbackground=bg_color, highlightthickness=3)
    
    home_btn = Button(options_fr, text='Home', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, command=lambda: on_click_option(home_btn, home_page))
    home_btn.place(x=4, y=50)
    # making home the initial page 
    home_btn.config(highlightbackground=bg_color, highlightthickness=1)
    home_page()
    
    details_btn = Button(options_fr, text='Marks', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, justify=LEFT, command=lambda: on_click_option(details_btn, marks_page))
    details_btn.place(x=4, y=120)
    
    security_btn = Button(options_fr, text='Security', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, command=lambda: on_click_option(security_btn, security_page))
    security_btn.place(x=4, y=190)
    
    edit_btn = Button(options_fr, text='Edit', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, justify=LEFT, command=lambda: on_click_option(edit_btn, edit_page))
    edit_btn.place(x=4, y=260)
    
    logout_btn = Button(options_fr, text='Log Out', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, command=lambda: on_click_option(logout_btn, logout_page))
    logout_btn.place(x=4, y=330)
    
        
    options_fr.place(x=0, y=0, width=120, height=575)
    
    
    
    dashboard_fr.pack(pady=5)
    dashboard_fr.pack_propagate(False)
    dashboard_fr.configure(width=480, height=580)
    