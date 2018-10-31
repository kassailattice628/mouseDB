"""select_sql.py"""
##########
import sqlite3
import pandas as pd
from tkinter import messagebox

#Connect DB
conn = sqlite3.connect("mouseDB.sqlite3")
c = conn.cursor()

#選択した条件でマウスを検索して表示 <= mouseDB_App から
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

## 購入マウスの登録
def make_new_records(w):
    #read from subwindow
    num_male = w[1].get()
    num_female = w[2].get()
    birth_date = w[3].get()
    line = w[4].get()
    genotype = w[5].get()
    user = w[6].get()
    
    sex_str = ["M"] * int(num_male)
    sex_str.extend(["F"] * int(num_female))
    num_i = int(num_male) + int(num_female)
    #SQL
    for i in range(0, num_i):
        sql ="""
            INSERT INTO individual (sex, line, genotype, birth_date, user)
            VALUES ("{}", "{}", "{}", "{}", "{}")
            """.format(sex_str[i], line, genotype, birth_date, user)
        c.execute(sql)
        conn.commit()
    last_i = c.lastrowid
    return last_i, num_i
### END of "new_registers"

## mate イベントの作成
def make_new_mate(w):
    #read from subwindow
    id_male = w[1].get()
    id_female = w[2].get()
    start_date = w[3].get()

    #登録されている mouseか確認
    s = find_id(id_male, id_female)
    if s == 0:
        return 0

    #id_female の状態を取得
    state = find_state(id_female)

    if state == 'B':
        sql ="""
            INSERT INTO mate (male_id, female_id, start_date)
            VALUES ("{}", "{}", "{}")
        """.format(id_male, id_female, start_date)
        c.execute(sql)
        conn.commit()
        last_i = c.lastrowid

        #mother の state を変える
        change_state(id_female, 'M')
        return last_i
    else:
        res = messagebox.showwarning("title", "mother_id is not appropriate!")
        print("showwarning", res)
        return 0

### END if "make_new_mate"

def make_new_preg(w):
    #read from subwindow
    mate_id = w[1].get()
    # mate_id から motherの id を取得
    sql = """
        SELECT female_id FROM mate WHERE mate_id = "{}"
        """.format(mate_id)
    c.execute(sql)
    id_female = c.fetchall()[0][0]
    #state 変更 (M->P)
    change_state(id_female, 'P')
    #"mate" success を 1 に変更
    make_success("mate", 1, "mate_id", mate_id)
    #"mate"end_date を登録

    #pregnancy に新しい record を作成
    sql ="""
        INSERT INTO pregnancy(mate_id)
        VALUES ("{}")
        """.format(mate_id)
    c.execute(sql)
    conn.commit()
    last_i = c.lastrowid
    return last_i
### END of make_new_mate ###

def make_new_birth(w):
    #read params from sub window
    preg_id = w[1].get()
    num_male = w[2].get()
    num_female = w[3].get()
    birth_date = w[4].get()

    # preg_id から motherの id を取得
    sql = """
        SELECT female_id FROM mate WHERE mate_id = 
        (SELECT mate_id FROM pregnancy WHERE preg_id = "{}")
        """.format(preg_id)
    c.execute(sql)
    id_female = c.fetchall()[0][0]
    #state 変更 (P->W)
    change_state(id_female, 'W')
    #"pregnancy" success を 1 に変更
    make_success("pregnancy", 1, "preg_id", preg_id)
    #birth に新しい record を登録
    sql ="""
        INSERT INTO birth(preg_id, num_pup_male, num_pup_female, birth_date)
        VALUES ("{}", "{}", "{}", "{}")
        """.format(preg_id, num_male, num_female, birth_date)
    c.execute(sql)
    conn.commit()
    last_i = c.lastrowid

    #"birth" success を 1 に変更
    make_success("birth", 1, "birth_id", last_i)

    return last_i
### END OF make_new_birth ###

##########
def make_new_wean(w):
    #read params from sub window
    birth_id = w[1].get()
    num_male = w[2].get()
    num_female = w[3].get()
    line = w[4].get()
    genotype = w[5].get()
    user = w[6].get()

    # birth_id から mother_id, father_id を取得
    sql = """
        SELECT female_id, male_id FROM mate WHERE mate_id = 
        (SELECT mate_id FROM pregnancy WHERE preg_id = 
        (SELECT preg_id FROM birth WHERE birth_id = "{}"))
        """.format(birth_id)
    c.execute(sql)
    ids = c.fetchall()[0]
    mother_id = ids[0]
    father_id = ids[1]

    #state 変更
    change_state(mother_id, 'B')

    #wean に新しい record を登録
    sql ="""
        INSERT INTO wean (birth_id, num_pup_male, num_pup_female)
        VALUES ("{}", "{}", "{}")
        """.format(birth_id, num_male, num_female)
    c.execute(sql)
    conn.commit()
    last_i = c.lastrowid

    #"wean" success を 1 に変更
    make_success("wean", 1, "wean_id", last_i)

    #birth_date を取得
    sql = """
        SELECT birth_date FROM birth WHERE birth_id = "{}"
        """.format(birth_id)
    c.execute(sql)
    birth_date = c.fetchall()[0][0]

    #新しい individual を登録
    sex_str = ["M"] * int(num_male)
    sex_str.extend(["F"] * int(num_female))
    num_i = int(num_male) + int(num_female)
    for i in range(0, num_i):
        sql ="""
            INSERT INTO individual (sex, line, genotype, birth_date, user, father_id, mother_id)
            VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")
            """.format(sex_str[i], line, genotype, birth_date, user, father_id, mother_id)
        c.execute(sql)
        conn.commit()

    # データ表示用
    return last_i

