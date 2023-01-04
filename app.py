import tkinter as T
import mysql.connector as mysql
import tkinter.messagebox as err
from tkinter import ttk

# predefined user functions import
# from src.add import add

# main
fonts = {
    'head': ('Arial', 15, 'bold'),
    'label': ('Garamond', 14),
    'entry': ('Garamond', 12)
}

colors = {
    'left': '#b3b3cc',
    'center': '#c2c2d6',
    'head': '#6699ff',
    'right': 'Gray'
}

connection = mysql.connect(
    user='root', passwd='Darshan@101', database='chad', host='localhost')
cursor = connection.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS Shop (Item_ID INT PRIMARY KEY NOT NULL, Item_Name VARCHAR(64), Price INT)')

app = T.Tk()
app.title('Shop Management System')
app.geometry('1000x600')
app.resizable(False, False)

cursor.execute('SELECT * FROM Shop')
cursor.fetchall()
total = cursor.rowcount

id = T.IntVar(app)
name = T.StringVar(app)
price = T.IntVar(app)
id.set(total + 1)


def reset():
    for i in ['id', 'name', 'price']:
        exec(f'{i}.set("")')


def display():
    global Tree
    Tree.delete(*Tree.get_children())
    cursor.execute('SELECT * FROM Shop')
    res = cursor.fetchall()
    for rec in res:
        Tree.insert('', T.END, values=rec)


def add():
    xid = id.get()
    xname = name.get()
    xprice = price.get()
    if not xid or not xname or not xprice:
        err.showerror('Error', 'Missing (Empty) Fields')
    else:
        try:
            cursor.execute(
                f'INSERT INTO Shop VALUES ({xid}, "{xname}", {xprice})')
            connection.commit()
            err.showinfo('Success', f'Added Record (ID: {xid})')
            display()
            reset()
        except:
            err.showerror('Error', 'Given values have an invalid type')


def delete():
    global Tree
    if not Tree.selection():
        err.showerror('Error', 'Please select a record to delete')
    else:
        rec = Tree.focus()
        values = Tree.item(rec)
        select = values['values']
        Tree.delete(rec)
        cursor.execute(f'DELETE FROM Shop WHERE Item_ID={select[0]}')
        connection.commit()
        err.showinfo('Success', f'Deleted Record with ID = {select[0]}')
        display()


def openMod():
    global Tree
    rec = Tree.focus()
    if not rec:
        err.showerror(
            'Error', 'Please select a value from the tree to modify!')
        return
    mod = T.Tk()
    mod.geometry('400x250')
    mod.resizable(False, False)
    item = Tree.item(rec)
    val = item['values']
    mod.title(f'Modifying item: "{val[1]}"')
    mname = T.StringVar(mod)
    mprice = T.IntVar(mod)
    mname.set(val[1])
    mprice.set(int(val[2]))

    def modify():
        yname = mname.get()
        yprice = mprice.get()
        if not yname or not yprice:
            err.showerror('Error', 'Please enter values')
            return
        try:
            cursor.execute(f'DELETE FROM Shop WHERE Item_Id = {val[0]}')
            connection.commit()
            cursor.execute(
                f'INSERT INTO Shop VALUES ({val[0]}, "{yname}", {yprice})')
            connection.commit()
            err.showinfo('Success!', f'Modified Record with ID: {val[0]}')
            display()
            mod.destroy()
        except:
            err.showerror('Error', 'An unknown error occurred!')
            mod.destroy()
    T.Label(mod, text='New Name:', font=fonts['label']).pack(padx=10, pady=10)
    T.Entry(mod, width=20, textvariable=mname,
            font=fonts['entry']).pack(padx=10, pady=10)

    T.Label(mod, text='New Price:', font=fonts['label']).pack(padx=10, pady=10)
    T.Entry(mod, width=20, textvariable=mprice,
            font=fonts['entry']).pack(padx=10, pady=10)

    T.Button(mod, text='Submit', font=fonts['label'], bg='green', command=modify, width=20).pack(
        padx=10, pady=10)
    mod.update()
    mod.mainloop()


T.Label(app, text='Welcome to Shop Management System!',
        font=fonts['head'], bg=colors['head']).pack(side=T.TOP, fill=T.X)
LFrame = T.Frame(app, bg=colors['left'])
LFrame.place(x=0, y=30, relheight=1, relwidth=0.2)

CFrame = T.Frame(app, bg=colors['center'])
CFrame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

RFrame = T.Frame(app, bg=colors['right'])
RFrame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

T.Label(LFrame, text='Item ID', font=fonts['label'], bg=colors['left']).pack(
    padx=10, pady=10)
T.Entry(LFrame, width=19, textvariable=id,
        font=fonts['entry']).pack(padx=10, pady=10)

T.Label(LFrame, text='Name', font=fonts['label'], bg=colors['left']).pack(
    padx=10, pady=10)
T.Entry(LFrame, width=19, textvariable=name,
        font=fonts['entry']).pack(padx=10, pady=10)

T.Label(LFrame, text='Price', font=fonts['label'], bg=colors['left']).pack(
    padx=10, pady=10)
T.Entry(LFrame, width=19, textvariable=price,
        font=fonts['entry']).pack(padx=10, pady=10)

T.Button(LFrame, text='Reset',
         font=fonts['label'], command=reset).pack(padx=10, pady=10, fill=T.X)

T.Button(CFrame, text='Add',
         font=fonts['label'], command=add).pack(padx=10, pady=10, fill=T.X)
T.Button(CFrame, text='Delete',
         font=fonts['label'], command=delete).pack(padx=10, pady=10, fill=T.X)
T.Button(CFrame, text='Modify',
         font=fonts['label'], command=openMod).pack(padx=10, pady=10, fill=T.X)
T.Button(CFrame, text='Generate Bill',
         font=fonts['label'], ).pack(padx=10, pady=10, fill=T.X)

T.Label(RFrame, text='Shop Database',
        font=fonts['head'], bg='red').pack(side=T.TOP, fill=T.X)

Tree = ttk.Treeview(RFrame, height=100, selectmode=T.BROWSE,
                    columns=('Item ID', 'Name', 'Price'))
XScroll = T.Scrollbar(Tree, orient=T.HORIZONTAL, command=Tree.xview)
XScroll.pack(side=T.BOTTOM, fill=T.X)
YScroll = T.Scrollbar(Tree, orient=T.VERTICAL, command=Tree.yview)
YScroll.pack(side=T.RIGHT, fill=T.Y)

Tree.config(yscrollcommand=YScroll.set, xscrollcommand=XScroll.set)

Tree.heading('Item ID', text='ID', anchor=T.CENTER)
Tree.heading('Name', text='Name', anchor=T.CENTER)
Tree.heading('Price', text='Price', anchor=T.CENTER)

Tree.column('#0', width=0, stretch=T.NO)
Tree.column('#1', width=120, stretch=T.NO)
Tree.column('#2', width=200, stretch=T.NO)

Tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display()
app.update()
app.mainloop()
