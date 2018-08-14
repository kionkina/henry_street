import sqlite3
import hashlib

#---------------NOTES------------------------------------
# use this query to reset autoincrement after 
# manually deleting a row:

# q = 'UPDATE sqlite_sequence SET seq = ? WHERE seq = ?'#
# c.execute(q, (current_seq, desired_seq))
#--------------------------------------------------------

DB = "base.db"


#returns True if user exists, False otherwise
def auth(username, password):
#    print "running db auth"
    db = sqlite3.connect(DB)
    c = db.cursor()
    pwd = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM donors WHERE username = ? AND password = ?'
    result = c.execute(query, (username, pwd))
    ret = result.fetchone()
#    print ret
    db.close()
    if ret != None:
        return True
    else:
        return False

print auth('kionkina', 'karina')
print auth('kionkina', 'karin')
                       
def add_donor(fname, lname,username, password, email):
    print "running add_donor..."
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM donors WHERE username = ?'
    check = c.execute(query, (username,))
    if check.fetchone() == None:
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

def get_user_id(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    print username
    query = 'SELECT user_id from donors WHERE username = ?' 
    result = c.execute(query, (username,))
    if result:
        print "result"
        print result
        for tuple in result:
            return tuple[0]
    else:
        print "no such username"
        return 

def list_of_transactions(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
    user_id = get_user_id(username)
    print user_id
    query = 'SELECT * FROM transactions WHERE user_id = ?' 
    result = c.execute(query, (user_id,))
    ret = []
    for transaction in result:
        if transaction == None:
            return 
        else:
            trans = []
            for i in transaction:
                trans.append(i)
            ret.append(trans)
    return ret
    
print list_of_transactions('kionkina') 

#------------------------ ADMIN FXNS -------------------------------------------------------

#Have not tested these yet, but should work...

def add_item(price, name, description, due_date):
    db = sqlite3.connect(DB)
    c = db.cursor()
    q = 'SELECT * FROM items WHERE name = ?'
    c.execute(q,name)
    if check.fetchone() == None:
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
    if test_result.fetchone() == None:
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
    if test_result.fetchone() == None:
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
    if test_result.fetchone() == None:
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
    if test_result.fetchone() == None:
        print "THIS ITEM DOESNT EXIST"
        return False
    else:
        query = 'UPDATE items SET due_date =? WHERE item_id = ?'
        c.execute(query, (new_due_date, item_id))
        db.commit()
        db.close()
        return True
    


#index 0: item_id
#index 1: price
#index 2: name
#index 3: description
#index 4: due date


def get_item_info(item_id):
    db = sqlite3.connect(DB)
    c = db.cursor()
    ret = []
    test = 'SELECT * FROM items WHERE item_id = ?'
    result = c.execute(test, (item_id,))
#    print "printing result..."
    query_result = result.fetchone()
#    print query_result
#    print "does it == None?"
#    print query_result == None
    if query_result != None:
        for i in query_result:
            ret.append(i)
    db.commit()
    db.close()
    return ret

def get_all_item_info():
    db = sqlite3.connect(DB)
    c = db.cursor()
    ret = []
    total_q = "SELECT max(item_id) FROM items"
    total = c.execute(total_q)
#    print "total.fetchone()[0]"
#    print total.fetchone()[0]
    total = total.fetchone()[0]
    for i in range(1, total+1):
        print "i: "
        print i
        ret.append(get_item_info(i))
    db.commit()
    db.close()
    print "printing ret"
    print ret
    return ret


print get_item_info(1)        
print get_item_info(2)        

