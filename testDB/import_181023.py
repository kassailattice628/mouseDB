#import data from Richard's DB

##########
import pandas as pd
import sqlite3
##########
df = pd.read_csv('export.csv') #exported @ 181023
sub = ['id', 'sex', 'status','line', 'gene', 'birth_date', 'death_date', 'father', 'mother', 'user']

df_sub = df[sub]
df_sub.columns = ['mouse_id', 'sex', 'status','line', 'gene', 'birth_date', 'retire_date', 'father_id', 'mother_id', 'user']]

status = df_sub['status']
status.update(status.map({'-':'B', 'NaN':'R'}))

line = df_sub['line']
line.update(line.str.replace('-ΔNeo',''))

gene = df_sub['gene']
gene.update(gene.fillna('-'))
gene.update(gene.map({'-':'unknown'}))

bd = df_sub['birth_date']
bd.update(bd.str.replace('-', '').str[2:])

dd = df_sub['death_date']
dd.update(dd.str.replace('-', '').str[2:])

fa = df_sub['father']
fa.update(fa.str.replace('Mouse-', ''))
ma = df_sub['mother']
ma.update(ma.str.replace('Mouse-', ''))

###
db = "mouse_db.sqlite3"
conn = sqlite3.connect(db)
c = conn.cursor()

df_sub.to_sql("individual", conn, if_exists="replace")

conn.close()