from interface.util import *
from database_setup.teacher import TeacherDB
from database_setup.college import SubjectDB, AdminDB

bg_color_option='#c3c3c3'

def admin_dashboard(root: Tk, identifier: str):
    global user
    
    admin = AdminDB()
    user = admin.get_details(identifier)
    print(user)
    
    def update_user():
        global user
        user = admin.get_details(identifier)
        print(user)
    
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
    
    #MARK: home menu
    def home_page():
        home_page_fr = Frame(pages_fr)
        
        hi_lb = Label(home_page_fr, text='Hi, {}'.format(user[1]), font=('Bold', 15))
        hi_lb.place(x=130, y=50)
        
        details_lb = Label(home_page_fr,
                           text='''Username : {}\n\nId : {}'''.format(user[1], user[0]),
                           font=('Bold', 13), justify=LEFT)
        details_lb.place(x=20, y=130)
        
        home_page_fr.pack(fill=BOTH, expand=True)
        
        
    #MARK: teacher menu
    def teacher_page():
        
        def get_teacher_details():
            teach = TeacherDB()
            sub = SubjectDB()
            identifier = search_input.get()
            
            if find_by_option_btn.get() == 'id':
                details = teach.get_details_by_id(identifier)
            elif find_by_option_btn.get() == 'name':
                details = teach.get_details_by_name(identifier)
            
            # clear privious results
            for item in record_table.get_children():
                record_table.delete(item)
                
            if details:                    
                for detail in details:
                    curr_subject = sub.get_subject_name(detail[5])
                    if not curr_subject:
                        curr_subject = '-'
                    teacher_detail = [detail[0], detail[2] + " " + detail[3], curr_subject]
                    record_table.insert(parent='', index='end', values=teacher_detail)
            
            teach.close_connection()

        def generate_teacher_card():
            selection = record_table.selection()
            selected_id = record_table.item(item=selection, option='values')[0]
            
            teach = TeacherDB()
            sub = SubjectDB()
            teacher_details = teach.get_details(selected_id)
            subject_name = sub.get_subject_name(teacher_details[6])
            if not subject_name:
                subject_name = '-'
            
            teacher_card_fr = Frame(teacher_page_fr, highlightbackground='black', highlightthickness=3)
            
            heading_lb = Label(teacher_card_fr, text='Teacher Info', bg=bg_color, 
                            fg='white', font=('Bold', 13))
            heading_lb.place(x=0, y=0, width=344)
            
            back_btn = Button(teacher_card_fr, text='back', bg=bg_color,
                            fg='white', font=('Bold', 15), command=teacher_card_fr.destroy)
            back_btn.place(x=10, y=40)

            details_lb = Label(teacher_card_fr,
                            text='''Email : {}\n\nId : {}\n\nName : {}\n\nPhone No. : {}\n\nSubject : {}'''.format(teacher_details[1], teacher_details[0], teacher_details[3] + " " + teacher_details[4], teacher_details[5], subject_name),
                            font=('Bold', 13), justify=LEFT)
            details_lb.place(x=20, y=130)
            
            teacher_card_fr.pack(pady=10)
            teacher_card_fr.pack_propagate(False)
            teacher_card_fr.configure(width=400, height=400)
            teach.close_connection()
            sub.close_connection()
        
        def edit_subject():
            teach = TeacherDB()
            sub = SubjectDB()
            
            def help_subject():
                sub1 = SubjectDB()
                subjects = sub1.get_subject_names()
                # print(subjects)
                msg = ""
                for i in range(0, 6):
                    msg += str(i+1) + " : " + str(subjects[i])
                    if i % 2 == 0:
                        msg += "\t"
                    else:
                        msg += "\n"
                message_box(root, msg)
                sub1.close_connection()
                get_teacher_details()

            def update_subject_id():
                new_subject_id = int(new_subject_id_input.get())
                if not new_subject_id:
                    return
                if new_subject_id < 1 or new_subject_id > 6:
                    message_box(root, "Subject\ndoesn't exist.")
                    return
                msg = teach.update_teacher(selected_id, None, None, None, None, None, new_subject_id)
                message_box(root, msg)
                teacher_card_fr.destroy()
                teach.close_connection()
                get_teacher_details()
            
            selection = record_table.selection()
            selected_id = record_table.item(item=selection, option='values')[0]
            
            teacher_details = teach.get_details(selected_id)
            current_subject_id = teacher_details[6]
            if not current_subject_id:
                current_subject_id = '-'
            current_subject = sub.get_subject_name(teacher_details[6])
            if not current_subject:
                current_subject = '-'
            
            teacher_card_fr = Frame(teacher_page_fr, highlightbackground='black', highlightthickness=3)
            
            heading_lb = Label(teacher_card_fr, text='Update Associated Subject', bg=bg_color, 
                            fg='white', font=('Bold', 13))
            heading_lb.place(x=0, y=0, width=344)
            
            back_btn = Button(teacher_card_fr, text='back', bg=bg_color,
                            fg='white', font=('Bold', 10), command=teacher_card_fr.destroy)
            back_btn.place(x=10, y=40)

            details_lb = Label(teacher_card_fr,
                            text='''Id : {}\nCurrent Subject Id : {}\nCurrent Subject : {}'''.format(teacher_details[0], current_subject_id, current_subject),
                            font=('Bold', 13), justify=LEFT)
            details_lb.place(x=20, y=100)
            
            new_subject_id_lb = Label(teacher_card_fr, text='Enter New Subject Id', font=('Bold', 13))
            new_subject_id_lb.place(x=20, y=180)
            
            new_subject_id_help_lb = Button(teacher_card_fr, text='help', font=('Bold', 9), command=help_subject)
            new_subject_id_help_lb.place(x=250, y=180)
            
            new_subject_id_input = Entry(teacher_card_fr, font=('Bold', 13))
            new_subject_id_input.place(x=20, y=210)
            
            submit_btn = Button(teacher_card_fr, text='Submit', font=('Bold', 15),
                        bg=bg_color, fg='white', command=update_subject_id)
            submit_btn.place(x=120, y=260, height=40)
            
            teacher_card_fr.pack(pady=10)
            teacher_card_fr.pack_propagate(False)
            teacher_card_fr.configure(width=400, height=350)
            sub.close_connection()

        def enable_buttons():
            generate_teacher_card_btn.config(state=NORMAL)
            edit_subject_id_btn.config(state=NORMAL)

        
        search_filters = ['id', 'name']
        
        #MARK: teacher page
        teacher_page_fr = Frame(pages_fr)
        
        find_teacher_record_lb = Label(teacher_page_fr, text='Update teacher Score', font=('Bold', 13), fg="white", bg=bg_color)
        find_teacher_record_lb.place(x=20, y=10, width=300)
        
        find_by_lb = Label(teacher_page_fr, text="Find By:", font=('Bold', 12))
        find_by_lb.place(x=15, y=50)
        
        find_by_option_btn = Combobox(teacher_page_fr, font=('Bold', 12), state='readonly', values=search_filters)
        find_by_option_btn.place(x=80, y=50, width=80)
        find_by_option_btn.set('id')
        
        search_input = Entry(teacher_page_fr, font=('Bold', 12))
        search_input.place(x=20, y=90)
        search_input.bind('<KeyRelease>', lambda e: get_teacher_details())
        
        record_table_lb = Label(teacher_page_fr, text='Record Table', font=('Bold', 13), bg=bg_color, fg='white')
        record_table_lb.place(x=20, y=160, width=300)
        
        record_table = Treeview(teacher_page_fr)
        record_table.place(x=0, y=200, width=350)
        record_table.bind('<<TreeviewSelect>>', lambda e: enable_buttons())
        
        record_table['columns'] = ('id', 'name', 'subject_id')
        record_table.column('#0', stretch=NO, width=0)
        
        record_table.heading('id', text='Id', anchor=W)
        record_table.column('id', width=35, anchor=W)
        record_table.heading('name', text='Name', anchor=W)
        record_table.column('name', width=85, anchor=W)
        record_table.heading('subject_id', text='Subject', anchor=W)
        record_table.column('subject_id', width=45, anchor=W)
        
        generate_teacher_card_btn = Button(teacher_page_fr, text='Show teacher Card', font=('Bold', 13), bg=bg_color, fg='white', state=DISABLED, command=generate_teacher_card) 
        generate_teacher_card_btn.place(x=160, y=450)
        
        edit_subject_id_btn = Button(teacher_page_fr, text='Edit Subject', font=('Bold', 13), bg=bg_color, fg='white', state=DISABLED, command=edit_subject)
        edit_subject_id_btn.place(x=10, y=450)
        
        
        teacher_page_fr.pack(fill=BOTH, expand=True)
    
    
    #MARK: result menu
    def publish_result():
        
        def publish_result_status():
            global result_published_status
            
            if not result_published_status:
                if conformation_box(root, "publish result?"):
                    result_published_status = True
                    change_result_published_status()
                    publish_result_fr.destroy()
                    publish_result()

        def unpublish_result_status():
            global result_published_status
            
            if result_published_status:
                if conformation_box(root, "unpublish result?"):
                    result_published_status = False
                    change_result_published_status()
                    publish_result_fr.destroy()
                    publish_result()

        if result_published_status:
            current_status = 'Published'
        else:
            current_status = 'Unpublished'
            
        publish_result_fr = Frame(pages_fr)
        
        publish_heading_lb = Label(publish_result_fr, text='Publish Result', font=('Bold', 13), fg="white", bg=bg_color)
        publish_heading_lb.place(x=20, y=10, width=300)
        
        description_lb = Label(publish_result_fr, text='Click "Publish" to publish the result or \n"Unpublish" to unpublish it.', font=('Bold', 12))
        description_lb.place(x=30, y=80)
        
        current_status_lb = Label(publish_result_fr, text=f'Current Status: {current_status}', font=('Bold', 12))
        current_status_lb.place(x=60, y=150)
        
        publish_btn = Button(publish_result_fr, text='Publish', font=('Bold', 15),
                    bg=bg_color, fg='white', command=publish_result_status)
        publish_btn.place(x=50, y=300, height=40)
        
        unpublish_btn = Button(publish_result_fr, text='Unpublish', font=('Bold', 15),
                    bg=bg_color, fg='white', command=unpublish_result_status)
        unpublish_btn.place(x=200, y=300, height=40)
        
        if result_published_status:
            publish_btn.config(state=DISABLED)
            unpublish_btn.config(state=NORMAL)
        else:
            unpublish_btn.config(state=DISABLED)
            publish_btn.config(state=NORMAL)
        
        publish_result_fr.pack(fill=BOTH, expand=True)
    
    
    #MARK: security menu
    def security_page():
        
        def submit_em():
            new_username = new_username_ent.get()
            
            if new_username == '':
                new_username = None
                message_box(root, 'Username can\'t be empty!')
                return
                
            msg = admin.update_admin(user[0], new_username, None)
            message_box(root, msg)
            update_user()                
                
        def submit_pw():
            old_pw = current_pw_ent.get()
            new_pw = new_pw_ent.get()
            
            if old_pw != user[2]:
                message_box(root, 'Wrong Password!')
            else:
                if new_pw == '':
                    new_pw = None
                    message_box(root, 'Password can\'t be empty!')
                    return
                    
                msg = admin.update_admin(user[0], None, new_pw)
                message_box(root, msg)
                update_user()                
                
        security_page_fr = Frame(pages_fr)
        
        
        new_username_lb = Label(security_page_fr, text='Enter New Username', font=('Bold', 12))
        new_username_lb.place(x=50, y=30)
        
        new_username_ent = Entry(security_page_fr, font=('Bold', 12), highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
        new_username_ent.place(x=50, y=60)
        new_username_ent.insert(END, user[1])
        
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
        
    #MARK: logout menu
    def logout_page():
        answer = conformation_box(root, message='Log Out?')
        if answer == True:
            dashboard_fr.destroy()
            root.update()
        return
    
    
    #MARK: menu options
    options_fr = Frame(dashboard_fr, bg=bg_color_option, highlightbackground=bg_color, highlightthickness=3)
    
    home_btn = Button(options_fr, text='Home', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, command=lambda: on_click_option(home_btn, home_page))
    home_btn.place(x=4, y=50)
    # making home the initial page 
    home_btn.config(highlightbackground=bg_color, highlightthickness=1)
    home_page()
    
    find_teacher_btn = Button(options_fr, text='Teacher', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, justify=LEFT, command=lambda: on_click_option(find_teacher_btn, teacher_page))
    find_teacher_btn.place(x=4, y=120)
    
    publish_result_btn = Button(options_fr, text='Result', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, justify=LEFT, command=lambda: on_click_option(publish_result_btn, publish_result))
    publish_result_btn.place(x=4, y=190)
    
    security_btn = Button(options_fr, text='Security', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, command=lambda: on_click_option(security_btn, security_page))
    security_btn.place(x=4, y=260)
    
    logout_btn = Button(options_fr, text='Log Out', font=('Bold', 15), fg=bg_color, bg=bg_color_option, highlightbackground=bg_color_option, bd=0, command=lambda: on_click_option(logout_btn, logout_page))
    logout_btn.place(x=4, y=330)
    
        
    options_fr.place(x=0, y=0, width=120, height=575)
    
    
    
    dashboard_fr.pack(pady=5)
    dashboard_fr.pack_propagate(False)
    dashboard_fr.configure(width=480, height=580)
    