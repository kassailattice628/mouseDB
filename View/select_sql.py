"""select_sql.py"""
##########
import sqlite3
import pandas as pd
from tkinter import messagebox

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
        sql = """
        SELECT h.wean_id, h.birth_id, m.female_id, w.num_pup_male, w.num_pup_female
        FROM history h JOIN wean w ON h.wean_id = w.wean_id JOIN mate m ON h.mate_id = m.mate_id
        WHERE w.wean_id <= {}
        ORDER BY w.wean_id DESC
        """.format(ind+9)

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
