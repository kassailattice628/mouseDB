#import data from Richard's DB

##########
import pandas as pd
import sqlite3
import pandas.io.sql as psql
import make_tables
##########

make_tables

##########
df = pd.read_csv('./testDB/export.csv') #exported @ 181023
######
#index のみとり出し
df_sub_ind = pd.DataFrame({'mouse_id':df.index[:]})
######
#その他
sub = ['id', 'sex', 'status','line', 'gene', 'birth_date', 'death_date', 'father', 'mother', 'user']

df_sub = df[sub]
df_sub.columns = ['old_id', 'sex', 'status','line', 'genotype', 'birth_date', 'retire_date', 'father_id', 'mother_id', 'user']

status = df_sub['status']
status.update(status.map({'-':'B', 'NaN':'R'}))

line = df_sub['line']
line.update(line.str.replace('-ΔNeo',''))

genotype = df_sub['genotype']
genotype.update(genotype.fillna('-'))
genotype.update(genotype.map({'-':'unknown'}))

bd = df_sub['birth_date']
bd.update(bd.str.replace('-', '').str[2:])

dd = df_sub['retire_date']
dd.update(dd.str.replace('-', '').str[2:])

fa = df_sub['father_id']
fa.update(fa.str.replace('Mouse-', ''))
ma = df_sub['mother_id']
ma.update(ma.str.replace('Mouse-', ''))

# DataFrame から
df_concat = pd.concat([df_sub_ind, df_sub], axis=1)
###
db = "mouseDB.sqlite3"
with sqlite3.connect(db) as conn:
    psql.to_sql(df_concat, 'individual', conn, index=False, if_exists='append')

conn.close()