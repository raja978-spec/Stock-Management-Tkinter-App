from tkinter import *
from PIL import Image, ImageTk
from project_config import *
from login import *

w = Tk()
w.geometry('700x500')
w.title('Welcome Page')

login_background_image = Image.open('stationary.jpg').resize((700, 500))
login_background_image_tk = ImageTk.PhotoImage(login_background_image)

label_image = Label(w, image=login_background_image_tk)
label_image.image = login_background_image_tk
label_image.place(x=0, y=0)  

welcome_note = Label(w, text='''
Welcome to the 
Zink stationary shop''', 
                     font=CustomFontStyle(font_size=25), 
                     bg='white')
welcome_note.place(x=30, y=190)

def show_login_page():
    w.withdraw()
    Login_Page()

login_btn = Button(w, text='Click to login',
                   bg=background_color,
                   activebackground='white',
                   activeforeground='yellow',
                   command=show_login_page,
                   font=CustomFontStyle(font_size=15))
login_btn.place(x=100, y=350)
w.mainloop()