##########
def make_retire(w):
    #id 範囲指定
    id1= w[1].get()
    id2= w[2].get()
    end_date = w[3].get()

    #ID
    if id1 == "" or  id2 == "":
        res = messagebox.showwarning("title", "Please put ID in both start From and To Field!")
        print("showwarning", res)
        return 0
    else:
        mouse_ids = range(int(id1), int(id2)+1)
        for i in mouse_ids:
            #state check
            s = find_state(i)
            if s != 'R':
                #end_date 登録
                sql = """
                UPDATE individual
                SET retire_date = {}
                WHERE mouse_id = {}
                """ .format(end_date, str(i))
                c.execute(sql)
                #
                change_state(i, 'R')
                conn.commit()
            else:
                print('id:"{}" has already been set  "R".'.format(i))

        return int(id2)
    
# Preg, Birt, Wean で表示する Mate (success = NULL のもの) を表示
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

### END of "Get_mate_id"

def Get_set_diff(sql1, sql2, i):
    df1 = pd.read_sql_query(sql1, conn)
    df2 = pd.read_sql_query(sql2, conn)
    l1 = df1[i].unique()
    l2 = df2[i].unique()
    r = list(set(l1) - set(l2))
    r = [str(n) for n in r]
    return r


########## 未設定のデータを表示 ##########
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

#show_new と同じようの slq 直の方がいいか
########## 最新 10 のデータを表示 ##########
def latest10(tree, which):
    if which == "pregnancy":
        sql = """
        SELECT mate_id, female_id, male_id, start_date, end_date, success
        FROM mate
        WHERE success IS NULL AND mate_id >= (
            SELECT MAX(mate_id) from mate) -9
        """
        # mate table を表示したい
        #columns = "mate_id, female_id, male_id, start_date, end_date, success"
        #table = "mate"
        #conditions = "success IS NULL AND mate_id >= (select MAX(mate_id) from mate) - 9"

    elif which == "birth":
        sql = """
        SELECT h.preg_id, h.mate_id, m.male_id, m.female_id
        FROM history h JOIN mate m ON h.mate_id = m.mate_id JOIN pregnancy p ON h.preg_id = p.preg_id
        WHERE p.success IS NULL AND p.preg_id >= (select MAX(preg_id) FROM pregnancy) - 9
        """
        # pregnancy table を表示したい
        #columns = "h.preg_id, h.mate_id, m.male_id, m.female_id"
        #table = "history h JOIN mate m ON h.mate_id = m.mate_id JOIN pregnancy p ON h.preg_id = p.preg_id"
        #conditions = "p.success IS NULL AND p.preg_id >= (select MAX(preg_id) FROM pregnancy) - 9"

    elif which == "wean":
        sql = """
        SELECT h.birth_id, h.preg_id, m.female_id, b.num_pup_male, b.num_pup_female, b.birth_date
        FROM history h JOIN birth b ON h.birth_id = b.birth_id JOIN mate m ON h.mate_id = m.mate_id
        WHERE b.success IS 1 AND h.wean_id IS null
        ORDER BY h.birth_id
        """
    Update_View(tree, sql)

## show extraxted table ##
def Update_View(tree, sql):
    tree.delete(*tree.get_children())
    i = 0
    for r in c.execute(sql):
        tree.insert("", "end", tags=i, values=r)
        if i & 1:
            tree.tag_configure(i, background="#CCFFFF")
        i += 1

## event によって mother の status を変更
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

def make_success(name_table, success, name_id, i):
    sql ="""
        UPDATE "{}"
        SET success = "{}"
        WHERE "{}" = "{}"
    """.format(name_table, success, name_id, i)
    c.execute(sql)
    conn.commit()

def find_state(i):
    #mouse_id を受け取って status を返す
    sql = """
        SELECT status FROM individual WHERE mouse_id = "{}"
    """.format(i)
    c.execute(sql)
    s = c.fetchall()
    return  s[0][0]

def find_id(i1, i2):
    ii = 0
    for i in (i1, i2):
        if ii == 0:
            sex = 'M'
        elif ii == 1:
            sex = 'F'
    
        sql =  """
            SELECT mouse_id FROM individual WHERE mouse_id IN ("{}") AND sex = "{}";
        """.format(i, sex)
        c.execute(sql)
        ans = c.fetchall()
        if len(ans) == 0:
            res = messagebox.showwarning("Error", "mouse_id: '{}' ('{}')is not appropriate!".format(i, sex))
            print("showwarning", res)
            return 0
        ii += 1