import sqlite3

conn_old = sqlite3.connect('/Users/lattice/Documents/sqlite/testDB/mouseDB.sqlite3')
c_old = conn_old.cursor()

sql = """SELECT status, retire_date FROM individual"""
c_old.execute(sql)

old = c_old.fetchall()
conn_old.close()


###
conn_now = sqlite3.connect('/Users/lattice/Documents/sqlite/testDB/mouseDB2.sqlite3')
c_now = conn_now.cursor()

for i in range(0, len(old)):
    sql = """UPDATE individual SET status = "{}", retire_date="{}" WHERE mouse_id = "{}"
    """.format(old[i][0], old[i][1], i)
    c_now.execute(sql)
    conn_now.commit()


