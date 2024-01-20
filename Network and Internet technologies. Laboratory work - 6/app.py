import sqlite3
from flask import Flask, session

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

conn = sqlite3.connect("library.sqlite")
f = open('library.db', 'r', encoding='utf-8-sig')
damp = f.read()
conn.executescript(damp)
conn.commit()
f.close()
conn.close()

import controllers.index
import controllers.new_reader
import controllers.search