# coding=utf-8

import sqlite3
import os
import datetime

base_path = os.getcwd()

conn = sqlite3.connect(base_path+'/test.db')
with conn:
    cu = conn.cursor()
    cu.execute('drop table if exists cars')
    cu.execute('create table cars (id integer,name text,price integer)')
    cars = (
        (1, 'Audi', 52642),
        (2, 'Mercedes', 57127),
        (3, 'Skoda', 9000),
        (4, 'Volvo', 29000),
        (5, 'Bentley', 350000),
        (6, 'Hummer', 41400),
        (7, 'Volkswagen', 21600)
    )
    cu.executemany('insert into cars values(?,?,?)', cars)

content = cu.execute('select * from cars')
print content.fetchall()
test = 500
cu.execute('update cars set price=?', (test,))
content = cu.execute('select * from cars')
print content.fetchall()
content = cu.execute('pragma table_info(cars)')
print content.fetchall()

print os.path.isabs('C:/cjaj/sfjl')
print os.path.split('/sajfl/sajfl/uuu')
a = 'a/b'
b = 'c.jpg'
aa = os.path.join(a, b)
print aa
print os.path.abspath('asfjaj/saf')
print os.path.basename('jafj/ajsf.')
print os.path.splitext(aa)
print os.path.expanduser('~')

