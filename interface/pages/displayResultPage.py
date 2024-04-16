from interface.util import *
from database_setup.college import SubjectDB
from database_setup.student import StudentDB, MarkDB, ResultDB

bg_color_option='#c3c3c3'

def display_result_page(root: Tk):
    global result_published_status
    if not published():
        message_box(root, "\nResult not published yet.\nContact admin.")
        return
    
    stud = StudentDB()
    markD = MarkDB()
    subs = SubjectDB()
    result = ResultDB()
    
    subjects = subs.get_subject_names()
    result.reload_result()
            
    dashboard_fr = Frame(root, highlightbackground=bg_color, highlightthickness=3)

        
    def get_student_details():
        identifier = search_input.get()
        order_filter = order_by_option_btn.get()
        
        if not identifier:
            details = result.get_results_with_filter(order_filter)
        else:
            details = result.get_details_by_roll_with_filter(identifier, order_filter)
        
        # clear privious results
        for item in record_table.get_children():
            record_table.delete(item)
            
        if details:                    
            for detail in details:
                detail = [(x if (x is not None and x) else '-') for x in detail]
                record_table.insert(parent='', index='end', values=detail)

        
    def generate_student_card():
        selection = record_table.selection()
        selected_roll = record_table.item(item=selection, option='values')[0]
        
        student_details = stud.get_details(selected_roll)
        
        student_card_fr = Frame(student_page_fr, highlightbackground='black', highlightthickness=3)
        
        heading_lb = Label(student_card_fr, text='Student Info', bg=bg_color, 
                        fg='white', font=('Bold', 13))
        heading_lb.place(x=0, y=0, width=344)
        
        back_btn = Button(student_card_fr, text='back', bg=bg_color,
                        fg='white', font=('Bold', 15), command=student_card_fr.destroy)
        back_btn.place(x=10, y=40)

        details_lb = Label(student_card_fr,
                        text='''Roll No. : {}\n\nName : {}'''.format(student_details[0], student_details[3] + " " + student_details[4]),
                        font=('Bold', 13), justify=LEFT)
        details_lb.place(x=20, y=130)
        
        student_card_fr.pack(pady=10)
        student_card_fr.pack_propagate(False)
        student_card_fr.configure(width=400, height=400)

    def enable_buttons():
        generate_student_card_btn.config(state=NORMAL)
    
    def back():
        dashboard_fr.destroy()
        root.update()
        return
    
    search_filters = ['Roll']
    order_filters = "Roll, "
    for subject in subjects:
        order_filters += f"{subject}, "
    order_filters += "Total"
    order_filters = tuple(order_filters.split(", "))
     
    student_page_fr = Frame(dashboard_fr)
    
    student_result_lb = Label(student_page_fr, text='Result Board', font=('Bold', 13), fg="white", bg=bg_color)
    student_result_lb.place(x=20, y=10, width=430)
    
    find_by_lb = Label(student_page_fr, text="Find By:", font=('Bold', 12))
    find_by_lb.place(x=25, y=50)
    
    find_by_option_btn = Combobox(student_page_fr, font=('Bold', 12), state='readonly', values=search_filters)
    find_by_option_btn.place(x=95, y=50, width=80)
    find_by_option_btn.set('Roll')
    
    search_input = Entry(student_page_fr, font=('Bold', 12))
    search_input.place(x=25, y=90)
    search_input.bind('<KeyRelease>', lambda e: get_student_details())
    
    order_by_lb = Label(student_page_fr, text="Order By:", font=('Bold', 12))
    order_by_lb.place(x=250, y=50)
    
    order_by_option_btn = Combobox(student_page_fr, font=('Bold', 12), state='readonly', values=order_filters)
    order_by_option_btn.place(x=345, y=50, width=80)
    order_by_option_btn.set('Total')
    
    apply_filter_btn = Button(student_page_fr, text='Apply Filter', font=('Bold', 13), bg=bg_color, fg='white', command=get_student_details) 
    apply_filter_btn.place(x=300, y=80)
    
    record_table_lb = Label(student_page_fr, text='Record Table', font=('Bold', 13), bg=bg_color, fg='white')
    record_table_lb.place(x=80, y=160, width=300)
    
    record_table = Treeview(student_page_fr)
    record_table.place(x=0, y=200, width=470)
    record_table.bind('<<TreeviewSelect>>', lambda e: enable_buttons())
    
    column_names = "roll, "
    for subject in subjects:
        column_names += f"{subject}, "
    column_names += "total"

    record_table['columns'] = tuple(column_names.split(", ")) 
    record_table.column('#0', stretch=NO, width=0)
    
    record_table.heading('roll', text='Roll', anchor=W)
    record_table.column('roll', width=15, anchor=W)
    for subject in subjects:
        record_table.heading(f'{subject}', text=f'{subject}', anchor=W)
        record_table.column(f'{subject}', width=25, anchor=W)
    record_table.heading('total', text='Total', anchor=W)
    record_table.column('total', width=25, anchor=W)
    
    
    generate_student_card_btn = Button(student_page_fr, text='Show Student Card', font=('Bold', 13), bg=bg_color, fg='white', state=DISABLED, command=generate_student_card) 
    generate_student_card_btn.place(x=130, y=450)
    
    
    back_btn = Button(student_page_fr, text='back', font=('Bold', 9), bg=bg_color, fg='white', command=back) 
    back_btn.place(x=30, y=520)
    
    student_page_fr.pack(fill=BOTH, expand=True)
    get_student_details()
    
    dashboard_fr.pack(pady=5)
    dashboard_fr.pack_propagate(False)
    dashboard_fr.configure(width=480, height=580)
    