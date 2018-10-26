""" sub window から parameter 取得して register したデータを消す """
import sqlite3
from tkinter import messagebox

def UnDo(which, w):
    conn = sqlite3.connect("mouseDB.sqlite3")
    c = conn.cursor()
    
    p = get_params(w)
    sql = make_sql(which, c, conn, p)
    Execute(sql, conn, c)

def get_params(w):
    p = []
    for i in range(1, len(w)-1):
        p.append( w[i].get()) 
    return p

def make_sql(which, c, conn, p):
    if which == "new":
        sql = delete_new_individuals(c, conn, p)
        return sql
    
    elif which == "mate":
        #autoincrement を 1 戻す
        reset_sequence(which, c, conn, 1)
        reset_status(which, c, conn)
        #最新の mate_id を消す
        delete_new(which, "mate_id", c, conn)
        return 0

    elif which == "pregnancy":
        reset_sequence(which, c, conn, 1)
        #mother の status を 'M' に戻す
        reset_status(which, c, conn)
        #mate の succsee を null に戻す
        reset_success("mate", "mate_id", c, conn, p)
        delete_new(which, "preg_id", c, conn)
        return 0

    elif which == "birth":
        reset_sequence(which, c, conn, 1)
        reset_status(which, c, conn)
        reset_success("pregnancy", "preg_id", c, conn, p)
        reset_success(which, "birth_id", c, conn, p)
        delete_new(which, "birth_id", c, conn)
        return 0

    elif which == "wean":
        reset_sequence(which, c, conn, 1)
        reset_status(which, c, conn)
        reset_success(which, "wean_id", c, conn, p)
        delete_new(which, "wean_id", c, conn)
        sql = delete_new_individuals(c, conn, p)
        return sql

    elif which == "retire":
        pass
    ### END OF 

#########
def delete_new(table, id_, c, conn):
    sql = """DELETE FROM {0} WHERE {1} =
        (SELECT MAX({2}) FROM {3})""".format(table, id_, id_, table)
    c.execute(sql)
    conn.commit()

def delete_new_individuals(c, conn, p):
    #individual に新しく登録した mouse_id を計算
    sql = """SELECT MAX(mouse_id) FROM individual"""
    c.execute(sql)
    n_end = int(c.fetchall()[0][0])
    n = int(p[0]) + int(p[1])
    n_start = n_end - n + 1

    #autoincrement も reset
    reset_sequence("individual", c, conn, n)

    #individual から該当する mouse_id を delete
    sql = """
        DELETE FROM individual WHERE mouse_id BETWEEN {} AND {};
        """.format(n_start, n_end)
    return sql

def reset_success(table, id_, c, conn, p):
    #p[0] が 選択した id のはずなので
    sql = """
        UPDATE {0} SET success = null WHERE {1} = {2}
        """.format(table, id_, p[0])

    c.execute(sql)
    conn.commit()


def reset_status(table, c, conn):
    #motherの状態を B に戻す
    if table == "mate":
        sql = """UPDATE individual SET status = 'B' WHERE mouse_id = 
            (SELECT female_id FROM mate WHERE mate_id = 
            (SELECT MAX(mate_id) FROM mate))"""

    elif table == "pregnancy":
        sql = """UPDATE individual SET status = 'M' WHERE mouse_id = 
            (SELECT female_id FROM mate WHERE mate_id =
            (SELECT mate_id FROM pregnancy WHERE preg_id =
            (SELECT MAX(preg_id) FROM pregnancy)))"""

    elif table == "birth":
        sql = """UPDATE individual SET status = 'P' WHERE mouse_id = 
            (SELECT female_id FROM mate WHERE mate_id =
            (SELECT mate_id FROM pregnancy WHERE preg_id =
            (SELECT preg_id FROM birth WHERE birth_id = 
            (SELECT MAX(birth_id) FROM birth))))"""

    elif table == "wean":
        sql = """UPDATE individual SET status = 'W' WHERE mouse_id = 
            (SELECT female_id FROM mate WHERE mate_id =
            (SELECT mate_id FROM pregnancy WHERE preg_id =
            (SELECT preg_id FROM birth WHERE birth_id =
            (SELECT birth_id FROM wean WHERE wean_id =
            (SELECT MAX(wean_id) FROM wean)))))"""

    c.execute(sql)
    conn.commit()

def reset_sequence(name, c, conn, n):
    #reset_sequence("individual", c, conn, n)
    sql = """
        SELECT seq FROM sqlite_sequence WHERE name = "{}"
        """.format(name)
    c.execute(sql)
    seq_now = int(c.fetchall()[0][0])
    seq_ori = seq_now - n
    sql = """
        UPDATE sqlite_sequence SET seq = "{}" WHERE name = "{}"
        """.format(seq_ori, name)
    c.execute(sql)
    conn.commit()

def Execute(sql, conn, c):
    if sql != 0:
        c.execute(sql)
        conn.commit()
        conn.close()
        return 1

if __name__ == '__main__':
    UnDo("new", [1,3])
    #app.run()