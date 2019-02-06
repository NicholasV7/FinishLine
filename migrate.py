from main_ok import db

db.drop_all()
db.create_all()

db.session.commit()

import sqlite3


conn = sqlite3.connect('database.sqlite')

cursor = conn.cursor()
cursor.execute("insert into association values('0', '0')")
cursor.execute("insert into left values('0', 'tstlog1', 'tst1', 'pswd1')")
cursor.execute("insert into left values('1', 'tstlog2', 'tst2', 'pswd2')")
cursor.execute("insert into right values('0', 'tst', 'tst1', '0','1')")
cursor.execute("insert into third values('0', 'tst1', '1', '0')")
conn.commit()

conn.close()
