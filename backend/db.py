import sqlite3
import pandas as pd

def select_data():
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TIME_SPECIES(id INTEGER PRIMARY KEY AUTOINCREMENT, time DATETIME,true_name TEXT, predict_name TEXT, TF TEXT)")
    df = pd.read_sql('SELECT * FROM TIME_SPECIES', con)
    cur.close()
    con.close()
    return df


def insert_data(time,true_name,predict_name):
    con = sqlite3.connect('./sample.db')
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TIME_SPECIES(id INTEGER PRIMARY KEY AUTOINCREMENT, time DATETIME,true_name TEXT, predict_name TEXT, TF TEXT)")
    sql = 'INSERT INTO TIME_SPECIES (time, true_name, predict_name, TF) values (?,?,?,?)'

    if true_name=='nodata':
        TF='NA'
    elif true_name==predict_name:
        TF=True
    else:
        TF=False

    data = [time, true_name, predict_name, TF]
    cur.execute(sql, data)
    con.commit()
    cur.close()
    con.close()