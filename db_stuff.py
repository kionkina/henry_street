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

#Have not tested these yet, but should work...

def add_item(price, name, description, due_date):
    db = sqlite3.connect(DB)
    c = db.cursor()
    q = 'SELECT * FROM items WHERE name = ?'
    c.execute(q,name)
    if not check.fetchone():
        c.execute('INSERT INTO items(price, name, description, due_date) VALUES (?,?,?,?)', (price, name, description, due_date))
        print "success!"
        db.commit()
        db.close()
        return True
    else:
        print "item (name) exists"
        return False

def edit_price(item_id, new_price):
    db = sqlite3.connect(DB)
    c = db.cursor()
    test = 'SELECT * FROM items WHERE item_id = ?'
    test_result = c.execute(test, item_id)
    if not test_result.fetchone():
        print "THIS ITEM DOESNT EXIST"
        return False
    else:
        query = 'UPDATE items SET price =? WHERE item_id = ?'
        c.execute(query, (new_price, item_id))
        db.commit()
        db.close()
        return True

def edit_name(item_id, new_name):
    db = sqlite3.connect(DB)
    c = db.cursor()
    test = 'SELECT * FROM items WHERE item_id = ?'
    test_result = c.execute(test, item_id)
    if not test_result.fetchone():
        print "THIS ITEM DOESNT EXIST"
        return False
    else:
        query = 'UPDATE items SET name =? WHERE item_id = ?'
        c.execute(query, (new_name, item_id))
        db.commit()
        db.close()
        return True

def edit_descr(item_id, new_descr):
    db = sqlite3.connect(DB)
    c = db.cursor()
    test = 'SELECT * FROM items WHERE item_id = ?'
    test_result = c.execute(test, item_id)
    if not test_result.fetchone():
        print "THIS ITEM DOESNT EXIST"
        return False
    else:
        query = 'UPDATE items SET description =? WHERE item_id = ?'
        c.execute(query, (new_descr, item_id))
        db.commit()
        db.close()
        return True

def edit_due_date(item_id, new_due_date):
    db = sqlite3.connect(DB)
    c = db.cursor()
    test = 'SELECT * FROM items WHERE item_id = ?'
    test_result = c.execute(test, item_id)
    if not test_result.fetchone():
        print "THIS ITEM DOESNT EXIST"
        return False
    else:
        query = 'UPDATE items SET due_date =? WHERE item_id = ?'
        c.execute(query, (new_due_date, item_id))
        db.commit()
        db.close()
        return True
    

