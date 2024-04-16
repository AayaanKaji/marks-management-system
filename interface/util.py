import sys
sys.path.append("../marks-management-system")

from tkinter import *
from tkinter.ttk import Combobox, Treeview
import re

bg_color = '#A020F0'
image_width = 40
image_height = 50


def check_email(email: str) -> bool:
    pattern = r"^[a-z]([a-z0-9]+)*(\.[a-z0-9]+)*@([a-z0-9]+)+(\.[a-z]{2,4})$"
    
    match = re.match(pattern=pattern, string=email)
    
    return bool(match)


def message_box(root: Tk, message: str):
    message_box_fr = Frame(root, highlightbackground=bg_color,
                                highlightthickness=3)
    message_lb = Label(message_box_fr, text=message, font=('Bold', 15),
                       justify=CENTER)
    message_lb.pack(pady=50)
    
    close_btn = Button(message_box_fr, text="X", font=('Bold',13),
                        bd=0, fg=bg_color, command=lambda: message_box_fr.destroy())
    close_btn.place(x=270, y=5)
    
    message_box_fr.place(x=100, y=120, width=320, height=220)
    
    root.wait_window(message_box_fr)


def conformation_box(root: Tk, message: str):
    
    answer = BooleanVar()
    answer.set(False)
    
    def action(ans):
        answer.set(ans)
        conformation_box_fr.destroy()
        root.update()
    
    conformation_box_fr = Frame(root, highlightbackground=bg_color,
                                highlightthickness=3)
    message_lb = Label(conformation_box_fr, text=message, font=('Bold', 15),
                       justify=CENTER)
    message_lb.pack(pady=20)
    
    cancel_btn = Button(conformation_box_fr, text="Cancel", font=('Bold',15),
                        bd=0, bg=bg_color, fg='white',
                        command=lambda: action(False))
    cancel_btn.place(x=50, y=160)
    
    yes_btn = Button(conformation_box_fr, text="Yes", font=('Bold',15),
                        bd=0, bg=bg_color, fg='white',
                        command=lambda: action(True))
    yes_btn.place(x=190, y=160)
    
    conformation_box_fr.place(x=100, y=120, width=320, height=220)
    
    root.wait_window(conformation_box_fr)
    return answer.get()


# to keep tack of result status
global result_published_status
result_published_status = False
    
def change_result_published_status():
    global result_published_status
    result_published_status = not result_published_status

def published() -> bool:
    global result_published_status
    if result_published_status:
        return True
    return False