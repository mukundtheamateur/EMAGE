#custom module
import source_rendition as emo
import detect_age_video as aged

import sqlite3
from tkinter import *

from multiprocessing import Process
import sys


agedetail = aged.agerec()
emotiondetail = emo.emotionrec()

conn = sqlite3.connect('music4.db')
c = conn.cursor()
#-----------------query---------------------
query = "SELECT rowid, * FROM music WHERE"
query = query + " " + str(agedetail) + " LIKE '1' AND "
query = query + str(emotiondetail) + " LIKE '1'"
print(query)
c.execute(query)
items = c.fetchall()
print_items = ''
for item in items:
    print_items = str(item[0]) + " " + str(item[1]) + "\t\t\t\t|" + str(item[2]) + "   " + str(item[3]) + "    " + str(item[4])+ "    " + str(item[5]) + "    " + str(item[6]) + "    " + str(item[7]) + "    " + str(item[8]) + "    " + str(item[9]) + "  |  " + str(item[10]) + "    " + str(item[11]) + "    " + str(item[12]) + "    " + str(item[13]) + "    " + str(item[14])
    print(print_items)

conn.commit()
conn.close()