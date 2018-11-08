#! /usr/bin/env python
# -*-coding: utf-8 -*-
""" View/register.py"""
##########
from View import select_sql as ss

class make_record():
    def __init__(self, which, params):
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

        elif self.which == 'mate':
            #p: 0:id_male, 1:id_female, 2:start_date
            last_i = ss.add_new_mate(self.p)
            return last_i

        elif self.which == 'pregnancy':
            #p: 0:id_mate

            last_i = ss.add_new_pregnancy(self.which, self.p)
            return last_i

        elif self.which == 'birth':
            #p: 0:id_preg, 1:#male_pups, #2:#female_pups, 3:birth_date
            last_i = ss.add_new_birth(self.which, self.p)
            return last_i

        elif self.which == 'wean':
            #p: 0:id_birth, 1:#male, 2:#female, 3:line, 4:genotype, 5:user
            last_i = ss.add_new_wean(self.which, self.p)
            return last_i

        elif self.which == 'retire':
            #空欄 error
            last_i = ss.retire(self.p)
            return last_i
            
        ### end of if which ==
    ### end of def regisuter
###end of class make_register

