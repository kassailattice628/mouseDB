""" View/window.py"""
##########
import tkinter as tk
import tkinter.ttk as ttk
import datetime

from View import select_sql as ss

class select_list():
    def __init__(self):
        self.menu = ("Buy", "Mate", "Pregnancy", "Birth", "Wean", "Retire")
        self.sex = ("", "M", "F")
        self.state = ("", "B","M","P","W","R")
        self.line = ("", "C57BL/6N", "GAD67-GFP","VGAT-Venus","VGAT-tdTomato")
        self.genotype = ("wt", "+/-", "-/-", "unknown")
        self.users = ("", "KASAI")
lists = select_list()

def OpenWindow():
    root = tk.Tk()
    root.title("MOUSE DB_KASAI")
    root.geometry("800x500")
    return root

### Frame ###
class Frame(tk.LabelFrame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.configure(
            bd=2,
            relief="ridge",
            text=""
        )
        self.configure(**kw)
        self.pack(fill="x")

    #Frame 設定
    def create_event(self):
        #texts = ["Buy", "Mate", "Pregnancy", "Birth", "Wean", "Retire"]
        callbacks = [new_buy_window, new_mate_window, new_pregnancy_window, new_birth_window, new_wean_window, retire_window]
        for i in range(0,6):
            a = myButton(self, text=lists.menu[i], command=callbacks[i])
            a.grid(row=0, column=i)

    def create_search(self):
        #show Button
        a = myButton(self, text="Show DB")
        a.grid(row=0)
        row1 = 1
        row2 = 2
        #ID, Birthday Entry
        b1 = self.labeled_Entry("ID from: ", row1, 0, 12)
        b2= self.labeled_Entry("to: ", row1, 2)
        b3 = self.labeled_Entry("Birth from: ", 1, 4)
        b4 = self.labeled_Entry("to: ", row1, 6)

        b5 = self.labeled_List("sex", lists.sex, row2, 0, 0)

        b6 = self.labeled_List("status", lists.state, row2, 2, 0)

        b7 = self.labeled_List("Gene", lists.line, row2, 4, 0)
        
        b8 = self.labeled_List("User", lists.users, row2, 6, 0)
        return a, b1, b2, b3, b4, b5, b6, b7, b8

    def new_buy(self):
        """
        new male mice, new female mice, status="B", BirthDay,
        line, genotype, userを入力させる
        """
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

        b4 = self.labeled_List("Gene: ", lists.line[1:], row2, 0, 0)

        b5 = self.labeled_List("Genotype: ", lists.genotype, row2, 2, 0)

        b6 = self.labeled_List("User: ", lists.users[1:], row2, 4, 0)

        a = myButton(self, text="Register", width=12)
        a.grid(row=2, column=5)

        #showDB
        return a, b1, b2, b3, b4, b5, b6

    def new_mate(self):
        """ new mate event
        add new record in mate DB
        select mother and father
        line, genotype, userを入力させる
        """
        row=0
        b1 = self.labeled_Entry("Father ID: ", row, 0, 12, 5)
        b1.insert(tk.END, "0")
        b2 = self.labeled_Entry("Mother ID: ", row, 2, 12, 5)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Start Date: ", row, 4, 12)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b3.insert(tk.END, today_str)

        a = myButton(self, text="Register", width=15)
        a.grid(row=1, column=6)
        return a, b1, b2, b3

    def new_pregnancy(self):
        #Drop list にする
        #SQL で Mate success の success が null の mate_id を取り出す 
        val = ss.Get_unsuccess_id('pregnancy')
        b1 = self.labeled_List("Mate ID: ", val, 0, 0, 0)

        a = myButton(self, text="Register", width=15)
        a.grid(row=0, column=4)
        return a, b1
    
    def new_birth(self):
        #Drop list で Pregnancy 選ばせる
        #pup の数（male, female), birth_date を登録する
        row = 0
        row1= 1
        val = ss.Get_unsuccess_id('birth')
        b1 = self.labeled_List("Preg ID:", val, row, 0, 0)
        b2 = self.labeled_Entry("Num Male Pups:", row1, 0, 12, 4)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Num Female Pups:", row1, 2, 12, 4)
        b3.insert(tk.END, "0")
        b4 = self.labeled_Entry("Brith Day: ", row1, 4, 12)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b4.insert(tk.END, today_str)

        a = myButton(self, text = "Register", width=12)
        a.grid(row=1, column=6)
        return a, b1, b2, b3, b4

    def new_wean(self):
        row = 0
        row1 = 1
        val = ss.Get_unsuccess_id('wean')
        b1 = self.labeled_List("Wean ID: ", val, row, 0, 0)
        b2 = self.labeled_Entry("Num Male Pups:", row1, 0, 15, 8)
        b2.insert(tk.END, "0")
        b3 = self.labeled_Entry("Num Female Pups:", row1, 2, 15, 8)
        b3.insert(tk.END, "0")
        b4 = self.labeled_List("Gene: ", lists.line[1:],  row1, 4, 1)
        b5 = self.labeled_List("genotype: ", lists.genotype[0:],  row1, 4, 0)
        b6 = self.labeled_List("Users: ", lists.users[1:],  2, 0, 0)

        a = myButton(self, text = "Register", width=12)
        a.grid(row=2, column=5)
        return a, b1, b2, b3, b4, b5, b6

    def retire(self):
        row = 0
        b1 = self.labeled_Entry("ID from: ", row, 0, 12)
        b2= self.labeled_Entry("to: ", row, 2)
        b3 = self.labeled_Entry("END date: ", row, 4, 12)
        today = datetime.datetime.today()
        today_str=today.strftime('%y%m%d')
        b3.insert(tk.END, today_str)

        a = myButton(self, text = "Register", width=12)
        a.grid(row=1, column=5)
        return a, b1, b2, b3

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

        a = myLabel(self, text=text, width=width1)
        a.grid(row=row, column=col)
        a = myEntry(self, width=width2)
        a.grid(row=row, column=col+1)
        return a

    def labeled_List(self, text, val, row, col, n):
        a = myLabel(self, text=text)
        a.grid(row=row, column=col)
        a = myCombobox(self)
        a["values"] = val
        a.current(n)
        a.grid(row=row, column=col+1)
        return a

### Buttons ###
class myButton(tk.Button):
    """ Event Menu 用のボタン"""
    def __init__(self, master=None, cnf={}, **kw):
        tk.Button.__init__(self, master, cnf, **kw)
        self.configure(
            font=("",12),
            width=10
        )
        self.configure(**kw)

class myLabel(tk.Label):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Label.__init__(self, master, cnf, **kw)
        self.configure(
            font=("",12),
            width=8
        )
        self.configure(**kw)

class myEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Entry.__init__(self, master, cnf, **kw)
        self.configure(
            font=("",12),
            width=8
        )

class myCombobox(ttk.Combobox):
    def __init__(self, master=None, cnf={}, **kw):
        ttk.Combobox.__init__(self, master, **kw)
        self.configure(
            state="readonly", 
            width=8)
        self.configure(**kw)

#### DataBase ####
class ShowDB():
    def __init__(self, master, n, which):
        self.master=master
        self.padding=n
        
        if which == "new":
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
        tree = ttk.Treeview(self.master, padding=self.padding)
        l = len(list_width)
        l_col = tuple(range(1, l+1))
        tree["column"] = l_col
        tree["show"]="headings" 

        for i in range(1, l+1):
            tree.column(i, width=list_width[i-1])
            tree.heading(i, text=list_text[i-1])
        tree.pack(fill="x")
        return tree

    def show_select(self):
        list_width = (10, 10, 10, 30)
        list_text = ('ID','SEX','Status','Gene')
        tree = self.show(list_width, list_text)
        return tree

    def show_mate(self):
        list_width = (10, 10, 10, 12, 12, 5)
        list_text = ('mate ID', 'Mother', 'Father', 'Start', 'End', 'Success')
        tree = self.show(list_width, list_text)
        return tree

    def show_preg(self):
        list_width = (10, 10, 5)
        list_text = ('pregnancy ID', 'mate ID', 'Success')
        tree = self.show(list_width, list_text)
        return tree

    def show_birth(self):
        list_width = (8, 8, 10, 10, 12, 5)
        list_text = ('birth ID', 'preg ID', 'Male pups', 'Female pups', 'Birth Day', 'Success')
        tree = self.show(list_width, list_text)
        return tree

    def show_wean(self):
        list_width = (10, 10, 10, 10, 5)
        list_text = ('wean ID', 'birth ID', 'Male pups', 'Female pups','Success')
        tree = self.show(list_width, list_text)
        return tree

    def show_retire(self):
        list_width = (10, 10, 10, 12)
        list_text = ('ID','SEX','Status','END date')
        tree = self.show(list_width, list_text)
        return tree

#### create subwindow ###

def SubWindow(title, geometry):
    sub=tk.Toplevel()
    sub.title(title)
    sub.geometry(geometry)
    return sub

##### open sub window ###
def new_buy_window():
    sub = SubWindow("New Buy", "700x300")
    f=Frame(sub, text="Select Menu")
    a = f.new_buy()
    a[0]["command"] = lambda:register(sub_tree.tree, a)
    sub_tree = ShowDB(sub, 20, "new")
    return sub_tree

def new_mate_window():
    sub = SubWindow("New Mate", "700x500")
    f=Frame(sub, text="Select Menu")
    a = f.new_mate()
    a[0]["command"] = lambda:register_mate(sub_tree.tree, a)
    sub_tree = ShowDB(sub, 20, "mate")
    print("open new_mate")

def new_pregnancy_window():
    sub = SubWindow("New Pregnancy", "700x500")
    f = Frame(sub, text="Select Menu")
    a = f.new_pregnancy()
    a[0]["command"] = lambda:register_pregnancy(sub_tree.tree, a)
    sub_tree = ShowDB(sub, 20, "pregnancy")
    
    sub_tree2 = ShowDB(sub, 20, "mate")
    ss.latest10(sub_tree2.tree, "pregnancy")
    print("open new_pregnancy")

def new_birth_window():
    sub = SubWindow("New Birth Event", "700x500")
    f = Frame(sub, text="Select Menu")
    a = f.new_birth()
    a[0]["command"] = lambda:register_birth(sub_tree.tree, a)
    sub_tree = ShowDB(sub, 20, "birth")

    sub_tree2 = ShowDB(sub, 20, "pregnancy")
    ss.latest10(sub_tree2.tree, "birth")
    print("open new_birth")

def new_wean_window():
    sub = SubWindow("New Wean Event", "700x500")
    f = Frame(sub, text="Select Menu")
    a = f.new_wean()
    a[0]["command"] = lambda:register_wean(sub_tree.tree, a)
    sub_tree = ShowDB(sub, 20, "wean")
    sub_tree2 = ShowDB(sub, 20, "birth")
    ss.latest10(sub_tree2.tree, "wean")
    print("open new_wean")

def retire_window():
    sub = SubWindow("Retire", "700x500")
    f = Frame(sub, text="Select Menu")
    a = f.retire()
    a[0]["command"] = lambda:register_retire(sub_tree.tree, a)
    sub_tree = ShowDB(sub, 20, "retire")
    print("open retire")

##### Register #####
def register(tree, a):
    b = ss.make_new_records(a)
    ss.select_new_sql(tree, a, b)

def register_mate(tree, a):
    b = ss.make_new_mate(a)
    ss.select_new_mate_sql(tree, a, b)
    
def register_pregnancy(tree, a):
    b = ss.make_new_preg(a)
    ss.select_new_preg_sql(tree, a, b)
    
def register_birth(tree, a):
    b = ss.make_new_birth(a)
    ss.select_new_birth_sql(tree, a, b)
    
def register_wean(tree, a):
    b = ss.make_new_wean(a)
    ss.select_new_wean_sql(tree, a, b)

def register_retire(tree, a):
    b = ss.make_retire(a)
    if b != 0:
        ss.select_retire_sql(tree, a, b)

