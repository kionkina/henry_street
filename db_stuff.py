import sqlite3
import hashlib

#---------------NOTES------------------------------------
# use this query to reset autoincrement after 
# manually deleting a row:

# q = 'UPDATE sqlite_sequence SET seq = ? WHERE seq = ?'#
# c.execute(q, (current_seq, desired_seq))
#--------------------------------------------------------

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
                       
def add_donor(fname, lname,username, password, email):
    print "running add_donor..."
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM donors WHERE username = ?'
    check = c.execute(query, (username,))
    if not check.fetchone():
        c.execute(q, (1, 6))
        new_pass = hashlib.sha256(password).hexdigest()
        c.execute('INSERT INTO donors(fname, lname, username, password, email) VALUES (?,?,?,?,?)', (fname, lname, username, new_pass, email))
        db.commit()
        db.close()
        print "SUCCESS!"
        return True
    else:
        print "credentials are already in use"
        db.commit()
        db.close()
        return False

#------------------------ ADMIN FXNS -------------------------------------------------------

#def add_item(price, name, description, due_date):
 #   db = sqlite3.connect(DB)
 #   c = db.cursor()

