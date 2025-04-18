#! /usr/bin/env python
# -*-coding: utf-8 -*-
""" View/window.py"""
##########
import tkinter as tk
import tkinter.ttk as ttk
import datetime

from View import select_sql as ss
from View import register

class select_list():
    def __init__(self):
        self.menu = ("Buy", "Mate", "Pregnancy", "Birth", "Wean", "Retire")
        self.sex = ("Any", "M", "F")
        self.state = ("Any", "B","M","P","W","R")
        #When you will add a new tg-line
        #change "def show_summary" and "def get_summary in select_sql"
        self.line = ("Any", "C57BL/6N", "GAD67-GFP","VGAT-Venus","VGAT-tdTomato", "VGAT-IRES-Cre", "Chat-IRES-Cre")
        self.genotype = ("wt", "+/-", "homo", "unknown")
        self.users = ("Any", "KASAI")
        self.results = ('Success', 'Fail')
lists = select_list()

class OpenWindow():
    def __init__(self, title, size):
        self.title = title
        self.size = size
        
    def main(self):
        root = tk.Tk()
        root.title(self.title)
        root.geometry(self.size)
        return root
        
    def sub(self):
        sub = tk.Toplevel()
        sub.title(self.title)
        sub.geometry(self.size)
        fc = close_sub(sub)
        sub.protocol("WM_DELETE_WINDOW", fc.close_fcn)
        return sub

