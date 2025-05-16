import tkinter as tk
from tkinter import ttk, messagebox
from model_connection import *
from project_config import *
import uuid
from datetime import datetime, date
from PIL import Image, ImageTk
from reports.year_report import generate_year_sales_report
from reports.month_report import generate_monthly_sales_report
from weekly_sales_report import generate_weekly_sales_report
        
#2025-02-23
#2025-04-10

stock_data = []

def get_updated_stock():
    stock_data.clear()  # Clear existing data to avoid duplicates
    result = run_query('select * from stock')
    if result:
        for i in result:
            stock_data.append(i)
            
def stock_app(logged_in_user):
    logged_in_user_details = logged_in_user
    root = tk.Toplevel()
    root.title("Zink Stationary Stock Management System")
    root.geometry("1100x700")
    root.configure(bg='#e6f2ff')

    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Treeview", background="white", foreground="black",
                    rowheight=25, fieldbackground="white", font=('Helvetica', 10))
   
    style.configure("Treeview.Heading",
                background="#007acc",  # Blue background
                foreground="white",    # White text
                font=('Helvetica', 10, 'bold'))
    
    style.map("Treeview.Heading",
          relief=[('active', 'groove'), ('pressed', 'sunken')])
    
    style.configure("TNotebook.Tab",
                    background="#cce6ff",
                    foreground="black",
                    font=('Helvetica', 10, 'bold'),
                    padding=[10, 5])
    style.map("TNotebook.Tab",
              background=[("selected", "#007acc")],
              foreground=[("selected", "white")])

    header_frame = tk.Frame(root, bg='#4da6ff')
    header_frame.pack(fill='x')

    title_label = tk.Label(header_frame, text="Zink Stationary Stock Management System", font=CustomFontStyle(font_size=15, weight='bold'),
                           bg='#4da6ff', fg='white')
    title_label.pack(side='left', padx=20, pady=10)

    logged_in_user_name = logged_in_user_details[1].split('@')[0]
    user_label = tk.Label(header_frame, text=f"Logged in as: {logged_in_user_name}", font=CustomFontStyle(font_size=12),
                          bg='#4da6ff', fg='white')
    user_label.pack(side='right', padx=20)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    # ======== Stocks Tab ========
    stocks_tab = tk.Frame(notebook, bg='#e6f2ff')
    notebook.add(stocks_tab, text='Stocks')

    tk.Label(stocks_tab, text="Available Stocks", bg='#e6f2ff',
             font=CustomFontStyle(font_size=16, weight='bold')).pack(pady=10)

    stock_tree = ttk.Treeview(stocks_tab, columns=("Item Code","Item", "Quantity", "Price", "Edit", "Delete"), show='headings', height=10)
    for col in ("Item Code","Item", "Quantity", "Price", "Edit", "Delete"):
        stock_tree.heading(col, text=col)
        stock_tree.column(col, width=100 if col not in ["Edit", "Delete"] else 60, anchor='center')


    stock_tree.pack(padx=20, pady=10, fill='x')

    # Tag configurations for row colors
    stock_tree.tag_configure('alert', background='#EDA0A0')
    def refresh_stock_table():
        get_updated_stock()
        for row in stock_tree.get_children():
            stock_tree.delete(row)
        for index, item in enumerate(stock_data):
            tag = '' 
            if item[2]<=10:
                tag='alert'
            print()
            stock_tree.insert('', 'end', values=(*item, '✏', '🗑'), tags=(tag,))

    def on_row_click(event):
        region = stock_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = stock_tree.identify_column(event.x)
        row_id = stock_tree.identify_row(event.y)

        if not row_id:
            return

        values = stock_tree.item(row_id)['values']
        item_code = values[0]

        if column == "#5":  # Edit column
            item_name, quantity, price = values[1], values[2], values[3]
            item_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            item_entry.insert(0, item_name)
            quantity_entry.insert(0, quantity)
            price_entry.insert(0, price)

            # Change Add button to Update behavior
            def update_stock():
                updated_item = item_entry.get()
                updated_quantity = quantity_entry.get()
                updated_price = price_entry.get()
                if updated_item and updated_quantity.isdigit() and updated_price.replace('.', '', 1).isdigit():
                    query = f'UPDATE stock SET item_name=%s, quantity=%s, price=%s WHERE id="{item_code}"'
                    run_query(query, data_to_insert=(updated_item, int(updated_quantity), float(updated_price)))
                    refresh_stock_table()
                    update_reports()
                    update_item_dropdown()
                    item_entry.delete(0, tk.END)
                    quantity_entry.delete(0, tk.END)
                    price_entry.delete(0, tk.END)
                    update_btn.config(text="Add Stock", command=add_stock)
                    add_frame.config(text='Add New Stock')

            update_btn.config(text="Update Stock", command=update_stock)
            add_frame.config(text='Update Existing Stock')


        elif column == "#6":  # Delete column
            confirm = messagebox.askyesno("Confirm Delete", f"Delete item '{values[1]}'?")
            if confirm:
                run_query(f'DELETE FROM stock WHERE id="{item_code}"', update_to_db=True)
                refresh_stock_table()
                # update_reports()
                # update_item_dropdown()


    stock_tree.bind("<Button-1>", on_row_click)

    add_frame = tk.LabelFrame(stocks_tab, text="Add New Stock", font=('Helvetica', 14, 'bold'),
                              bg='white', padx=20, pady=20)
    add_frame.pack(pady=20, padx=20, fill='x')

    tk.Label(add_frame, text="Item Name:", bg='white', font=('Helvetica', 11)).grid(row=0, column=0, padx=10, pady=10)
    item_entry = ttk.Entry(add_frame, font=('Helvetica', 11), width=25)
    item_entry.grid(row=0, column=1)

    tk.Label(add_frame, text="Quantity:", bg='white', font=('Helvetica', 11)).grid(row=0, column=2, padx=10, pady=10)
    quantity_entry = ttk.Entry(add_frame, font=('Helvetica', 11), width=25)
    quantity_entry.grid(row=0, column=3)

    tk.Label(add_frame, text="Price:", bg='white', font=('Helvetica', 11)).grid(row=0, column=4, padx=10, pady=10)
    price_entry = ttk.Entry(add_frame, font=('Helvetica', 11), width=25)
    price_entry.grid(row=0, column=5)
    
    def clear_values_to_update():
        item_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        update_btn.config(text='Add Stock')
        add_frame.config(text='Add New Stock')
        return 0
    
    cancel_btn = tk.Button(add_frame, text="Cancel", 
                       bg=background_color,
                       activebackground='white',
                       activeforeground='yellow',
                       font=CustomFontStyle(font_size=10),
                       command=clear_values_to_update)
    cancel_btn.grid(row=0, column=7, padx=10)
    def add_stock():
        item = item_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()
        if item and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            insert="Insert into stock(item_name, quantity, price) values(%s,%s,%s)"
            run_query(insert, data_to_insert=(item, int(quantity), float(price)))
            result = run_query('select * from stock')
            if len(stock_data):
                stock_data.clear()
            for i in result:
                stock_data.append(i)
            item_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            refresh_stock_table()
            update_reports()
            update_item_dropdown()
        else:
            messagebox.showerror("Invalid Input", "Enter valid name, quantity, and price.")

    update_btn = tk.Button(add_frame, text="Add Stock", 
                       bg=background_color,
                       activebackground='white',
                       activeforeground='yellow',
                       font=CustomFontStyle(font_size=10),
                       command=add_stock)
    update_btn.grid(row=0, column=6, padx=10)


    # ======== Memo Tab ========
    memo_tab = tk.Frame(notebook, bg='#e6f2ff')
    notebook.add(memo_tab, text='Memo')

    memo_frame = tk.LabelFrame(memo_tab, text="Generate Cash Memo", font=('Helvetica', 14, 'bold'),
                           bg='white', padx=5, pady=5)
    memo_frame.pack(pady=20, padx=20, fill='x')

    tk.Label(memo_frame, text="Select Item:", bg='white', font=('Helvetica', 11)
             ).grid(row=0, column=0, sticky='w', padx=(5, 2), pady=5)

    selected_item = tk.StringVar()
    item_dropdown = ttk.Combobox(memo_frame, textvariable=selected_item, font=('Helvetica', 11),
                             width=20, state='readonly')
    item_dropdown.grid(row=0, column=1, sticky='w', padx=(2, 5), pady=5)

    tk.Label(memo_frame, text="Quantity:", bg='white', font=('Helvetica', 11)
    ).grid(row=0, column=2, sticky='w', padx=(5, 2), pady=5)

    quantity_input = ttk.Entry(memo_frame, font=('Helvetica', 11), width=10)
    quantity_input.grid(row=0, column=3, sticky='w', padx=(2, 5), pady=5)

    purchase_items = []

    def add_to_purchase_list():
        item_name = selected_item.get()
        qty_str = quantity_input.get()

        if not item_name or not qty_str.isdigit():
            messagebox.showerror("Invalid Input", "Please select item and enter valid quantity.")
            return

        qty = int(qty_str)
        index = 0
        for item in stock_data:
            if item[1] == item_name:
                if qty > item[2]:
                    messagebox.showerror("Stock Error", "Not enough stock available.")
                    return
                total = qty * item[3]
                purchase_items.append([index,item_name, item[3], qty, total])
                index+=1
                refresh_purchase_table()
                return

    def refresh_purchase_table():
        memo_tree.delete(*memo_tree.get_children())
        for idx, (_, item, price, qty, total) in enumerate(purchase_items, start=1):
            memo_tree.insert('', 'end', values=(idx, item, f"₹{price:.2f}", qty, f"₹{total:.2f}",'✏', '🗑'))
    
    def generate_memo():
        if not purchase_items:
            messagebox.showwarning("No Items", "Add at least one item to generate memo.")
            return
        memo_id = int(str(uuid.uuid4().int)[:5])
        total_amount = sum(item[4] for item in purchase_items)
        memo_text = f"========== CASH MEMO {memo_id} ==========\n"
        for _,item, price, qty, total in purchase_items:
            insert_query="Insert into sales(memo_id,item_name,price,quantity,total_amount) values(%s, %s, %s, %s, %s)"
            run_query(insert_query, data_to_insert=(memo_id,item,price,qty,total))
            run_query(f'update stock set quantity=quantity-{qty} where item_name="{item}"',
                      update_to_db=True)
            print(item,qty,price,total)
            memo_text += f"{item:15} x {qty:<3} @ ₹{price:<7.2f} = ₹{total:.2f}\n"
        memo_text += "----------------------------------------\n"
        memo_text += f"TOTAL BILL: ₹{total_amount:.2f}\n"
        memo_text += "========================================\n"

        messagebox.showinfo("Memo Generated", memo_text)
       
        purchase_items.clear()
        memo_edit_frame.pack_forget()
        refresh_purchase_table()

    tk.Button(memo_frame, text="Add items to purchase list",
          bg=background_color,
          activebackground='white',
          activeforeground='yellow',
          command=add_to_purchase_list).grid(row=0, column=4, padx=(10, 5), pady=5)

    tk.Button(memo_frame, text="Generate Memo",
          bg=background_color,
          activebackground='white',
          activeforeground='yellow',
          command=generate_memo).grid(row=0, column=5, padx=(5, 10), pady=5)

    # Purchase Items Table
    memo_tree = ttk.Treeview(memo_tab, columns=("S.No", "Item", "Price", "Qty", "Total",'Edit','Delete'), show='headings')
    for col in ("S.No", "Item", "Price", "Qty", "Total",'Edit','Delete'):
        memo_tree.heading(col, text=col)
        memo_tree.column(col, width=100 if col not in ["Edit", "Delete"] else 60, anchor='center')
    memo_tree.pack(padx=20, pady=20, fill='x')

    def update_item_dropdown():
        item_dropdown['values'] = [item[1] for item in stock_data]
    
    memo_edit_frame = tk.LabelFrame(memo_tab, text="Edit Purchase Items", font=('Helvetica', 14, 'bold'),
                           bg='white', padx=5, pady=5)
    item_index_want_updated_quantity = 0
    def on_row_click(event):
        region = memo_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = memo_tree.identify_column(event.x)
        row_id = memo_tree.identify_row(event.y)

        if not row_id:
            return

        values = memo_tree.item(row_id)['values']
        item_code = values[0]

        if column == "#6":  # Edit column
            nonlocal item_index_want_updated_quantity 
            item_index_want_updated_quantity = values[0]-1
            if not edited_quantity.get().strip() == '':
                edited_quantity.delete(0,tk.END)    
            edited_quantity.insert(0,values[3])
            memo_edit_frame.pack(padx=10, pady=10, fill='x')


        elif column == "#7":  # Delete column
            confirm = messagebox.askyesno("Confirm Delete", f"Delete item '{values[1]}'?")
            if confirm:
                purchase_items.pop(item_code-1)
                refresh_purchase_table()

    print(purchase_items)
    memo_tree.bind("<Button-1>", on_row_click) 

    tk.Label(memo_edit_frame, text="Quantity:", bg='white', font=('Helvetica', 11)
    ).grid(row=0, column=0)

    edited_quantity = ttk.Entry(memo_edit_frame, font=('Helvetica', 11), width=10)
    edited_quantity.grid(row=0, column=1, sticky='w', padx=(2, 5), pady=5)

    def change_quantity():
        e_quan = edited_quantity.get()
        purchase_items[item_index_want_updated_quantity][3] = int(e_quan)
        purchase_items[item_index_want_updated_quantity][4] = purchase_items[item_index_want_updated_quantity][2] * int(e_quan)
        print(item_index_want_updated_quantity)
        print(purchase_items[item_index_want_updated_quantity])
        refresh_purchase_table()
        memo_edit_frame.place_forget()
    
    def cancel_quantity_edit():
        memo_edit_frame.pack_forget()
        edited_quantity.delete(0, tk.END)
        
    tk.Button(memo_edit_frame, text="Change quantity",
          bg=background_color,
          activebackground='white',
          activeforeground='yellow',
          command=change_quantity).grid(row=0, column=4, padx=(10, 5), pady=5)
    tk.Button(memo_edit_frame, text="Cancel change",
          bg=background_color,
          activebackground='white',
          activeforeground='yellow',
          command=cancel_quantity_edit).grid(row=0, column=5, padx=(10, 5), pady=5)
    # ======== Report Tab ========
    report_tab = tk.Frame(notebook, bg='#e6f2ff')
    notebook.add(report_tab, text='Report')

    report_frame = tk.LabelFrame(report_tab, text="Inventory Report", font=('Helvetica', 14, 'bold'),
                                 bg='white', padx=20, pady=20)
    report_frame.pack(pady=30, padx=30, fill='x')

    total_items_label = tk.Label(report_frame, text="Total Items: 0", font=('Helvetica', 12), bg='white')
    total_items_label.pack(pady=10)

    total_value_label = tk.Label(report_frame, text="Total Inventory Value: ₹0", font=('Helvetica', 12), bg='white')
    total_value_label.pack(pady=10)

    report_sales = tk.LabelFrame(report_tab, text="Sales Report", font=('Helvetica', 14, 'bold'),
                                 bg='white', padx=20, pady=20)
    report_sales.pack(pady=30, padx=30, fill='x')
    
    def generate_sales_report():
        generate_year_sales_report()
        generate_monthly_sales_report()
        generate_weekly_sales_report()


    import os
    if os.path.exists('year_sales.jpg') and os.path.exists('month_sales.jpg') and os.path.exists('weekly_sales_report.jpg'):
        year_sales_chart = Image.open('year_sales.jpg').resize((450, 300))
        year_sales_chart_tk = ImageTk.PhotoImage(year_sales_chart)
        report_sales.year_image = year_sales_chart_tk 

        month_sales_chart = Image.open('month_sales.jpg').resize((450, 300))
        month_sales_chart_tk = ImageTk.PhotoImage(month_sales_chart)
        report_sales.month_image = month_sales_chart_tk 

        weekly_sales_chart = Image.open('weekly_sales_report.jpg').resize((450, 300))
        weekly_sales_chart_tk = ImageTk.PhotoImage(weekly_sales_chart)
        report_sales.week_image = weekly_sales_chart_tk 
        
         # Display Yearly Sales Chart
        year_label = tk.Label(report_sales, image=report_sales.year_image, bg='white')
        year_label.pack(side='left', padx=10, pady=10)

        # Display Monthly Sales Chart
        month_label = tk.Label(report_sales, image=report_sales.month_image, bg='white')
        month_label.pack(side='left', padx=10, pady=10)

        # Display Weekly Sales Chart
        week_label = tk.Label(report_sales, image=report_sales.week_image, bg='white')
        week_label.pack(side='left', padx=10, pady=10)

    else:
        tk.Label(report_sales, text="Couldn't generate report", 
                 font=CustomFontStyle(font_size=10, weight='bold')).pack()

    def update_reports():
        total_items = len(stock_data)
        total_value = sum(qty * price for _, _, qty, price in stock_data)
        total_items_label.config(text=f"Total Items: {total_items}")
        total_value_label.config(text=f"Total Inventory Value: ₹{total_value:.2f}")

    # ======== Settings Tab ========
    settings_tab = tk.Frame(notebook, bg='#e6f2ff')
    notebook.add(settings_tab, text='Settings')

    settings_frame = tk.LabelFrame(settings_tab, text="User Settings", font=('Helvetica', 14, 'bold'),
                                   bg='white', padx=20, pady=20)
    settings_frame.pack(pady=40, padx=40, fill='x')

    tk.Label(settings_frame, text="Gmail:", font=('Helvetica', 11), bg='white').grid(row=0, column=0, padx=10, pady=10)
    name_entry = ttk.Entry(settings_frame, font=('Helvetica', 11), width=30)
    name_entry.insert(0, logged_in_user_details[1])
    name_entry.grid(row=0, column=1)

    tk.Label(settings_frame, text="Password:", font=('Helvetica', 11), bg='white').grid(row=1, column=0, padx=10, pady=10)
    email_entry = ttk.Entry(settings_frame, font=('Helvetica', 11), width=30)
    email_entry.insert(0, logged_in_user_details[2])
    email_entry.grid(row=1, column=1)

    def save_settings():
        nonlocal logged_in_user_details   
        new_email = name_entry.get().strip()
        new_password = email_entry.get().strip()
        if new_email and new_password:
            is_name_changed = new_email != logged_in_user_details[1]
            is_password_changed = new_password != logged_in_user_details[2]
            message_label = ''

            if is_name_changed or is_password_changed:
                if is_name_changed:
                    result = run_query(f'Update Users Set gmail="{new_email}" where id={logged_in_user_details[0]}', update_to_db=True,
                                       reterival_id=logged_in_user_details[0])
                    
                    logged_in_user_details = result[0]
                    message_label += 'Gmail '
                if is_password_changed:
                    result = run_query(f'Update Users Set password="{new_password}" where id={logged_in_user_details[0]}', update_to_db=True,
                                       reterival_id=logged_in_user_details[0])
                    logged_in_user_details = result[0]
                    message_label += 'Password '
                
                new_name = logged_in_user_details[1].split('@')[0]
                user_label.config(text=f"Logged in as: {new_name}")
                messagebox.showinfo("Success", f"User {message_label} updated successfully.")
        else:
            messagebox.showerror("Invalid Input", "Both fields are required.")

    tk.Button(settings_frame, text="Save Changes", command=save_settings,
               bg=background_color,
                   activebackground='white',
                   activeforeground='yellow',
                   ).grid(row=2, column=1, pady=20)

    # refresh_stock_table()
    # #update_reports()
    # update_item_dropdown()

    def on_tab_change(event):
        notebook = event.widget
        selected_tab = notebook.select()
        tab_index = notebook.index(selected_tab)
        if tab_index==0:
            refresh_stock_table()
        elif tab_index==1:
            update_item_dropdown()
        elif tab_index==2:
            refresh_stock_table()
            update_reports()
            generate_sales_report()

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)
    root.mainloop()
#stock_app((1,'user','pass','pass'))
