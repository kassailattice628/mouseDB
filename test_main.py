""" test 実行 """ 
from View import test as t
import tkinter as tk
import sqlite3

def main():
    root = tk.Tk()
    root.title = "test" 
    root.size = "800x600"

    f = tk.Frame(root)
    f.pack(fill="x")

    a = tk.Label(f, text="aaa")
    a.pack(side="left")

    e0 = tk.Entry(f)
    e0.insert(tk.END, "2")
    e0.pack(side="left")

    e1 = tk.Entry(f)
    e1.insert(tk.END, "1")
    e1.pack(side="left")

    e2 = tk.Entry(f)
    e2.insert(tk.END, "0")
    e2.pack(side="left")

    e3 = tk.Entry(f)
    e3.insert(tk.END, "181211")
    e3.pack(side="left")

    c = tk.Label(f, text="ccc")
    c.pack(side="left")

    p = [a, e0, e1, e2, e3, c]
    r = t.make_record("wean", p)
    r.register()

    root.mainloop()



if __name__ == '__main__':
    main()
    #Window

    #mate

    #preg

    #wean

    #birth