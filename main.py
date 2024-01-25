# PRODUCT ENTRY

# libraries:
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sv_ttk                  # theme: dark, light, sprites-dark, sprites-light
import mysql.connector

import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# root:
root = tk.Tk()
root.title("Product Entry")

# set appearance:
style = ttk.Style(root)
sv_ttk.set_theme("light")  


# ----------------------------------------------------------------------------------------
# connect to mysql
# made it global connection
try:
    print('Connecting to mysql database...')
    
    # config:
    config = {
        'user': 'root',
        'passwd': 'hilarypvenc',
        'host': 'localhost',
        'port': 3306,
        'database': 'store'
    }
    database = mysql.connector.connect(**config)    # connect to databse
    cursor = database.cursor()                      # set cursor

    print('Successfully connected to database!')

except mysql.connector.Error as err:
    print('Error! Trouble connecting to database.')
    print('Error: ', err)
    
    messagebox.showwarning('Connection Error!', f'Trouble connecting to database. \nError: {err}')

# ----------------------------------------------------------------------------------------
# global variables:
col_names = ['Product ID', 'Name', 'Category', 'Price']     # used in treeview headings
# ----------------------------------------------------------------------------------------
# functions

def load_data():
    try:
        print('Loading data to treeview from database...')

        # add the headings:
        for heading in col_names:                   # col names is a global library :)
            treeview.heading(heading, text=heading)

        # get the products:
        
        # fetch query:
        fetch_data = '''
            SELECT id, name, category, price FROM products
            WHERE removed = 0;
        '''
        cursor.execute(fetch_data)
        rows = cursor.fetchall()            # save the retrieved data to 'rows'

        # display data to treeview:
        for row in rows:
            treeview.insert('', 'end', values=row)
    
    except mysql.connector.Error as err:
        print('Error! Trouble retrieving data from database.')
        print('Error: ', err)
        
        messagebox.showwarning('Retrieve Error!', f'Trouble retrieving data from database. \nError: {err}')
    
    finally:
        database.commit()           # commit



# get functions:
def get_data(query):            # get data from query
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        messagebox.showwarning(
            title='Parse Data Error!', 
            message=f'Failed to parse Data!\nError: {err}'
        )

def get_pdtotal():
    # get data:
    query = '''
        SELECT COUNT(*) AS total_products FROM products
        WHERE removed = 0;
    '''
    data = get_data(query)
    
    data = data[0][0]               # fetch the data that is returned as a list of tuple
    print('Total Data: ', data)
    return str(data)

def get_pdadded():      # method to extract the newest added product 
    # get data:
    query = '''
        SELECT name FROM products
        WHERE removed = 0
        ORDER BY date_added DESC
        LIMIT 1;
    '''
    data = get_data(query)
    data = data[0][0]
    print('Newly Added: ', data)
    return str(data)

def get_pdmostexpensive():      # method to extact the most expensive product
    # get the data:
    query = '''
        SELECT name, price FROM products
        WHERE removed = 0
        ORDER BY price DESC
        LIMIT 1;
    '''

    data =  get_data(query)
    pdname = data[0][0]
    pdprc = data[0][1]

    data = [pdname, pdprc]
    print('Most expensive data: ', data)

    return data

