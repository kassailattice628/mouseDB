""" データ登録用の Class，window の情報を読んで，チェックして，登録．id 情報を返す""" 
import sqlite3
from tkinter import messagebox as mbox

class make_record():
    def __init__(self, which, params):
        self.conn = sqlite3.connect('mouseDB.sqlite3')
        self.c = self.conn.cursor()

        self.which = which
        self.params = params

        #subwindow からデータを読み取る
        self.p = []
        for i in range(1, len(self.params)-1):
            p_str = self.params[i].get()
            #空白除去
            p_str = p_str.replace(' ', '')
            self.p.append(p_str)
        print(self.p)

    def register(self):
        if self.which == 'buy':
            #p: 0:num_male,1:num_female,2:birthdate,3:line,4:genotype,5:user
            num_m = int(self.p[0])
            num_f = int(self.p[1])
            num_i = num_m + num_f
            sex_str = ['M'] * num_m
            sex_str.extend(['F'] * num_f)
            params = (self.p[3], self.p[4], self.p[2], None, None, self.p[5])
            add_new_records(num_i, sex_str, params, self.c)
            last_i = self.c.lastrowid

            self.conn.commit()
            return last_i, num_i

        ###################
        elif self.which == 'mate':
            #p: 0:id_male, 1:id_female, 2:start_date

            # chekc whether male and female are registered.
            v1 = check_id(self.p[0:2], self.c)
            if v1 == 0:
                return 0

            # get female state
            f_state = get_female_status(self.p[1], self.c)

            # add new mate record
            if f_state == 'B':
                sql = """ 
                INSERT INTO mate (male_id, female_id, start_date) values(?, ?, ?)
                """
                self.c.execute(sql, self.p[0:3])
                last_i = self.c.lastrowid

                change_state(self.p[1], 'M', self.c)

                # add mate_id into history
                add_to_history("mate_id", last_i, self.c, self.conn)

                self.conn.commit()
                print("commit a mate event")
                return last_i
            else:
                return 0

        ###################
        elif self.which == 'pregnancy':
            #p: 0:id_mate
            ids = find_mate_ids(self.which, self.p[0], self.c)

            change_state(ids[2], 'P', self.c)

            make_success("mate", 1, "mate_id", self.p[0], self.c)
            # mate.end_date を登録
            # ~~~~~
            #

            sql = """
            INSERT INTO pregnancy DEFAULT VALUES
            """
            self.c.execute(sql)
            last_i = self.c.lastrowid

            add_to_history("preg_id", last_i, self.c, mate_id = self.p[0])

            self.conn.commit()
            print("commit a pregnancy event")
            return last_i

        ####################
        elif self.which == 'birth':
            #p: 0:id_preg, 1:#male, 2:#female, 3:birth_date
            ids = find_mate_ids(self.which, self.p[0], self.c)
            change_state(ids[2], 'W', self.c)
            make_success("pregnancy", 1, "preg_id", self.p[0], self.c)


            #update success in birth table
            if int(self.p[1]) == 0 & int(self.p[2]) == 0:
                success = 0
            else:
                success = 1

            sql = """
            INSERT INTO birth (num_pup_male, num_pup_female, birth_date, success) VALUES (?, ?, ?)
            """
            val = (self.p[1], self.p[2], self.p[3], success)
            self.c.execute(sql, val)
            last_i = self.c.lastrowid

            add_to_history("birth_id", last_i, self.c, mate_id = self.p[0])

            self.conn.commit()
            print("commit a birth event")
            return last_i

        elif self.which == 'wean':
            #p: 0:id_wean, 1:#male, 2:#female, 3:line, 4:genotype, 5:user
            num_m = int(self.p[1])
            num_f = int(self.p[2])

            ids = find_mate_ids(self.which, self.p[0], self.c)
            bd = get_birthday(ids[0], self.c)

            change_state(ids[2], 'B', self.c)
            if num_m == 0 & num_f== 0:
                success = 0
            else:
                success = 1
            sql = """
            INSERT INTO wean (num_pup_male, num_pup_female, success) VALUES (?, ?, ?)
            """
            val = (self.p[1], self.p[2], success)
            self.c.execute(sql, val)
            last_i = self.c.lastrowid
            add_to_history("wean_id", last_i, self.c, mate_id = self.p[0])

            #insert new mice into individual
            num_i = num_m + num_f
            sex_str = ['M'] * num_m
            sex_str.extend(['F'] * num_f)

            params = (self.p[3], self.p[4], bd, ids[1], ids[2], self.p[5])
            add_new_records(num_i, sex_str, params, self.c)

            self.conn.commit()
            print("commit a birth event")
            return last_i

########## sub functions##########
def add_new_records(n, sex, p, c):
    print(p)
    #n:num_pups, p:parameters, c:cursor
    for i in range(0, n):
        sql = """
        INSERT INTO individual (sex, line, genotype, birth_date, father_id, mother_id, user) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        c.execute(sql, (sex[i], p[0], p[1], p[2], p[3], p[4], p[5]))

def add_to_history(which, i, c, mate_id = []):
    if which == 'mate_id':
        sql = """
        INSERT INTO history(mate_id) values("{}")
        """.format(i)
        c.execute(sql)
    else:
        sql = """
        UPDATE history SET "{}" = "{}" WHERE mate_id = "{}"
        """.format(which, i, mate_id)
        c.execute(sql)

    #commit って最後にやってもいいのか？
    #conn.commit()

def find_mate_ids(which, i, c):
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
    print(sql)
    c.execute(sql)
    ans = c.fetchall()[0]
    return ans

def get_sex(i, c):
    sql = """
    SELECT sex FROM individual WHERE mouse_id = "{}"
    """.format(i)
    c.execute(sql)
    return c.fetchall()[0][0]

def check_id(list_id, c):
    M = get_sex(list_id[0], c)
    F = get_sex(list_id[1], c)
    ans =[M, F]
    if ans == ['M', 'F']:
        return 1
    else:
        show_warrn("mouse_id is not appropriate!")
        return 0

def get_female_status(female_id, c):
    sql = """
    SELECT status FROM individual WHERE mouse_id = "{}"
    """.format(female_id)
    c.execute(sql)
    ans = c.fetchall()[0][0]
    return(ans)

def get_birthday(mate_id, c):
    sql = """
    SELECT birth_date FROM birth WHERE birth_id =
    (SELECT birth_id FROM history WHERE mate_id = "{}")
    """.format(mate_id)
    c.execute(sql)
    ans = c.fetchall()[0][0]
    return(ans)

def change_state(i, state, c):
    if state == "None":
        pass
    else:
        sql ="""
            UPDATE individual
            SET status = "{}"
            WHERE mouse_id = "{}"
        """.format(state, i)
        c.execute(sql)
        #conn.commit()

def make_success(name_table, val, name_id, i, c):
    sql = """ 
    UPDATE "{}" SET success = "{}" WHERE "{}" = "{}"
    """.format(name_table, val, name_id, i)
    c.execute(sql)
    #conn.commit()

def show_warrn(text):
    res = mbox.showwarning("title", text)
    print("showwarning", res)
    return 0
