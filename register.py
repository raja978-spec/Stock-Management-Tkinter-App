from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from project_config import *
from main import *
from model_connection import *

def Register_Page():
    w = Toplevel()
    w.geometry('700x500')
    w.title('Register Page')

    login_background_image = Image.open('login_bg.jpg').resize((700, 500))
    login_background_image_tk = ImageTk.PhotoImage(login_background_image)
    w.bg_image = login_background_image_tk  # Keep reference

    bg_label = Label(w, image=login_background_image_tk)
    bg_label.place(x=0, y=0)

    form_frame = Frame(w, bg="white")
    form_frame.place(x=50, y=100)

    heading_label = Label(form_frame, text='Register', 
                          font=CustomFontStyle(font_size=30, weight='bold'),
                          bg='white')
    heading_label.grid(row=0, column=0, columnspan=2, pady=20)

    gmail_label = Label(form_frame, text='Gmail:', 
                        font=CustomFontStyle(font_size=15),
                        bg='white')
    gmail_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)

    g_entry = Entry(form_frame, bg='white', font=CustomFontStyle(font_size=15))
    g_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = Label(form_frame, text='Password:', 
                           font=CustomFontStyle(font_size=15),
                           bg='white')
    password_label.grid(row=2, column=0, sticky='e', padx=10, pady=10)

    pass_entry = Entry(form_frame, bg='white', font=CustomFontStyle(font_size=15), show='*')
    pass_entry.grid(row=2, column=1, padx=10, pady=10)

    re_pass_label = Label(form_frame, text='Re-enter Password:', 
                          font=CustomFontStyle(font_size=15),
                          bg='white')
    re_pass_label.grid(row=3, column=0, sticky='e', padx=10, pady=10)

    re_pass_entry = Entry(form_frame, bg='white', font=CustomFontStyle(font_size=15), show='*')
    re_pass_entry.grid(row=3, column=1, padx=10, pady=10)

    def validate_and_submit():
        if pass_entry.get() != re_pass_entry.get():
            messagebox.showerror("Error", "Passwords do not match!")
        else:
            gmail = g_entry.get()
            password = pass_entry.get()
            print(gmail, password)
            insert_user_to_db = 'Insert Into Users(gmail, password) Values(%s,%s)'
            run_query(insert_user_to_db,(gmail, password))
            w.withdraw()
            messagebox.showinfo("Success", "Registration successful! Please login with that credential")


    login_btn = Button(form_frame, text='Sign up',
                       bg=background_color,
                       activebackground='white',
                       activeforeground='yellow',
                       font=CustomFontStyle(font_size=15),
                       command=validate_and_submit)
    login_btn.grid(row=4, column=0, columnspan=2, pady=20)

    w.mainloop()
