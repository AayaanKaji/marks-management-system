from interface.util import *
from database_setup.teacher import TeacherDB
from database_setup.college import SubjectDB
from database_setup.student import StudentDB, MarkDB

bg_color_option='#c3c3c3'

def teacher_dashboard(root: Tk, identifier: str):
    global user
    
    teac = TeacherDB()
    user = teac.get_details(identifier)
    print(user)
    teac.close_connection()
    sub = SubjectDB()
    subject_name = sub.get_subject_name(user[6])
    if not subject_name:
        subject_name = 'Subject'
    sub.close_connection()
    
    def update_user():
        global user
        teac = TeacherDB()
        user = teac.get_details(identifier)
        print(user)
        teac.close_connection()
    
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
                           text='''Email : {}\n\nId : {}\n\nName : {}\n\nPhone No. : {}\n\nSubject : {}'''.format(user[1], user[0], user[3] + " " + user[4], user[5], subject_name),
                           font=('Bold', 13), justify=LEFT)
        details_lb.place(x=20, y=130)
        
        home_page_fr.pack(fill=BOTH, expand=True)
        
        
    def find_student_page():
        
        def get_student_details():
            stud = StudentDB()
            markD = MarkDB()
            subject_id = user[6]
            identifier = search_input.get()
            
            if find_by_option_btn.get() == 'roll':
                details = stud.get_details_by_roll(identifier)
            elif find_by_option_btn.get() == 'name':
                details = stud.get_details_by_name(identifier)
            
            # clear privious results
            for item in record_table.get_children():
                record_table.delete(item)
                
            if details:                    
                for detail in details:
                    mark = markD.get_mark(detail[0], subject_id)
                    if not mark:
                        mark = '-'
                    student_detail = [detail[0], detail[2] + " " + detail[3], mark]
                    record_table.insert(parent='', index='end', values=student_detail)
            
            stud.close_connection()
            markD.close_connection()

        def generate_student_card():
            selection = record_table.selection()
            selected_roll = record_table.item(item=selection, option='values')[0]
            
            stud = StudentDB()
            student_details = stud.get_details(selected_roll)
            
            student_card_fr = Frame(find_student_page_fr, highlightbackground='black', highlightthickness=3)
            
            heading_lb = Label(student_card_fr, text='Student Info', bg=bg_color, 
                            fg='white', font=('Bold', 13))
            heading_lb.place(x=0, y=0, width=344)
            
            back_btn = Button(student_card_fr, text='back', bg=bg_color,
                            fg='white', font=('Bold', 15), command=student_card_fr.destroy)
            back_btn.place(x=10, y=40)

            details_lb = Label(student_card_fr,
                            text='''Email : {}\n\nRoll No. : {}\n\nName : {}\n\nPhone No. : {}'''.format(student_details[1], student_details[0], student_details[3] + " " + student_details[4], student_details[5]),
                            font=('Bold', 13), justify=LEFT)
            details_lb.place(x=20, y=130)
            
            student_card_fr.pack(pady=10)
            student_card_fr.pack_propagate(False)
            student_card_fr.configure(width=400, height=400)
            stud.close_connection()
        
        def edit_mark():
            if not user[6]:
                message_box(root, "You are not \nassociated \nwith any subject")
                return
            
            stud = StudentDB()
            markD = MarkDB()
            
            def update_marks():
                new_mark = int(new_mark_input.get())
                if not new_mark:
                    return
                msg = markD.update_mark(selected_roll, user[6], new_mark)
                message_box(root, msg)
                student_card_fr.destroy()
                markD.close_connection()
                get_student_details()
            
            selection = record_table.selection()
            selected_roll = record_table.item(item=selection, option='values')[0]
            
            student_details = stud.get_details(selected_roll)
            current_mark = markD.get_mark(student_details[0], user[6])
            if not current_mark:
                current_mark = '-'
            
            student_card_fr = Frame(find_student_page_fr, highlightbackground='black', highlightthickness=3)
            
            heading_lb = Label(student_card_fr, text='Update Marks', bg=bg_color, 
                            fg='white', font=('Bold', 13))
            heading_lb.place(x=0, y=0, width=344)
            
            back_btn = Button(student_card_fr, text='back', bg=bg_color,
                            fg='white', font=('Bold', 10), command=student_card_fr.destroy)
            back_btn.place(x=10, y=40)

            details_lb = Label(student_card_fr,
                            text='''Roll No. : {}\nCurrent Score : {}'''.format(student_details[0], current_mark),
                            font=('Bold', 13), justify=LEFT)
            details_lb.place(x=20, y=100)
            
            new_mark_lb = Label(student_card_fr, text='Enter New Score', font=('Bold', 13))
            new_mark_lb.place(x=20, y=180)
            
            new_mark_input = Entry(student_card_fr, font=('Bold', 13))
            new_mark_input.place(x=20, y=210)
            
            submit_btn = Button(student_card_fr, text='Submit', font=('Bold', 15),
                        bg=bg_color, fg='white', command=update_marks)
            submit_btn.place(x=120, y=260, height=40)
            
            student_card_fr.pack(pady=10)
            student_card_fr.pack_propagate(False)
            student_card_fr.configure(width=400, height=350)
            stud.close_connection()

        def enable_buttons():
            generate_student_card_btn.config(state=NORMAL)
            edit_mark_btn.config(state=NORMAL)

        
        search_filters = ['roll', 'name']
        
        find_student_page_fr = Frame(pages_fr)
        
        find_student_record_lb = Label(find_student_page_fr, text='Update Student Score', font=('Bold', 13), fg="white", bg=bg_color)
        find_student_record_lb.place(x=20, y=10, width=300)
        
        find_by_lb = Label(find_student_page_fr, text="Find By:", font=('Bold', 12))
        find_by_lb.place(x=15, y=50)
        
        find_by_option_btn = Combobox(find_student_page_fr, font=('Bold', 12), state='readonly', values=search_filters)
        find_by_option_btn.place(x=80, y=50, width=80)
        find_by_option_btn.set('roll')
        
        search_input = Entry(find_student_page_fr, font=('Bold', 12))
        search_input.place(x=20, y=90)
        search_input.bind('<KeyRelease>', lambda e: get_student_details())
        
        record_table_lb = Label(find_student_page_fr, text='Record Table', font=('Bold', 13), bg=bg_color, fg='white')
        record_table_lb.place(x=20, y=160, width=300)
        
        record_table = Treeview(find_student_page_fr)
        record_table.place(x=0, y=200, width=350)
        record_table.bind('<<TreeviewSelect>>', lambda e: enable_buttons())
        
        record_table['columns'] = ('roll', 'name', 'marks')
        record_table.column('#0', stretch=NO, width=0)
        
        record_table.heading('roll', text='Roll No', anchor=W)
        record_table.column('roll', width=35, anchor=W)
        record_table.heading('name', text='Name', anchor=W)
        record_table.column('name', width=85, anchor=W)
        record_table.heading('marks', text=f'{subject_name} Marks', anchor=W)
        record_table.column('marks', width=45, anchor=W)
        
        generate_student_card_btn = Button(find_student_page_fr, text='Show Student Card', font=('Bold', 13), bg=bg_color, fg='white', state=DISABLED, command=generate_student_card) 
        generate_student_card_btn.place(x=160, y=450)
        
        edit_mark_btn = Button(find_student_page_fr, text='Edit Mark', font=('Bold', 13), bg=bg_color, fg='white', state=DISABLED, command=edit_mark)
        edit_mark_btn.place(x=10, y=450)
        
        
        find_student_page_fr.pack(fill=BOTH, expand=True)
        
    def security_page():
        
        def submit_em():
            new_email = new_email_ent.get()
            teac1 = TeacherDB()
            
            if new_email == '':
                new_email = None
                message_box(root, 'Email can\'t be empty!')
                return
            if not check_email(new_email):
                message_box(root, 'Wrong Email Format!')
                return
                
            msg = teac1.update_teacher(user[0], new_email, None)
            message_box(root, msg)
            update_user()
            teac1.close_connection()
                
                
        def submit_pw():
            old_pw = current_pw_ent.get()
            new_pw = new_pw_ent.get()
            teac1 = TeacherDB()
            
            if old_pw != user[2]:
                message_box(root, 'Wrong Password!')
            else:
                if new_pw == '':
                    new_pw = None
                    message_box(root, 'Password can\'t be empty!')
                    return
                    
                msg = teac1.update_teacher(user[0], None, new_pw)
                message_box(root, msg)
                update_user()
            teac1.close_connection()
                
                
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
            teac1 = TeacherDB()
            new_fn = first_name_ent.get()
            new_ln = last_name_ent.get()
            new_ph = phone_ent.get()
            print(new_fn)
            
            if new_fn == '':
                message_box(root, 'First Name \ncan\'t be empty!')
                return
            
            if not conformation_box(root, 'Update?'):
                return
            msg = teac1.update_teacher(user[0], None, None, new_fn, new_ln, new_ph)
            message_box(root, msg)
            update_user()
            teac1.close_connection()
            
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
    
    find_student_btn = Button(options_fr, text='Student', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, justify=LEFT, command=lambda: on_click_option(find_student_btn, find_student_page))
    find_student_btn.place(x=4, y=120)
    
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
    