""" sub window から parameter 取得して register したデータを消す """
import sqlite3
import tkinter import messagebox

def UnDo(which, w):
    conn = sqlite3.connect("mouseDB.sqlite3")
    c = conn.cursor()
    
    p = get_params(w)
    r = Execute(which, conn, c, p)

def get_params(w):
    p = []
    for i in range(1, len(w)-1):
        print(i)
        #p.append(i)
        p.append( w[i].get())
    return p

def Execute(which, conn, c, p):
    if which == "new":
        sql = """SELECT MAX(mouse_id) FROM individual"""
        c.execute(sql)
        r_e = int(c.fetchall()[0][0])
        p1 = int(p[0])
        p2 = int(p[1])
        r_s = r_e - p1 - p2 +1

        sql = """
            DELETE FROM individual WHERE mouse_id BETWEEN {} AND {};
            """.format(r_s, r_e)
        
        c.execute(sql)
        conn.commit()
        conn.close()
        return 1
    
    elif which == "mate":
        pass
    elif which == "pregnancy":
        pass
    elif which == "birth":
        pass
    elif which == "wean":
        pass
    else:
        res = messagebox.showwarning("Error", "CANNOT USE UNDO")
            print("showwarning", res)
            return 0






if __name__ == '__main__':
    UnDo("new", [1,3])
    #app.run()