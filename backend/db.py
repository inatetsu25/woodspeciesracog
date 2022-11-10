import sqlite3

def select_data():
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TIME_SPECIES(time datetime,name text)")
    cur.execute("SELECT * FROM TIME_SPECIES")
    for row in cur:
        print(str(row[0]) + "," + str(row[1]))
    con.close()


def insert_data(time,name):
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    sql = 'INSERT INTO TIME_SPECIES (time, name) values (?,?)'
    data = [time, name]
    cur.execute(sql, data)
    con.commit()
    con.close()