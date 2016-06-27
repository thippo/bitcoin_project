import sqlite3

conn = sqlite3.connect('bitcoin.db')
cu = conn.cursor()
cu.execute('create table ordertable (id integer UNIQUE, date integer, price double, amount double, cost double)')
cu.execute('create table indextable (name varchar(8) , cost double)')
cu.execute("insert into indextable values('daysmean', 0)")
cu.execute("insert into indextable values('costmean', 0)")
cu.execute("create table message (name varchar, price double, buy integer)")
cu.execute("insert into message values('now', 0, 0)")
conn.commit()
conn.close()
