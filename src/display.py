from tkinter import ttk
import tkinter as T


def display(cursor, Tree: ttk.Treeview):
    Tree.delete(*Tree.get_children())
    cursor.execute('SELECT * FROM Shop')
    res = cursor.fetchall()
    for rec in res:
        Tree.insert('', T.END, values=rec)
    return
