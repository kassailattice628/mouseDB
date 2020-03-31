#! /usr/bin/env python
# -*-coding: utf-8 -*-

"""select_sql.py"""
##########
import datetime
import sqlite3
import pandas as pd
from tkinter import messagebox as mbox

#Connect DB
conn = sqlite3.connect("mouseDB.sqlite3")
c = conn.cursor()

#選択した条件でマウスを検索して表示
# <= mouseDB_App から
def show_selet(tree, w):
    sql = select_sql(w, 'show')
    tree.delete(*tree.get_children())
    Update_View(tree, sql)

def to_csv_select(tree, w):
    sql = select_sql(w, 'csv')
    
    #sqlite -> pandas df -> csv
    df = pd.read_sql_query(sql, conn)
    df = df.fillna(int(0))
    df = df.replace('M', 1)
    df = df.replace('F', 2)
    df.columns = ['id', 'sex', 'mom', 'dad']
    #df['mom'] = df['mom'].astype(int)
    #df['dad'] = df['dad'].astype(int)
    now = datetime.datetime.now()
    fname = '~/Desktop/df_{0:%y%m%d}.csv'.format(now)
    df.to_csv(fname)

def select_sql(w, t):
    id1= w[1].get()
    id2= w[2].get()
    bd1= w[3].get()
    bd2= w[4].get()
    sex= w[5].get()
    status= w[6].get()
    line= w[7].get()
    user= w[8].get()

    #ID
    if id1 == "" and id2 == "":
        cond1 = "1"
    elif id1 != ""  and id2 == "":
        cond1 = "mouse_id >= {}".format(id1)
    elif id1 == "" and id2 != "":
        cond1 = "mouse_id <= {}".format(id2)
    else:
        cond1 = "mouse_id BETWEEN {0} AND {1}".format(id1, id2)
    
    #Birth Day
    if bd1 == "" and bd2 == "":
        cond2 = "1"
    elif bd1 != ""  and bd2 == "":
        cond2 = "birth_date >= {}".format(bd1)
    elif bd1 == "" and bd2 != "":
        cond2 = "birth_date <= {}".format(bd2)
    else:
        cond2 = "birth_date BETWEEN {0} AND {1}".format(bd1,bd2)

    #SEX
    if sex == "Any":
        cond3 = "1"
    else:
        cond3 = 'sex = "{}"'.format(sex)
    #STATUS
    if status == "Any":
        cond4 = "1"
    else:
        cond4 = 'status = "{}"'.format(status)
    #GENE
    if line == "Any":
        cond5 = "1"
    else:
        cond5 = 'line = "{}"'.format(line)
    #USER 
    if user == "Any":
        cond6 = "1"
    else:
        cond6 = 'user = "{}"'.format(user)

    if t == 'show':
        #show in window
        sql1 ="""
        SELECT mouse_id, sex, status, birth_date, line, user"""
    
    elif t == 'csv':
        #csv (for kinship)
        sql1 ="""
        SELECT mouse_id, sex, mother_id, father_id"""
    
    sql = (sql1 + 
    """
    FROM individual
    WHERE {0} AND {1} AND {2} AND {3} AND {4} AND {5}
    ORDER BY mouse_id
    """.format(cond1, cond2, cond3, cond4, cond5, cond6))

    return sql
### END of "select_sql"

# <= window.py から
def get_unsuccess_id(which):
    if which == 'pregnancy':
        name_id = 'mate_id'
        sql = 'SELECT mate_id FROM mate WHERE success IS null'

    elif which == 'birth':
        name_id = 'preg_id'
        sql = 'SELECT preg_id FROM pregnancy WHERE success IS null'

    elif which == 'wean':
        name_id = 'birth_id'
        sql = 'SELECT h.birth_id FROM history h JOIN birth b ON h.birth_id = b.birth_id WHERE b.success IS 1 AND h.wean_id IS null ORDER BY h.birth_id'

    df = pd.read_sql_query(sql, conn)

    r = df[name_id].unique()
    r = [str(i) for i in r]
    if len(r) != 0:
        return r
    else:
        return ['None']
### END of "get_unsuccess_id"