class Frame(tk.LabelFrame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.configure(
            bd=2,
            relief="ridge",
            text=""
        )
        self.master = master
        self.configure(**kw)
        self.pack(fill="x")

    def create_event(self):
        # Main Menu Buttons
        callbacks = [new_buy_window, new_mate_window, new_pregnancy_window, new_birth_window, new_wean_window, retire_window]
        for i in range(0, len(lists.menu)):
            #lists is defined by select_list
            a = myButton(self, text=lists.menu[i], command=callbacks[i])
            a.grid(row=0, column=i)

    def create_search(self):
        # Main Search Menu
        a1 = myButton(self, text = "Show DB")
        a1.grid(row=0)

        a2 = myButton(self, text = "Save CSV")
        a2.grid(row=0, column=1)

        row1 = 1
        row2 = 2
        b1 = self.labeled_Entry("ID from: ", row1, 0, 12)
        b2= self.labeled_Entry("to: ", row1, 2)
        b3 = self.labeled_Entry("Birth from: ", 1, 4)
        b4 = self.labeled_Entry("to: ", row1, 6)
        b5 = self.labeled_List("sex", lists.sex, row2, 0, 0)
        b6 = self.labeled_List("status", lists.state, row2, 2, 0)
        b7 = self.labeled_List("Gene", lists.line, row2, 4, 0)
        b8 = self.labeled_List("User", lists.users, row2, 6, 0)

        return a1, b1, b2, b3, b4, b5, b6, b7, b8, a2

########## Main Menu Button Fcn ##########
    def new_buy(self):
        row=0
        row2=1
        b1 = self.labeled_Entry("Num Males: ", row, 0, 12)
        b1.insert(tk.END, "0")
        b2 = self.labeled_Entry("Num Females: ", row, 2, 15)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Birth Date: ", row, 4, 10)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b3.insert(tk.END, today_str)

        b4 = self.labeled_List("Gene: ", lists.line[1:], row2, 0, 0, 11)
        b5 = self.labeled_List("Genotype: ", lists.genotype, row2, 2, 0)
        b6 = self.labeled_List("User: ", lists.users[1:], row2, 4, 0)

        a = myButton(self, text="Register", width=12)
        a.grid(row = 2, column = 4)
        c = myButton(self, text="UnDo", width=12)
        c.grid(row = 2, column = 5)

        return a, b1, b2, b3, b4, b5, b6, c

    def new_mate(self):
        row=0
        b1 = self.labeled_Entry("Father ID: ", row, 0, 12, 5)
        b1.insert(tk.END, "0")
        b2 = self.labeled_Entry("Mother ID: ", row, 2, 12, 5)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Start Date: ", row, 4, 12)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b3.insert(tk.END, today_str)

        a = myButton(self, text="Register", width=12)
        a.grid(row = 1, column = 4)
        c = myButton(self, text="UnDo", width=12)
        c.grid(row = 1, column = 5)

        return a, b1, b2, b3, c

    def new_pregnancy(self):
        val = ss.get_unsuccess_id('pregnancy')
        b1 = self.labeled_List("Mate ID: ", val, 0, 0, 0)

        b2 = self.labeled_List("Results: ", lists.results, 0, 2, 0)

        a = myButton(self, text = "Register", width = 12)
        a.grid(row = 0, column = 4)
        c = myButton(self, text = "UnDo", width = 12)
        c.grid(row = 0, column = 5)

        return a, b1, b2, c
    
    def new_birth(self):
        row = 0
        row1 = 1
        val = ss.get_unsuccess_id('birth')
        b1 = self.labeled_List("Preg ID:", val, row, 0, 0)
        b2 = self.labeled_Entry("Num Male Pups:", row1, 0, 12, 4)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Num Female Pups:", row1, 2, 12, 4)
        b3.insert(tk.END, "0")
        b4 = self.labeled_Entry("Brith Day: ", row1, 4, 12)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b4.insert(tk.END, today_str)

        a = myButton(self, text = "Register", width = 12)
        a.grid(row = 2, column = 4)
        c = myButton(self, text = "UnDo", width = 12)
        c.grid(row = 2, column = 5)

        return a, b1, b2, b3, b4, c

    def new_wean(self):
        row = 0
        row1 = 1
        row2= 2
        val = ss.get_unsuccess_id('wean')
        b1 = self.labeled_List("Birth ID: ", val, row, 0, 0)
        b2 = self.labeled_Entry("Num Male Pups:", row1, 0, 15, 8)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Num Female Pups:", row1, 2, 15, 8)
        b3.insert(tk.END, "0")
        b4 = self.labeled_List("Gene: ", lists.line[1:], row1, 4, 0, 11)
        b5 = self.labeled_List("genotype: ", lists.genotype[0:], row2, 0, 0)
        b6 = self.labeled_List("Users: ", lists.users[1:], row2, 2, 0)

        a = myButton(self, text = "Register", width = 12)
        a.grid(row = row2, column = 4)
        c = myButton(self, text = "UnDo", width = 12)
        c.grid(row = row2, column = 5)

        return a, b1, b2, b3, b4, b5, b6, c

    def retire(self):
        row = 0
        b1 = self.labeled_Entry("ID from: ", row, 0, 12)
        b2 = self.labeled_Entry("to: ", row, 2)
        b3 = self.labeled_Entry("Retire date: ", row, 4, 12)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b3.insert(tk.END, today_str)

        a = myButton(self, text = "Register", width = 12)
        a.grid(row = 1, column = 4)
        c = myButton(self, text="UnDo", width = 12)
        c.grid(row = 1, column = 5)

        return a, b1, b2, b3, c

    def labeled_Entry(self, text, row, col, *args):
        if len(args) == 1:
            width1 = args[0]
            width2 = 8
        elif len(args)== 2:
            width1 = args[0]
            width2 = args[1]
        else:
            width1 = 8
            width2 = 8

        a = myLabel(self, text = text, width = width1)
        a.grid(row = row, column = col)
        a = myEntry(self, width = width2)
        a.grid(row = row, column = col+1)

        return a

    def labeled_List(self, text, val, row, col, n, *args):
        a = myLabel(self, text = text)
        a.grid(row = row, column = col)
        if len(args) == 1:
            a = myCombobox(self, width = args[0])
        else:
            a = myCombobox(self)

        a["values"] = val
        a.current(n)
        a.grid(row = row, column = col+1)
        
        return a

    def show_summary(self):
        s = ss.get_summary()
        t1 = """ {} (M) and {} (F) mice are 'B'. """.format(s[0], s[1])
        t2 = """ {} mice (F) are 'M'. """.format(s[2])
        t3 = """ {} mice (F) are 'P'. """.format(s[3])
        t4 = """ {} mice (F) are 'W'. """.format(s[4])
        t5 = """ Total {} mice are breeding now. """.format(s[5])
        t6 = """ {} mice were killed in this year""".format(s[6])
        t7 = """{}(WT), {}(GAD67-GFP), {}(V-Venus), {}(V-Tomato), {}(V-Cre) and {}(Chat-Cre) were killed""".format(s[7][0], s[7][1], s[7][2], s[7][3], s[7][4], s[7][5])

        txt1 = myLabel(self, text = t1)
        txt2 = myLabel(self, text = t2)
        txt3 = myLabel(self, text = t3)
        txt4 = myLabel(self, text = t4)
        txt5 = myLabel(self, text = t5)
        txt6 = myLabel(self, text = t6)
        txt7 = myLabel(self, text = t7)
        
        txt1.pack(fill = "x")
        txt2.pack(fill = "x")
        txt3.pack(fill = "x")
        txt4.pack(fill = "x")
        txt5.pack(fill = "x")
        txt6.pack(fill = "x")
        txt7.pack(fill = "x")
        
        return 1

    def show_db(self):
        tree = ShowDB(self, 20, 'buy')
        return tree

### Buttons ###
class myButton(tk.Button):
    """ Event Menu 用のボタン"""
    def __init__(self, master = None, cnf = {}, **kw):
        tk.Button.__init__(self, master, cnf, **kw)
        self.configure(
            font = ("", 12),
            width = 10
        )
        self.configure(**kw)

class myLabel(tk.Label):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        self.configure(
            font = ("", 12),
            width = 8
        )
        self.configure(**kw)

class myEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Entry.__init__(self, master, cnf, **kw)
        self.configure(
            font = ("", 12),
            width = 8
        )

class myCombobox(ttk.Combobox):
    def __init__(self, master=None, cnf={}, **kw):
        ttk.Combobox.__init__(self, master, **kw)
        self.configure(
            state = "readonly",
            width = 8)
        self.configure(**kw)

########## Window に DB テーブルの表示 ##########
class ShowDB():
    def __init__(self, master, n, which):
        self.master = master
        self.padding = n
        
        if which == "buy":
            self.tree = self.show_select()
        elif which == "mate":
            self.tree = self.show_mate()
        elif which == "pregnancy":
            self.tree = self.show_preg()
        elif which == "birth":
            self.tree = self.show_birth()
        elif which == "wean":
            self.tree = self.show_wean()
        elif which == "retire":
            self.tree = self.show_retire()

    def show(self, list_width, list_text):
        #空のテーブルを表示
        tree = ttk.Treeview(self.master, padding = self.padding)
        l = len(list_width)
        l_col = tuple(range(1, l+1))
        tree["column"] = l_col
        tree["show"] = "headings"

        for i in range(1, l+1):
            tree.column(i, width = list_width[i-1])
            tree.heading(i, text = list_text[i-1])
        tree.pack(fill = "x")
        return tree

    def show_select(self):
        list_width = (5, 5, 5, 10,10)
        list_text = ('ID','Sex','Status','BirthDay','Line', 'User')
        tree = self.show(list_width, list_text)
        return tree

    def show_mate(self):
        list_width = (10, 10, 10, 12, 12, 5)
        list_text = ('mate ID', 'Mother', 'Father', 'Start', 'End', 'Success')
        tree = self.show(list_width, list_text)
        return tree

    def show_preg(self):
        list_width = (10, 10, 10, 10)
        list_text = ('pregnancy ID', 'mate ID', 'Father','Mother')
        tree = self.show(list_width, list_text)
        return tree

    def show_birth(self):
        list_width = (10, 10, 10, 10, 10, 12)
        list_text = ('birth ID', 'preg ID', 'Mother', '#Male pups', '#Female pups', 'Birth Day')
        tree = self.show(list_width, list_text)
        return tree

    def show_wean(self):
        list_width = (10, 10, 10, 10, 5)
        list_text = ('wean ID', 'birth ID', 'Mother', '#Male pups', '#Female pups')
        tree = self.show(list_width, list_text)
        return tree

    def show_retire(self):
        list_width = (10, 10, 10, 12)
        list_text = ('ID','SEX','Status',' Retire date')
        tree = self.show(list_width, list_text)
        return tree

##### open sub window ###
def new_buy_window():
    sub = OpenWindow("New Buy", "900x300").sub()
    f = Frame(sub, text = "Select Menu")
    a = f.new_buy()
    a[0]["command"] = lambda:make_register(sub_tree.tree, a, "buy")
    sub_tree = ShowDB(sub, 20, "buy")

    a[-1]["command"] = lambda:ss.undo()
    return sub_tree

def new_mate_window():
    sub = OpenWindow("New Mate", "900x500").sub()
    f = Frame(sub, text = "Select Menu")
    a = f.new_mate()
    a[0]["command"] = lambda:make_register(sub_tree.tree, a, 'mate')
    sub_tree = ShowDB(sub, 20, "mate")

    a[-1]["command"] = lambda:ss.undo()

def new_pregnancy_window():
    sub = OpenWindow("New Pregnancy", "800x600").sub()
    f = Frame(sub, text = "Select Menu")
    a = f.new_pregnancy()
    a[0]["command"] = lambda:make_register(sub_tree.tree, a, 'pregnancy')
    sub_tree = ShowDB(sub, 20, "pregnancy")
    
    sub_tree2 = ShowDB(sub, 20, "mate")
    #ss.latest10(sub_tree2.tree, "pregnancy")
    #とりあえず全部出すように変更
    ss.latest_all(sub_tree2.tree, "pregnancy")
    a[-1]["command"] = lambda:ss.undo()

def new_birth_window():
    sub = OpenWindow("New Birth Event", "900x500").sub()
    f = Frame(sub, text = "Select Menu")
    a = f.new_birth()
    a[0]["command"] = lambda:make_register(sub_tree.tree, a, 'birth')
    sub_tree = ShowDB(sub, 20, "birth")

    sub_tree2 = ShowDB(sub, 20, "pregnancy")
    ss.latest10(sub_tree2.tree, "birth")
    a[-1]["command"] = lambda:ss.undo()

def new_wean_window():
    sub = OpenWindow("New Wean Event", "900x500").sub()
    f = Frame(sub, text = "Select Menu")
    a = f.new_wean()
    a[0]["command"] = lambda:make_register(sub_tree.tree, a, 'wean')
    sub_tree = ShowDB(sub, 20, "wean")
    sub_tree2 = ShowDB(sub, 20, "birth")
    ss.latest10(sub_tree2.tree, "wean")
    a[-1]["command"] = lambda:ss.undo()

def retire_window():
    sub = OpenWindow("Retire", "800x500").sub()
    f = Frame(sub, text = "Select Menu")
    a = f.retire()
    a[0]["command"] = lambda:make_register(sub_tree.tree, a, 'retire')
    sub_tree = ShowDB(sub, 20, "retire")
    a[-1]["command"] = lambda:ss.undo()

##### Register #####

def make_register(tree, a, which):
    # a = parames setting from subwindows
    r = register.make_record(which, a)
    # b = (last_i)
    b = r.register()
    ss.select_new(tree, b, which)

##### Window Close Object #####
class close_sub():
    def __init__(self, sub):
        self.sub = sub
    def close_fcn(self):
        ss.save()
        self.sub.destroy()

