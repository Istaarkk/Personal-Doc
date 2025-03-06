import sqlite3
import pathlib as pl
import logging
import hashlib

log = logging.getLogger(__name__)

class Passwd:
    def __init__(self, text):
        self.val = hashlib.sha256(text.encode('utf-8')).hexdigest()

def adapt_pwd(pwd):
    return str(pwd.val)

class Model:
    def __init__(self):
        self.con = sqlite3.connect('model.db')
        self.here = pl.Path(__file__).parent.resolve()
        sqlite3.register_adapter(Passwd, adapt_pwd)

    def load_sql(self, sqlscript):
        cur = self.con.cursor()
        with open(self.here / sqlscript, 'r') as f:
            try:
                cur.executescript(f.read())
            except Exception as e:
                log.error(str(e))

    def insert_account(self, data):
        with self.con as curs:
            curs.executemany("insert into ACCOUNT (ACC_LOGIN, ACC_NAME, ACC_SURNAME, ACC_PWD, ACC_MAIL) values (?, ?, ?, ?, ?)", data)