########## 未設定のデータを表示 ##########
# <= window.py から
def select_new(tree, ind, which):
    if which == 'buy':
        i = ind[0] - ind[1] + 1
        print(ind)
        sql = """
        SELECT mouse_id, sex, status, line, user
        FROM individual
        WHERE mouse_id >= {}
        """.format( i )
        
    elif which == 'mate':
        sql = """
        SELECT mate_id, female_id, male_id, start_date, end_date, success
        FROM mate
        WHERE mate_id <= {}
        ORDER BY mate_id DESC
        """.format(ind+9)

    elif which == 'pregnancy':
        sql = """
        SELECT h.preg_id, h.mate_id, m.male_id, m.female_id
        FROM history h JOIN mate m ON h.mate_id = m.mate_id JOIN pregnancy p ON h.preg_id = p.preg_id
        WHERE h.mate_id <= {}
        ORDER BY p.preg_id DESC
        """.format(ind+9)
    
    elif which == 'pregnancy2':
        sql = 0
        print("mate end!")

    elif which == 'birth':
        sql = """
        SELECT h.birth_id, h.preg_id, m.female_id, b.num_pup_male, b.num_pup_female, b.birth_date
        FROM history h JOIN birth b ON h.birth_id = b.birth_id JOIN mate m ON h.mate_id = m.mate_id
        WHERE b.birth_id <= {}
        ORDER BY b.birth_id DESC
        """.format(ind+9)

    elif which == 'wean':
        if ind != 0:
            sql = """
            SELECT h.wean_id, h.birth_id, m.female_id, w.num_pup_male, w.num_pup_female
            FROM history h JOIN wean w ON h.wean_id = w.wean_id JOIN mate m ON h.mate_id = m.mate_id
            WHERE w.wean_id <= {}
            ORDER BY w.wean_id DESC
            """.format(ind+9)
        else:
            sql = 0
            print(" wean failure!")

    elif which == 'retire':
        #check id
        if ind != 0:
            sql = """
            SELECT mouse_id, sex, status, retire_date
            FROM individual
            WHERE mouse_id <= "{}" AND status = 'R'
            ORDER BY mouse_id DESC
            """.format(ind+9)
        else:
            sql = 0
            print(" no mice are selected!")
    #表示 
    if sql != 0:
        Update_View(tree, sql)

########## 最新 10 のデータを表示 ##########
# <= window.py から
def latest_all(tree, which):
    if which == "pregnancy":
        sql = """
        SELECT mate_id, female_id, male_id, start_date, end_date, success
        FROM mate WHERE success IS NULL
        """

    elif which == "birth":
        sql = """
        SELECT h.preg_id, h.mate_id, m.male_id, m.female_id
        FROM history h JOIN mate m ON h.mate_id = m.mate_id JOIN pregnancy p ON h.preg_id = p.preg_id
        WHERE p.success IS NULL
        """
    Update_View(tree, sql)

def latest10(tree, which):
    if which == "pregnancy":
        sql = """
        SELECT mate_id, female_id, male_id, start_date, end_date, success
        FROM mate
        WHERE success IS NULL AND mate_id >= (
            SELECT MAX(mate_id) from mate) -9
        """
        
    elif which == "birth":
        sql = """
        SELECT h.preg_id, h.mate_id, m.male_id, m.female_id
        FROM history h JOIN mate m ON h.mate_id = m.mate_id JOIN pregnancy p ON h.preg_id = p.preg_id
         
        WHERE p.success IS NULL AND p.preg_id >= (select MAX(preg_id) FROM pregnancy) - 9
        """

    elif which == "wean":
        sql = """
        SELECT h.birth_id, h.preg_id, m.female_id, b.num_pup_male, b.num_pup_female, b.birth_date
        FROM history h JOIN birth b ON h.birth_id = b.birth_id JOIN mate m ON h.mate_id = m.mate_id
        WHERE b.success IS 1 AND h.wean_id IS null
        ORDER BY h.birth_id
        """
    Update_View(tree, sql)

########## テーブルの update ##########
# select_new, latest10 から
def Update_View(tree, sql):
    tree.delete(*tree.get_children())
    i = 0
    for r in c.execute(sql):
        tree.insert("", "end", tags=i, values=r)
        if i & 1:
            tree.tag_configure(i, background="#CCFFFF")
        i += 1


### sub functions for make_record ###

