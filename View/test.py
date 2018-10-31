""" View/test.py"""

import sqlite3
from View import select_sql as ss

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
            last_i = ss.add_new_records(num_i, sex_str, params)
            return last_i, num_i

        ###################
        elif self.which == 'mate':
            #p: 0:id_male, 1:id_female, 2:start_date

            # chekc whether male and female are registered.
            v1 = ss.check_id(self.p[0:2])
            v2 = ss.check_sex(self.p[0:2])

            if v1 == 0 or v2 == 0:
                return 0

            f_state = ss.get_status(self.p[1])

            # add new mate record
            if f_state == 'B':
                sql = """ 
                INSERT INTO mate (male_id, female_id, start_date) values(?, ?, ?)
                """
                self.c.execute(sql, self.p[0:3])
                last_i = self.c.lastrowid
                self.conn.commit()

                ss.change_state(self.p[1], 'M')

                ss.add_to_history("mate_id", last_i)

                print("commit a mate event")
                return last_i
            else:
                ss.show_warn("status of id:'{}' is not 'B'".format(self.p[1]))
                return 0

        ###################
        elif self.which == 'pregnancy':
            #p: 0:id_mate
            ids = ss.find_mate_ids(self.which, self.p[0])

            ss.change_state(ids[2], 'P')

            ss.make_success("mate", 1, "mate_id", self.p[0])
            # mate.end_date を登録
            # ~~~~~
            #

            sql = """
            INSERT INTO pregnancy DEFAULT VALUES
            """
            self.c.execute(sql)
            last_i = self.c.lastrowid
            self.conn.commit()

            ss.add_to_history("preg_id", last_i, mate_id = self.p[0])

            print("commit a pregnancy event")
            return last_i

        ####################
        elif self.which == 'birth':
            #p: 0:id_preg, 1:#male_pups, 2:#female_pups, 3:birth_date
            ids = ss.find_mate_ids(self.which, self.p[0])
            ss.change_state(ids[2], 'W')
            ss.make_success("pregnancy", 1, "preg_id", self.p[0])

            #update birth table
            if int(self.p[1]) == 0 and int(self.p[2]) == 0:
                success = 0
            else:
                success = 1

            sql = """
            INSERT INTO birth (num_pup_male, num_pup_female, birth_date, success) VALUES (?, ?, ?, ?)
            """
            val = (self.p[1], self.p[2], self.p[3], success)
            self.c.execute(sql, val)
            last_i = self.c.lastrowid
            self.conn.commit()

            ss.add_to_history("birth_id", last_i, mate_id = ids[0])
            
            print("commit a birth event")
            return last_i

        elif self.which == 'wean':
            #p: 0:id_birth, 1:#male, 2:#female, 3:line, 4:genotype, 5:user
            num_m = int(self.p[1])
            num_f = int(self.p[2])

            ids = ss.find_mate_ids(self.which, self.p[0])
            bd = ss.get_birthday(ids[0])
            ss.change_state(ids[2], 'B')

            if num_m == 0 and num_f== 0:
                success = 0
                print("no mice wean")
            else:
                success = 1
            sql = """
            INSERT INTO wean (num_pup_male, num_pup_female, success) VALUES (?, ?, ?)
            """
            val = (self.p[1], self.p[2], success)
            self.c.execute(sql, val)
            last_i = self.c.lastrowid
            self.conn.commit()

            ss.add_to_history("wean_id", last_i, mate_id = ids[0])

            if success == 1:
                num_i = num_m + num_f
                sex_str = ['M'] * num_m
                sex_str.extend(['F'] * num_f)

                params = (self.p[3], self.p[4], bd, ids[1], ids[2], self.p[5])

                last_i = ss.add_new_records(num_i, sex_str, params)

                print("commit a birth event")
            else:
                last_i = 0
            return last_i

        elif self.which == 'retire':
            #空欄 error
            if self.p[0] == '' or self.p[1] == '':
                ss.show_warn('Please put ID in both FROM and TO fields!')
                return 0
            
            #0:id from, 1: id to, 2: retire date
            v1 = ss.check_id(self.p[0:2])
            if v1 == 0:
                return 0
            
            ids = range(int(self.p[0]), int(self.p[1])+1)
            for i in ids:
                s = ss.get_status(i)
                if s != 'R':
                    sql = """ 
                    UPDATE individual SET retire_date = {} WHERE mouse_id = {}
                    """.format(self.p[2], str(i))
                    self.c.execute(sql)
                    self.conn.commit()
                    
                    ss.change_state(i, 'R')
                else:
                    print('id:"{}" has already been set as "R".'.format(i))
            return int(self.p[1])