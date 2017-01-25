#!/usr/bin/python

import sqlite3

GL_DB_NAME = 'bmh.db'
GL_DB_TABLE_USERS = 'USERS'
GL_DB_TABLE_BOOKMARKS = 'BOOKMARKS'

def db_create():
    conn = sqlite3.connect(GL_DB_NAME)
    
    command = '''CREATE TABLE %s
        (ID CHAR(24) PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        PASSWD         CHAR(18)     NOT NULL,
        BMID           INT,
        PHONENB        INT(11),
        ADDRESS        CHAR(50),
        SALARY         REAL);'''%GL_DB_TABLE_USERS
    conn.execute(command)
    
    conn.execute('''CREATE TABLE %s
        (ID         INT PRIMARY KEY     NOT NULL,
        USERID      CHAR(24)    NOT NULL,
        LABEL       CHAR(50)    NOT NULL,
        CONTENT     );'''%GL_DB_TABLE_BOOKMARKS)
    
    conn.close()

def db_query_user(p):
    conn = sqlite3.connect(GL_DB_NAME)
    print "Opened database successfully";

    cursor = conn.execute("SELECT id, name, passwd from %s where id = \"%s\""%(GL_DB_TABLE_USERS,p))
    data_user = None
    for row in cursor:
        print "ID = ", row[0]
        print "NAME = ", row[1]
        print "PASSWD = ", row[2], "\n"
        data_user={'id':row[0], 'name':row[1], 'passwd':row[2]}
    
    conn.close()
    return data_user

def db_insert_user(l):
    # list->[ID,NAME,PASSWD]
    print 'list->%s\n'%str(l)
    if len(l)!=3:
        print 'data base insert cancel, parameter format error'
        return None
    if not db_query_user(l[0])==None:
        return 'user [%s] exist already'%l[0]

    conn = sqlite3.connect(GL_DB_NAME)
    conn.execute("INSERT INTO %s (ID,NAME,PASSWD)\
                 VALUES (\"%s\", \"%s\", \"%s\")"%(GL_DB_TABLE_USERS,l[0],l[1],l[2]) );
    conn.commit()
    conn.close()
    return True;

def db_insert_bookmark(l):
    # USERID,LABEL,CONTENT
    print 'insert bookmark->%s\n'%str(l)
    conn = sqlite3.connect(GL_DB_NAME)
    if len(l)!=3:
        print 'data base insert cancel, parameter format error'
        return
    cursor = conn.execute("SELECT COUNT(*) FROM %s"%GL_DB_TABLE_BOOKMARKS)
    count = -1
    for i in cursor:
        print 'count:',i[0]
        count = i[0]

    conn.execute("INSERT INTO %s (ID,USERID,LABEL,CONTENT)\
                 VALUES (%s, \"%s\", \"%s\", \"%s\")"%(GL_DB_TABLE_BOOKMARKS,count+1,l[0],l[1],l[2]) );
    conn.commit()
    conn.close()

def db_delete_bmarks(bms):
    print 'delete bookmark ', bms
    
    conn = sqlite3.connect(GL_DB_NAME)
    for i in bms:
        if 'id' not in i:
#            return 'parameter error while modify bookmark'
            continue
        conn.execute("DELETE FROM %s WHERE ID = %s"%(GL_DB_TABLE_BOOKMARKS, i['id']) );
    conn.commit()
    conn.close()

def db_query_bmarks(p):
    conn = sqlite3.connect(GL_DB_NAME)
#
    cursor = conn.execute("SELECT id,userid,label,content from %s where userid = \"%s\""%(GL_DB_TABLE_BOOKMARKS,p) )
    data_bmarks = []
    for row in cursor:
#        print "ID = ", row[0]
#        print "LABEL = ", row[2]
#        print "CONTENT = ", row[3], "\n"
        data_bmarks.append({'id':row[0],'userid':row[1],'label':row[2],'content':row[3]})

    conn.close()
    return data_bmarks

def db_modify_bookmark(pt):
    # USERID,LABEL,CONTENT
    print 'modify bookmark->%s\n'%str(pt)
    conn = sqlite3.connect(GL_DB_NAME)
    if 'id' not in pt or 'address' not in pt:
        return 'parameter error while modify bookmark'
    cursor = conn.execute("SELECT id,userid,label,content from %s where id = \"%s\""%(GL_DB_TABLE_BOOKMARKS,pt['id']))
    t_bm = {}
    for i in cursor:
        print 'query [%s]:%s'%(pt['id'],i)
        t_bm['id'] = i[0]
        t_bm['userid'] = i[1]
        t_bm['label'] = i[2]
        t_bm['address'] = i[3]
    if t_bm['label']!=None and t_bm['address']!=None and t_bm['label']==pt['label'] and t_bm['address']==pt['address']:
        print 'cancel modify bookmark, same bookmark'
        conn.close()
        return 'fail'

    conn.execute("UPDATE %s SET label = '%s', content = '%s' WHERE id = %s;"%(GL_DB_TABLE_BOOKMARKS,pt['label'],pt['address'],pt['id']) );
    conn.commit()
    conn.close()


if __name__ == "__main__":
#    ls = "name:"
#    db_create()
#
#    ls = ["black201","xiaoming","ming123"]
#    db_insert_user(ls)
    u = db_query_user("black2011")
    if not u==None:
        print 'name->',u['name']
    else:
        print 'None user'
#    db_insert_bookmark(["black201","eisp","http://eisp.idpbg.efoxconn.com"])
#    db_insert_bookmark(["black201","culture","http://culture.efoxconn.com"])
#    bmarks = db_query_bmarks("black201")
#    for bm in bmarks:
#        print bm['userid'],bm['label'], bm['content']

#    t_bm = {'index': u'1', 'address': u'http://eisp.idpbg.efoxconn.com', 'id': u'12', 'label': u'eispp'}
#    rst = db_modify_bookmark(t_bm)
#    if rst == None:
#        print 'modify seccess'
#    else:
#        print 'modify failure, ', rst


