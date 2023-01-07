# TypeDefs
from tkinter import IntVar, StringVar, ttk

# Pre Defined User Functions Import
from src.display import display
from src.reset import reset


def add(cursor, connection, id: IntVar, name: StringVar, price: IntVar, box, Tree: ttk.Treeview):
    xid = id.get()
    xname = name.get()
    xprice = price.get()
    if not xid or not xname or not xprice:
        box.showarning('Warning!', 'Please enter values')
    else:
        try:
            cursor.execute(
                f'INSERT INTO Shop VALUES ({xid}, "{xname}", {xprice})')
            connection.commit()
            box.showinfo('Success!', f'Added Record with ID: {xid}')
            display(cursor, Tree)
            reset(id, name, price)
            return
        except:
            box.showerror('Error!', 'Given values have an invalid type')
            return
