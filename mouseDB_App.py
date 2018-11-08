#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" mouseDB App """
import sys
from View import window
from View import select_sql
import tkinter as tk

class mouseDB_App():
    def __init__(self):
        self.run()

    def run(self):
        #main Window
        root = window.OpenWindow("MOUSE DB_KASAI", "800x550").main()

        #Frame0
        f0 = window.Frame(root, text="Event Menu")
        f0.create_event()
        #Frame1
        f1 = window.Frame(root, text="Search Menu")
        a = f1.create_search()
        a[0]["command"]=lambda:select_sql.select_sql(tree.tree, a)
        #DB View
        f2 = window.Frame(root, text="Table")
        tree = f2.show_db() 
        #tree = window.ShowDB(root, 20, "buy")

        # Frame3
        f3 = window.Frame(root, text="Summary")
        f3.show_summary()

        # start app
        root.mainloop()


########## MAIN ##########
if __name__ == '__main__':
    app = mouseDB_App()
    #app.run()