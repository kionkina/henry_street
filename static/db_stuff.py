import sqlite3
import hashlib

DB = "base.db"

def auth(username, password):
    print "running db auth"
    db = sqlite3.connect(DB)
    c = db.cursor()
    pwd = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM donors WHERE username = ? AND password = ?'
    result = c.execute(query, (username, pwd))
    ret = result.fetchone()
    print ret
    db.close()
    return ret
                       
