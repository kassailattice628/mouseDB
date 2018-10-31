"""select_sql.py"""
##########
import sqlite3
import pandas as pd
from tkinter import messagebox as mbox

#Connect DB
conn = sqlite3.connect("mouseDB.sqlite3")
c = conn.cursor()

#選択した条件でマウスを検索して表示
# <= mouseDB_App から
def select_sql(tree, w):
    tree.delete(*tree.get_children())
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

    sql ="""
    SELECT mouse_id, sex, status, birth_date, line, user
    FROM individual
    WHERE {0} AND {1} AND {2} AND {3} AND {4} AND {5}
    ORDER BY mouse_id
    """.format(cond1, cond2, cond3, cond4, cond5, cond6)

    Update_View(tree, sql)
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
    print(n)
    print(sex)
    print(p)
    for i in range(0, n):
        sql = """
        INSERT INTO individual (sex, line, genotype, birth_date, father_id, mother_id, user) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        c.execute(sql, (sex[i], p[0], p[1], p[2], p[3], p[4], p[5]))
    last_i = c.lastrowid
    conn.commit()
    return last_i

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
    conn.commit()

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
        conn.commit()

def make_success(name_table, val, name_id, i):
    sql = """ 
    UPDATE "{}" SET success = "{}" WHERE "{}" = "{}"
    """.format(name_table, val, name_id, i)
    c.execute(sql)
    conn.commit()


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


def show_warn(text):
    res = mbox.showwarning("title", text)
    print("showwarning", res)
    return 0