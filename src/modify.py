import tkinter as T
from tkinter import ttk

from config import fonts
from src.display import display


def modify(cursor, connection, box, Tree: ttk.Treeview):
    rec = Tree.focus()
    if not rec:
        box.showerror(
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
    def Mod():
        yname = mname.get()
        yprice = mprice.get()
        if not yname or not yprice:
            box.showerror('Error', 'Please enter values')
            return
        try:
            cursor.execute(f'DELETE FROM Shop WHERE Item_Id = {val[0]}')
            connection.commit()
            cursor.execute(
                f'INSERT INTO Shop VALUES ({val[0]}, "{yname}", {yprice})')
            connection.commit()
            box.showinfo('Success!', f'Modified Record with ID: {val[0]}')
            display(cursor, Tree)
            return mod.destroy()
        except:
            box.showerror('Error', 'An unknown error occurred!')
            return mod.destroy()    
    T.Label(mod, text='New Name:', font=fonts['label']).pack(padx=10, pady=10)
    T.Entry(mod, width=20, textvariable=mname,
            font=fonts['entry']).pack(padx=10, pady=10)

    T.Label(mod, text='New Price:', font=fonts['label']).pack(padx=10, pady=10)
    T.Entry(mod, width=20, textvariable=mprice,
            font=fonts['entry']).pack(padx=10, pady=10)

    T.Button(mod, text='Submit', font=fonts['label'], bg='green', command=Mod, width=20).pack(
        padx=10, pady=10)
    mod.update()
    mod.mainloop()
    return