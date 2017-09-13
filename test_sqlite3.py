import sqlite3

conn = sqlite3.connect("tutorial.db")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)")

def data_entry():
    c.execute("INSERT INTO stuffToPlot VALUES(14512354, '2017-07-05', 'Python', 5)")
    conn.commit()
    c.close()  # close cursor and connection
    conn.close()

create_table()
data_entry()