import sqlite3

conn = sqlite3.connect("mouseDB.sqlite3")
conn.execute('PRAGMA foreign_keys = 1')

def create_table(sql):
    conn.execute(sql)
    conn.commit()

#individual
sql = """
CREATE TABLE `individual` (
	`mouse_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`old_id`	INTEGER NOT NULL,
	`sex`	TEXT NOT NULL DEFAULT 'M',
	`status`	TEXT NOT NULL DEFAULT 'B',
	`line`	TEXT DEFAULT 'C57BL6',
	`genotype`	TEXT DEFAULT 'wt',
	`birth_date`	TEXT,
	`retire_date`	TEXT,
	`father_id`	INTEGER,
	`mother_id`	INTEGER,
	`generation`	INTEGER,
	`user`	TEXT DEFAULT 'KASAI'
);
"""
create_table(sql)

# mate
sql ="""
CREATE TABLE `mate` (
	`mate_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`male_id`	INTEGER NOT NULL,
	`female_id`	INTEGER NOT NULL,
	`start_date`	TEXT NOT NULL,
	`success`	INTEGER,
	`end_date`	TEXT
);"""
create_table(sql)

# pregnancy
sql="""
CREATE TABLE `pregnancy` (
	`preg_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`mate_id`	INTEGER NOT NULL,
	`success`	INTEGER,
	`male_id`	INTEGER NOT NULL,
	`female_id`	INTEGER NOT NULL,
	FOREIGN KEY(`mate_id`) REFERENCES `mate`(`mate_id`) ON UPDATE CASCADE ON DELETE SET NULL
);
"""
create_table(sql)

# brith
sql="""
CREATE TABLE `birth` (
	`birth_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`preg_id`	INTEGER NOT NULL,
	`num_pup_male`	INTEGER NOT NULL DEFAULT 0,
	`num_pup_female`	INTEGER NOT NULL DEFAULT 0,
	`birth_date`	TEXT NOT NULL,
	`success`	INTEGER,
	FOREIGN KEY(`preg_id`) REFERENCES `pregnancy`(`preg_id`) ON UPDATE CASCADE ON DELETE SET NULL
);
"""
create_table(sql)

#wean
sql="""
CREATE TABLE `wean` (
	`wean_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`birth_id`	INTEGER NOT NULL,
	`num_pup_male`	INTEGER NOT NULL DEFAULT 0,
	`num_pup_female`	INTEGER NOT NULL DEFAULT 0,
	`success`	INTEGER,
	FOREIGN KEY(`birth_id`) REFERENCES `birth`(`birth_id`) ON UPDATE CASCADE ON DELETE SET NULL
);
"""
create_table(sql)

#####
conn.commit()
conn.close()
