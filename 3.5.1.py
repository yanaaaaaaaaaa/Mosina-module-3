import sqlite3
from functools import reduce
import csv

def create_table(name, fields, db: sqlite3.Connection):
    c = db.cursor()
    c.execute(f'''CREATE TABLE {name} ({reduce(lambda x,y: x + y, fields)})''')
    db.commit()
    c.close()


with sqlite3.connect('python_proj.db') as db:
    with open('compile.csv') as file:
        reader = csv.reader(file)
        header = next(reader)
        new_header = header.copy()
        new_header[0] += ' TEXT PRIMARY KEY,'
        for i in range(1, len(new_header)):
            new_header[i] += ' REAL,'
        new_header[-1] = new_header[-1][:-1]
        #create_table('currencies', new_header, db)
        c = db.cursor()
        for row in reader:
            s = ""
            for el in row:
                s += f"'{el}', "
            s = s[:-2]
            command = f"INSERT INTO currencies VALUES ({s})"
            c.execute(command)
    db.commit()









