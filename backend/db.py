import sqlite3

def select_data():
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    # cur.execute("CREATE TABLE IF NOT EXISTS TIME_SPECIES(time datetime,true_name text, predict_name text, TF text)")
    cur.execute("SELECT * FROM TIME_SPECIES")
    for row in cur:
        print(str(row[0]))
        print(str(row[1]))
        print(str(row[2]))
        print(str(row[3]))
    con.close()


def insert_data(time,true_name,predict_name):
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TIME_SPECIES(time datetime,true_name text, predict_name text, TF text)")
    sql = 'INSERT INTO TIME_SPECIES (time, true_name, predict_name, TF) values (?,?,?,?)'

    if true_name=='nodata':
        TF='nodata'
    elif true_name==predict_name:
        TF=True
    else:
        TF=False

    data = [time, true_name, predict_name, TF]
    cur.execute(sql, data)
    con.commit()
    con.close()