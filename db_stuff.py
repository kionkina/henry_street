import sqlite3
import hashlib
import datetime

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

#print auth('kionkina', 'karina')
#print auth('kionkina', 'karin')


def admin_auth(username, password):
#    print "running db auth"
    db = sqlite3.connect(DB)
    c = db.cursor()
    pwd = hashlib.sha256(password).hexdigest()
    query = 'SELECT password FROM admins WHERE username = ? AND password = ?'
    result = c.execute(query, (username, pwd))
    ret = result.fetchone()
#    print ret
    db.close()
    if ret != None:
        return True
    else:
        return False

def add_donor(fname, lname,username, password, email):
    print "running add_donor..."
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT * FROM donors WHERE username = ?'
    check = c.execute(query, (username,))
    if check.fetchone() == None:
        c.execute(query, (username,))
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

def add_transaction(id, username):
	db = sqlite3.connect(DB)
	c = db.cursor()
	item_id=int(id)
	user_id = get_user_id(username)
	query = "INSERT INTO transactions VALUES ({0}, {1}, {2})"
	date=str(datetime.datetime.utcnow()).split()[0]
	print [user_id, item_id, date]
	c.execute(query.format(user_id, item_id, date))
	db.commit()
	db.close()
	return username

#------------------------ ADMIN FXNS -------------------------------------------------------


def add_the_item(name, price, SD, img, date, url, username):
    print "RUNNING ADD_ITEM"

    admin_id = get_admin_id(username)
    print "ADMIN ID IS:"
    print admin_id

    db = sqlite3.connect(DB)
    c = db.cursor()
    q = 'SELECT (EXISTS (SELECT 1 FROM items WHERE name = ?))'
    check = c.execute(q, (name,)).fetchone()[0]
    if check == 0:
        c.execute('INSERT INTO items(price, name, description, img, due_date, url, admin_id) VALUES (?,?,?,?,?,?,?)', (price, name, SD, img, date,url,admin_id))
        print "success!"
        db.commit()
        db.close()
        return True
    else:
#        print "item (name) exists"
        return False





def get_admin_id(username):
    db = sqlite3.connect(DB)
    c = db.cursor()
#    print username
    query = 'SELECT user_id from admins WHERE username = ?'
    result = c.execute(query, (username,))
    if result:
        for tuple in result:
            return tuple[0]
    else:
        print "no such username"
        return


#Have not tested these yet, but should work...

def add_item(price, name, description, due_date):
    db = sqlite3.connect(DB)
    c = db.cursor()
    q = 'SELECT * FROM items WHERE name = ?'
    c.execute(q, (name,))
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
#index 4: img
#index 5: due_date
#index 6: url
#index 7: admin_id
#index 8: num_collected

def get_item_info(item_id):
    '''
    Returns an array containing all aspects of
    item info

    [item_id, price, name, description, img, due_date, url, admin_id]

    '''
    db = sqlite3.connect(DB)
    c = db.cursor()
    ret = []
    test = 'SELECT * FROM items WHERE item_id = ?'
    result = c.execute(test, (item_id,))
    query_result = result.fetchone()
    if query_result != None:
        for i in query_result:
            ret.append(i)
    # APPENDING THE NUM_COLLECTED:
    ret.append(num_collected(item_id))
    db.commit()
    db.close()
    return ret

def get_all_item_info():
    '''
    Returns array with info arrays for each
    available item
    '''
    db = sqlite3.connect(DB)
    c = db.cursor()
    ret = []
    total_q = "SELECT max(item_id) FROM items"
    total = c.execute(total_q)
    total = total.fetchone()[0]
    for i in range(1, total+1):
#        print "i: "
#        print i
        ret.append(get_item_info(i))
    db.commit()
    db.close()
    return ret


def my_items(username):
    '''
    Takes admin username and returns list of item_ids
    of items added by the user
    '''
    print "RUNNING MY_ITEMS"
    id = get_admin_id(username)
    db = sqlite3.connect(DB)
    c = db.cursor()
    q = 'SELECT item_id FROM items WHERE admin_id = ?'
    result = c.execute(q, (id,))
    result = result.fetchall()
    ret = []
    for i in result:
        ret.append(i[0])
    print "RESULT IS"
    print ret
    return ret


def my_item_info(items):
    '''
    Uses list of item_ids to return list with
    item info for each id
    '''
    print "RUNNING MY_ITEM_INFO"
    ret = []
    for i in items:
        ret.append(get_item_info(i))
    print "RETURNING"
    print ret
    return ret

#print my_item_info(my_items("admin"))

#print "admin"
#print my_items("admin")
#print "boop"
#print my_items("boop")

def get_item_id(name):
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT item_id from items WHERE name = ?'
    result = c.execute(query, (name,))
    if result:
        for tuple in result:
            return tuple[0]
    else:
        print "no such username"
        return

'''
def num_collected(name):
    print "running num_collected for " + name
    item_id = get_item_id(name)
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT count(*) FROM transactions WHERE item_id = ?'
    result = c.execute(query, (item_id,))
    if result:
        for tuple in result:
            print tuple[0]
            return tuple[0]
    else:
        print "0"
        return 0
'''

def num_collected(item_id):
    print "running num_collected for " 
    db = sqlite3.connect(DB)
    c = db.cursor()
    query = 'SELECT count(*) FROM transactions WHERE item_id = ?'
    result = c.execute(query, (item_id,))
    if result:
        for tuple in result:
            print tuple[0]
            return tuple[0]
    else:
        print "0"
        return 0
