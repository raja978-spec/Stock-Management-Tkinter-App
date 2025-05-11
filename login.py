from tkinter import *
from PIL import Image, ImageTk
from project_config import *
from register import Register_Page
from main import *
from model_connection import *
from tkinter import messagebox

def Login_Page():
    w = Toplevel()
    w.geometry('700x500')
    w.title('Login Page')

    login_background_image = Image.open('login_bg.jpg').resize((700, 500))
    login_background_image_tk = ImageTk.PhotoImage(login_background_image)
    w.bg_image = login_background_image_tk 

    label_image = Label(w, image=login_background_image_tk)
    label_image.place(x=0, y=0)  

    heading_label = Label(w, text='Login', 
                        font=CustomFontStyle(font_size=30,
                                             weight='bold'),
                        background='white')
    heading_label.place(x=200, y=100)

    gmail_label = Label(w, text='Gmail:', 
                        font=CustomFontStyle(font_size=15),
                        background='white')
    gmail_label.place(x=200, y=200)

    g_entry = Entry(w,bg='white', font=CustomFontStyle(font_size=15)
                    )
    g_entry.place(x=350, y=200)

    password_label = Label(w, text='Password:', 
                        font=CustomFontStyle(font_size=15),
                        background='white')
    password_label.place(x=200, y=250)

    pass_entry = Entry(w,bg='white',font=CustomFontStyle(font_size=15))
    pass_entry.place(x=350, y=250)

    def show_main_page():
        result = run_query(f'select * from users where gmail="{g_entry.get()}" and password="{pass_entry.get()}"')
        is_user_exist = result.__len__()>=1
        logged_in_user = None

        if is_user_exist:
            w.withdraw()
            logged_in_user = result[0]
            stock_app(logged_in_user)
        else:
             messagebox.showerror("Error", "User doesn't exist please register (or) check the entered gmail and password is correct")
        return
    
    login_btn = Button(w, text='Login',
                   bg=background_color,
                   activebackground='white',
                   activeforeground='yellow',
                   command=show_main_page,
                   font=CustomFontStyle(font_size=15))
    login_btn.place(x=350, y=300)

    Or_label = Label(w,text='OR', font=CustomFontStyle(
        font_size=15, weight='bold'
    ),
    background='white')
    Or_label.place(x=350, y=350)

    def show_register():
        Register_Page()

    register_btn = Button(w, text='Register',
                   bg=background_color,
                   activebackground='white',
                   activeforeground='yellow',
                   command=show_register,
                   font=CustomFontStyle(font_size=15))
    register_btn.place(x=350, y=380)
    w.mainloop()
