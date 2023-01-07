# Type Defs
from tkinter import ttk
# User Pre-defined Functions Import
from src.display import display


def delete(cursor, connection, box, Tree: ttk.Treeview):
    if not Tree.selection():
        box.showarning(
            'Warning!', 'Please select a record from the tree to delete!')
    else:
        rec = Tree.focus()
        values = Tree.item(rec)
        select = values['values']
        Tree.delete(rec)
        cursor.execute(f'DELETE FROM Shop WHERE Item_ID={select[0]}')
        connection.commit()
        box.showinfo('Success!', f'Deleted Record with ID: {select[0]}')
        display(cursor, Tree)
    return