def bar_vis():      # data visual of the distribution of products per category\
    try:
        # get data:
        query = '''
            SELECT category, COUNT(id) as Products
            FROM products
            WHERE removed = 0
            GROUP BY category;
        '''
        data = get_data(query)
        # print(data)


        # VISUALIZE!
        # convert dataframe:
        df = pd.DataFrame(data, columns=['Category', '# Products'])
        print(df)

        # create the bar chart:
        global bar_canvas
        bar_fig, ax = plt.subplots(figsize=(6, 4))

        bar_fig.set_facecolor('none')       # remove background
        bar_fig.set_alpha(0)
        ax.patch.set_facecolor('none')
        ax.patch.set_alpha(0)

        ax.bar(df['Category'], df['# Products']) # x,y
        ax.set_title('Product Distribution by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('# of Products')    

        bar_canvas = FigureCanvasTkAgg(bar_fig, master=chartframe)
        bar_canvas.draw()       # similar to plt.show() but for tkinteer
        bar_canvas.get_tk_widget().pack(expand=True)
    
    except mysql.connector.Error as err:
        messagebox.showwarning(
            'Error!', 
            message=f'Unable to create visuals. \nError: {err}'
        )

    finally:
        plt.close(bar_fig)

# refreshes all the visualization
def refresh():
    bar_canvas.get_tk_widget().destroy()      # destroy the canvas
    get_pdtotal()
    get_pdmostexpensive()
    get_pdadded()
    bar_vis()
# bind for TREEVIEW:
def on_select(event):
    global selected_list
    selected_list = []

    # save the selected:
    selected_item = treeview.selection()
    
    if selected_item:   # if an item is selected.
        selected_list = list(treeview.item(selected_item, 'values'))
    
    print('Selected row: ', selected_list)
    
# get product:
def add_product():

    global popup, pdid_entry, pdname_entry, pdcat_entry, pdprice_entry

    # create a label:
    popup = tk.Toplevel()
    popup.title('Add Product')
    #popup.geometry('400x350')

    frame = ttk.LabelFrame(popup,text='Add New Product', labelanchor='ns')
    frame.pack(padx=10, pady=20, fill='both')
    
    # create prompt:
    pdid_label = ttk.Label(frame, text='ID: ')
    pdid_label.grid(row=1, column=0, sticky='news')
    pdid_entry = ttk.Entry(frame, text='Product ID')
    pdid_entry.grid(row=1, column=1, sticky='nsew')

    pdname_label = ttk.Label(frame, text='Name: ')
    pdname_label.grid(row=2, column=0, sticky='nsew')
    pdname_entry = ttk.Entry(frame)
    pdname_entry.grid(row=2, column=1, sticky='nsew')

    category_list = ['Technology', 'School Supplies', 'Accessories', 'Miscellaneous']
    pdcat_label = ttk.Label(frame, text='Category: ')
    pdcat_label.grid(row=3, column=0, sticky='nsew')
    pdcat_entry  = ttk.Combobox(frame, values=category_list, state='readonly')
    pdcat_entry.grid(row=3, column=1, sticky='nsew')
    pdcat_entry.set(category_list[0])       # set default value

    pdprice_label = ttk.Label(frame, text='Price (PhP): ')
    pdprice_label.grid(row=4, column=0)
    pdprice_entry = ttk.Entry(frame)
    pdprice_entry.grid(row=4, column=1)

    separator = ttk.Separator(frame)
    separator.grid(
        row=5, column=0, columnspan=2, sticky='nsew',
        pady=10
    )

    # confirm button:
    pd_button = ttk.Button(frame, text='ADD PRODUCT', command=insert_product)
    pd_button.grid(
        row=6, column=0, columnspan=2, sticky='nsew',
        pady=(5, 5)
    )

# button functions:
def insert_product():

    try:
        print('Inserting Product...')

        product_data = [pdid_entry.get(), pdname_entry.get(), pdcat_entry.get(), pdprice_entry.get()]    
        print('product data: ', product_data)

        if '' in product_data:
            messagebox.showwarning(title='Input Error!', message='ID, Name, Category, and Price cannot be empty.')
        elif not product_data[-1].replace('.','', 1).isdigit():
            messagebox.showwarning(title='Input Error!', message='Price contains string.')
        else:
            # add to database:
            query = '''
                INSERT INTO products (id, name, category, price)
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(query, product_data)
            database.commit()

            # add to display:
            treeview.insert('', tk.END, values=product_data)

            # refresh viz
            refresh()

    except mysql.connector.Error as err:
         messagebox.showwarning('Error!', f'Error in inserting the product or product value.\nError: {err}')
    
    finally:
        popup.destroy()

def delete_product():
    # confirm removing data:
    confirm = messagebox.askquestion(title='Product Removal', message='Confirm to remove product?')
    
    if confirm:
        try:
            print('Removing selected: ', selected_list)

            # remove data from sql:
            query = '''
                UPDATE products
                SET
                    removed = 1,
                    date_added = CURRENT_TIMESTAMP
                WHERE
                    id = %s AND
                    name = %s AND
                    category = %s AND
                    price = %s
                ;
            '''
            cursor.execute(query, selected_list)
            database.commit()

            # remove data from treeview:
            treeview.delete(treeview.selection())

            print(f'Data {selected_list} has been deleted.')

            # refresh data, visualizations, etc.:
            refresh()  

        except mysql.connector.Error as err:
            messagebox.showwarning('Error!', f'Error in deleting the product.\nError: {err}')
    else:
        pass

def update_product():

    if treeview.selection():
        global popup, new_pdid_entry, new_pdname_entry, new_pdcat_entry, new_pdprice_entry

        # create a label:
        popup = tk.Toplevel()
        popup.title('Update Product')
        #popup.geometry('400x350')

        frame = ttk.LabelFrame(popup,text='Update Product', labelanchor='ns')
        frame.pack(padx=10, pady=20, fill='both')
        
        # create prompt:
        pdid_label = ttk.Label(frame, text='ID: ')
        pdid_label.grid(row=1, column=0, sticky='news')
        new_pdid_entry = ttk.Entry(frame)
        new_pdid_entry.grid(row=1, column=1, sticky='nsew')

        pdname_label = ttk.Label(frame, text='Name: ')
        pdname_label.grid(row=2, column=0, sticky='nsew')
        new_pdname_entry = ttk.Entry(frame)
        new_pdname_entry.grid(row=2, column=1, sticky='nsew')

        category_list = ['Technology', 'School Supplies', 'Accessories', 'Miscellaneous']
        pdcat_label = ttk.Label(frame, text='Category: ')
        pdcat_label.grid(row=3, column=0, sticky='nsew')
        new_pdcat_entry  = ttk.Combobox(frame, values=category_list, state='readonly')
        new_pdcat_entry.grid(row=3, column=1, sticky='nsew')
        new_pdcat_entry.set(category_list[0])       # set default value

        pdprice_label = ttk.Label(frame, text='Price (PhP): ')
        pdprice_label.grid(row=4, column=0)
        new_pdprice_entry = ttk.Entry(frame)
        new_pdprice_entry.grid(row=4, column=1, sticky='nsew')

        separator = ttk.Separator(frame)
        separator.grid(
            row=5, column=0, columnspan=2, sticky='nsew',
            pady=10
        )

        # confirm button:
        pd_button = ttk.Button(frame, text='UPDATE PRODUCT', command=update_data)
        pd_button.grid(
            row=6, column=0, columnspan=2, sticky='nsew',
            pady=(5, 5)
        )
    else:
        messagebox.showerror(title='Error!', message='No Value Selected.')

def update_data():
    try:
        print('Updating Product...')

        product_data = [new_pdid_entry.get(), new_pdname_entry.get(), new_pdcat_entry.get(), new_pdprice_entry.get()]    
        print('product data: ', product_data)

        if '' in product_data:
            messagebox.showwarning(title='Input Error!', message='ID, Name, Category, and Price cannot be empty.')
        elif not product_data[-1].replace('.','', 1).isdigit():
            messagebox.showwarning(title='Input Error!', message='Price contains string.')
        else:
            
            # add to database:
            query = '''
                UPDATE products 
                SET 
                    id = %s, 
                    name = %s, 
                    category = %s, 
                    price = %s
                WHERE 
                    id = %s AND
                    name = %s AND
                    category = %s AND
                    price = %s
                ;
            '''
            new_query = product_data + selected_list  # selected list is the old data 
            cursor.execute(query, new_query)
            database.commit()

            # change/update the selected value in treeview:
            selected = treeview.focus()
            if selected:
                treeview.item(selected, values=product_data)
            
            # refresh viz
            refresh()

    except mysql.connector.Error as err:
         messagebox.showwarning('Error!', f'Error in updating the product or product value.\nError: {err}')
    
    finally:
        popup.destroy()



# ----------------------------------------------------------------------------------------
# TITLE FRAME:
titleframe = ttk.Frame(root)
titleframe.grid(
    row=0, column=0, columnspan=3, sticky='news',
    padx=10, pady=20
)    

# title frame: title label:
title_label = ttk.Label(titleframe, text='Product Information', font=('Arial Black', 14))
title_label.pack()


# MAIN FRAME:
mainframe = ttk.Frame(root)
mainframe.grid(row=1, column=0,sticky='news')


# MAINFFRAME: TREEVIEW
treeframe = ttk.LabelFrame(mainframe, text='Product Table')
treeframe.grid(
    row=0, column=0, sticky='news',
    padx=10, pady=(0, 10)
)

# treeframe: scrollbar
tree_scroll = ttk.Scrollbar(treeframe, orient='vertical')

# treeframe: treeview
treeview = ttk.Treeview(
    treeframe, show='headings',
    yscrollcommand=tree_scroll.set,
    columns=col_names,
    height=20
)
treeview.bind('<<TreeviewSelect>>', on_select)        # bind the selection of rows in treeview on select

# treeframe: treeview: set/customize width(styles)
treeview.column(col_names[0], width=80)
treeview.column(col_names[1], width=120)
treeview.column(col_names[2], width=120)
treeview.column(col_names[3], width=120)

# add treeview to the frame
treeview.grid(
    row=0, column=0, sticky='nsew',
    padx=(10, 0), pady=5   
)
# load the data:
load_data()

# configure the scrollbar:
tree_scroll.grid(
    row=0, column=1, sticky='nsew',
    padx=(0,10), pady=5   
)
tree_scroll.config(command=treeview.yview)


# treeframe: buttonframe
buttonframe = ttk.Frame(treeframe)
buttonframe.grid(
    row=1, column=0, columnspan=2, sticky='news',
    padx=10, pady=5    
)

# treeframe: buttonframe: insert, update, remove
in_button = ttk.Button(buttonframe, text='INSERT', command=add_product, width=13)
#in_button.pack( padx=5, pady=(10, 5), fill='both')
in_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

up_button = ttk.Button(buttonframe, text='UPDATE', command=update_product, width=13)
#up_button.pack(padx=5, pady=5, fill='both')
up_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

del_button = ttk.Button(buttonframe, text='DELETE', command=delete_product, width=13)
#del_button.pack( padx=5, pady=5, fill='both')
del_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')


# VISUALIZATION
visframe = ttk.LabelFrame(root, text='DATA VISUALIZATION', labelanchor='ns')
visframe.grid(row=1, column=2, sticky='nsew')

# visframe: dataframe:
data_frame = ttk.Frame(visframe)
data_frame.grid(row=0, column=0)

# visframe: dataframe: total products, recently added, most expensive
pdtotal_label = ttk.Label(data_frame, text='Total Products: '+get_pdtotal().title(), font=('Arial', 10, 'bold'))
pdtotal_label.grid(
    row=0, column=0, sticky='news',
    padx=5, pady=5
)
pdnew_label = ttk.Label(data_frame, text='Newly Added: '+get_pdadded().title(), font=('Arial', 10, 'bold'))
pdnew_label.grid(
    row=0, column=1, sticky='nsew',
    padx=5, pady=5
)

pdmax_label = ttk.Label(data_frame, text='Most Expensive: '+str(get_pdmostexpensive()[0]).title(), font=('Arial', 10, 'bold'))
pdmax_label.grid(
    row=1, column=0, sticky='nsew',
    padx=5, pady=5
)
pdmax_amount_label = ttk.Label(data_frame, text='Php '+str(get_pdmostexpensive()[1]), font=('Arial', 10, 'bold'))
pdmax_amount_label.grid(
    row=1, column=1, sticky='nsew',
    padx=5, pady=5
)

# visframe: chart frame
chartframe = ttk.Frame(visframe)
chartframe.grid(
    row=2, column=0,
    padx=10, pady=20   
)

# visframe: chartframe: add vis()
bar_vis()


# -------------------------------------------------------------------------------------
# Lock the window size to its current size
width = root.winfo_width()
height = root.winfo_height()
root.minsize(width, height)
root.maxsize(width, height)

# run code
root.eval('tk::PlaceWindow . center')       # always show the mainwindow at the center of the screen
root.mainloop() #  run mainloop:
print('Closing database...')
cursor.close()
database.close()
print('Database has been closed...')
print('Program has been terminated.')
