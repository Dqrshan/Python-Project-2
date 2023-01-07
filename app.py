import tkinter as T
import mysql.connector as mysql
import tkinter.messagebox as box
from tkinter import ttk

# pre defined fns import
from src.add import add
from src.delete import delete
from src.display import display
from src.modify import modify
from src.reset import reset
from src.bill import bill
from config import fonts, colors

connection = mysql.connect(
    user='root', passwd='', database='myfirstdb', host='localhost')
cursor = connection.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS Shop (Item_ID INT PRIMARY KEY NOT NULL, Item_Name VARCHAR(64), Price INT)')

app = T.Tk()
app.title('Shop Management System')
app.geometry('1000x600')
app.resizable(False, False)

id = T.IntVar(app)
name = T.StringVar(app)
price = T.IntVar(app)
def refresh():
    cursor.execute('SELECT * FROM Shop')
    cursor.fetchall()
    total = cursor.rowcount
    return id.set(total + 1)

def Add():
    global Tree
    add(cursor, connection, id, name, price, box, Tree)
    refresh()


def Delete():
    global Tree
    delete(cursor, connection, box, Tree)
    refresh()


def Modify():
    global Tree
    modify(cursor, connection, box, Tree)
    refresh()


def Reset():
    reset(id, name, price)
    refresh()

def Bill():
    bill(cursor)


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
         font=fonts['label'], command=Reset).pack(padx=10, pady=10, fill=T.X)

T.Button(CFrame, text='Add',
         font=fonts['label'], command=Add).pack(padx=10, pady=10, fill=T.X)
T.Button(CFrame, text='Delete',
         font=fonts['label'], command=Delete).pack(padx=10, pady=10, fill=T.X)
T.Button(CFrame, text='Modify',
         font=fonts['label'], command=Modify).pack(padx=10, pady=10, fill=T.X)
T.Button(CFrame, text='Generate Bill', command=Bill,
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

refresh()
display(cursor, Tree)

app.update()
app.mainloop()