########## UPDATE DB ##########
def add_new_records(n, sex, p):
    #n:num_pups, p:parameters, c:cursor
    for i in range(0, n):
        sql = """
        INSERT INTO individual (sex, line, genotype, birth_date, father_id, mother_id, user) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        c.execute(sql, (sex[i], p[0], p[1], p[2], p[3], p[4], p[5]))
    last_i = c.lastrowid
    return last_i

def add_new_mate(p):
    v1 = check_id(p[0:2])
    v2 = check_sex(p[0:2])
    if v1 == 0 or v2 == 0:
        return 0
    f_state = get_status(p[1])

    if f_state == 'B':
        #mate 登録
        sql = """
        INSERT INTO mate (male_id, female_id, start_date) values(?, ?, ?)
        """
        c.execute(sql, p)
        last_i = c.lastrowid
        #female state 変更
        change_state(p[1], 'M')
        add_to_history("mate_id", last_i)

        print("add a mate event")
        return last_i
    else:
        show_warn("status of id:'{}' is not 'B'".format(p[1]))
        return 0

def add_new_pregnancy(which, p):
    ids = find_mate_ids(which, p[0])
    print(p[1])
    
    if p[1] == 'Success':
        change_state(ids[2], 'P')
        make_success("mate", 1, "mate_id", p[0])

        sql = """
        INSERT INTO pregnancy DEFAULT VALUES
        """
        c.execute(sql)
        last_i = c.lastrowid
    
        add_to_history("preg_id", last_i,   mate_id = p[0])
        print("add a pregnancy event")

    elif p[1] == 'Fail':
        #update mate event to "fail"
        change_state(ids[2], 'B')
        make_success("mate", 0, "mate_id", p[0])
        last_i = 0

    return last_i

def add_new_birth(which, p):
    ids = find_mate_ids(which, p[0])

    make_success("pregnancy", 1, "preg_id", p[0])

    if int(p[1]) == 0 and int(p[2]) == 0:
        #出産後すぐ全滅の場合も 0, 0 にして B に戻す
        change_state(ids[2], 'B')
        success = 0
    else:
        change_state(ids[2], 'W')
        success = 1

    sql = """
    INSERT INTO birth (num_pup_male, num_pup_female, birth_date, success) VALUES (?, ?, ?, ?)
    """
    val = (p[1], p[2], p[3], success)
    c.execute(sql, val)
    last_i = c.lastrowid

    add_to_history('birth_id', last_i, mate_id = ids[0])

    print("add a birth event")
    return last_i

def add_new_wean(which, p):
    num_m = int(p[1])
    num_f = int(p[2])
    ids = find_mate_ids(which, p[0])
    bd = get_birthday(ids[0])
    #成功しても失敗しても B に戻す
    change_state(ids[2], 'B')

    if num_m == 0 and num_f == 0:
        success = 0
        print ("no mice wean")
    else:
        success = 1
    
    sql = """
    INSERT INTO wean (num_pup_male, num_pup_female, success) VALUES (?, ?, ?)
    """
    val = (p[1], p[2], success)
    c.execute(sql, val)
    last_i = c.lastrowid

    add_to_history('wean_id', last_i, mate_id = ids[0])

    #individual に登録
    if success == 1:
        num_i = num_m + num_f
        sex_str = ['M'] * num_m
        sex_str.extend(['F'] * num_f)
        params = (p[3], p[4], bd, ids[1], ids[2], p[5])
        last_i = add_new_records(num_i, sex_str, params)
        print('add a birth event')
    else:
        last_i = 0
    return last_i

def retire(p):
    if p[0] == '' or p[1] == '':
        show_warn('Please put ID in both FROM and TO fields!')
        return 0
    v1 = check_id(p[0:2])
    if v1 == 0:
        return 0
    ids = range(int(p[0]), int(p[1]) +1)
    for i in ids:
        s = get_status(i)
        if s != 'R':
            sql = """ 
            UPDATE individual SET retire_date = {} WHERE mouse_id = {}
            """.format(p[2], str(i))
            c.execute(sql)
            change_state(i, 'R')
        else:
            print('id:"{}" has already been set as "R".'.format(i))
    return int(p[1])

def add_to_history(which, i, mate_id = []):
    if which == 'mate_id':
        sql = """
        INSERT INTO history(mate_id) values("{}")
        """.format(i)
    else:
        sql = """
        UPDATE history SET "{}" = "{}" WHERE mate_id = "{}"
        """.format(which, i, mate_id)

    c.execute(sql)

def change_state(i, state):
    if state == "None":
        pass
    else:
        sql ="""
            UPDATE individual
            SET status = "{}"
            WHERE mouse_id = "{}"
        """.format(state, i)
        c.execute(sql)

def make_success(name_table, val, name_id, i):
    sql = """ 
    UPDATE "{}" SET success = "{}" WHERE "{}" = "{}"
    """.format(name_table, val, name_id, i)
    c.execute(sql)

########## serach ##########
def find_mate_ids(which, i):
    if which == 'pregnancy':
        name = 'mate_id'
    elif which == 'birth':
        name = 'preg_id'
    elif which == 'wean':
        name = 'birth_id'

    sql = """
    SELECT mate_id, male_id, female_id FROM mate WHERE mate_id = (
        SELECT mate_id FROM history WHERE {} = "{}")
    """.format(name, i)
    c.execute(sql)
    ans = c.fetchall()[0]
    return ans

def get_female_status(female_id):
    sql = """
    SELECT status FROM individual WHERE mouse_id = "{}"
    """.format(female_id)
    c.execute(sql)
    ans = c.fetchall()[0][0]
    return(ans)

def get_status(i):
    sql = """
    SELECT status FROM individual WHERE mouse_id = "{}"
    """.format(i)
    c.execute(sql)
    ans = c.fetchall()[0][0]
    return ans

def get_birthday(mate_id):
    sql = """
    SELECT birth_date FROM birth WHERE birth_id =
    (SELECT birth_id FROM history WHERE mate_id = "{}")
    """.format(mate_id)
    c.execute(sql)
    ans = c.fetchall()[0][0]
    return(ans)

######### validate ids ##########
def check_id(list_id):
    for i in (0, 1):
        sql = """
        SELECT mouse_id FROM individual WHERE mouse_id IN ("{}")
        """.format(list_id[i])
        c.execute(sql)
        ans = c.fetchall()
        if len(ans) == 0:
            show_warn("""mouse_id:"{}" is not in the DB!""".format(list_id[i]))
            return 0
    return 1

def check_sex(list_id):
    sex = ['M', 'F']
    for i in (0,1):
        if get_sex(list_id[i]) != sex[i]:
            show_warn("""sex of mouse_id:"{}" is not appropriate!""".format(list_id[i]))
            return 0
    return 1

def get_sex(i):
    sql = """
    SELECT sex FROM individual WHERE mouse_id = "{}"
    """.format(i)
    c.execute(sql)
    return c.fetchall()[0][0]

def get_summary():
    c1 = summary_sql("status = 'B' AND sex = 'M'")
    c2 = summary_sql("status = 'B' AND sex = 'F'")
    c3 = summary_sql("status = 'M'")
    c4 = summary_sql("status = 'P'")
    c5 = summary_sql("status = 'W'")
    c_all = summary_sql("status IS NOT 'R'")

    y = datetime.datetime.now()
    #DBでの西暦が2文字表記なので，調整
    if y.month <= 3:
        y1 = (y.year - 2000 - 1)*10000 + 401
        y2 = (y.year - 2000)*10000 + 331
    else:
        y1 = (y.year - 2000)*10000 + 401
        y2 = (y.year - 2000 + 1)*10000 + 331

    c_suc1 = summary_sql("""status = 'R' AND retire_date >= {} AND retire_date <= {}""".format(y1, y2))

    #c_suc_lines
    cs_l1 = summary_sql("""status = 'R' AND line = 'C57BL/6N' AND retire_date >= {} AND retire_date <= {}""".format(y1, y2))
    cs_l2 = summary_sql("""status = 'R' AND line = 'GAD67-GFP' AND retire_date >= {} AND retire_date <= {}""".format(y1, y2))
    cs_l3 = summary_sql("""status = 'R' AND line = 'VGAT-Venus' AND retire_date >= {} AND retire_date <= {}""".format(y1, y2))
    cs_l4 = summary_sql("""status = 'R' AND line = 'VGAT-tdTomato' AND retire_date >= {} AND retire_date <= {}""".format(y1, y2))
    cs_l5 = summary_sql("""status = 'R' AND line = 'VGAT-IRES-Cre' AND retire_date >= {} AND retire_date <= {}""".format(y1, y2))
    
    #number of suc for each line
    c_suc_each = [cs_l1, cs_l2, cs_l3, cs_l4, cs_l5]
 
    return [c1, c2, c3, c4, c5, c_all, c_suc1, c_suc_each] 

def summary_sql(condition):
    sql = """
    SELECT Count(mouse_id)
    FROM individual
    WHERE {}
    """.format(condition)
    c.execute(sql)
    ans = c.fetchall()[0][0]
    return ans


##########
def show_warn(text):
    res = mbox.showwarning("title", text)
    print("showwarning", res)
    return 0

##########
def save():
    print("save changes")
    conn.commit()

def undo():
    print("RollBack changes")
    conn.rollback()
    conn.commit()
    #Update_View