from interface.util import *
from interface.pages.welcomePage import welcome_page

root = Tk()
root.title("Marks Management System")
root.geometry("500x600")

welcome_page(root)

root.mainloop()