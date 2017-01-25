from flask import *
from tool import *

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def slash():
#    render_template('login.html')
    print '****go login*****'
    return redirect(url_for('login'))
#    return '<html><body><h1>Hello World</h1></body><html>'

#@app.route('/success/<name>')
#def success(name):
#    return '<html><meta http-equiv="refresh" content="5;url=hello.html"> <body> <h3>Hi, %s<br/>login seccess</h3></body></html>' % name

@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        print("POST method")
        user=request.form['nm']
        pw = request.form['pw'];
        if user==None or pw==None:
            return redirect(url_for('login'))
        if 'username' in session:
            user=session['username']
        else:
            session['username']=user
#        return render_template('hello.html', name=user)
        o_user = db_query_user(user)
        if not o_user==None and o_user['passwd']==pw:
            return '<html><meta http-equiv="refresh" content="5;url=home"> <body> <h3>Hi, %s<br/>login seccess</h3></body></html>' % user
        else:
            return '<html><body><h3>user name or pass word not correct</h3></body></html>'

#        return redirect(url_for('success',name=user))
    else:
        print("login GET method")
#        t_args = request.args
#        print type(t_args)
#        user=request.args.get('nm')
        if 'username' in session:
            print 'already login[%s], go home page'%session['username']
            return redirect(url_for('home'))
        else:
            print 'not login, go login'
            return render_template('login.html')
#        return redirect(url_for('success',name=user))

@app.route('/home')
def home():
    user = None
    if 'username' in session:
        user = session['username']
    if user == None:
        print 'user None'
        print 'redirect->', url_for('login')
        return redirect(url_for('login'))
#        return render_template('login.html')
    else:
        print 'user[%s] logined already'%user
        u = db_query_user(user)
        if u==None:
            print 'go home page failure'
            redirect(url_for('login'))
        rst = db_query_bmarks(user)
        for i in range(0, len(rst)):
            rst[i]['index']= i+1
        return render_template('home.html',name=user, bmarks=rst)

@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there session.pop('username', None)
    session.pop('username', None)
    return '<html><meta http-equiv="refresh" content="3;url=home"> <body><h3>logout success</h3></body></html>'

@app.route('/addbm',methods=['POST', 'GET'])
def addBookMark():
    if request.method=='POST':
        user = None
        if 'username' in session:
            user = session['username']
            u = db_query_user(user)
            if u==None:
                user = None
        if user == None:
            print 'user None while add bookmark'
            return redirect(url_for('login'))
        label = request.form['label']
        address = request.form['address']
        if label==None or address==None:
            return '<html><meta http-equiv="refresh" content="3;url=addbm"> <body> <h3>Hi, %s<br/>add bookmark failure</h3></body></html>' % user
        if not address.startswith('http://'):
            address = 'http://%s'%address
        db_insert_bookmark([user,label,address])
        return '<html><meta http-equiv="refresh" content="3;url=home"> <body> <h3>Hi, %s<br/>add bookmark success</h3></body></html>' % user
    else:
    
        return render_template('addbmark.html')

@app.route('/bmarkm',methods=['POST', 'GET'])
def bookmarkManage():
    if request.method=='POST':
        user = None
        if 'username' in session:
            user = session['username']
            u = db_query_user(user)
            if u==None:
                user = None
        if user == None:
            print 'user None while add bookmark'
            return redirect(url_for('login'))
        
#        label = request.form['label']
#        address = request.form['address']
        t_bm = {}
        print '--> form type: %s'%type(request.form)
        for i in request.form:
            v = request.form[i]
            t_bm[i]=v
            print '--%s :%s'%(i,v)
        
        label=t_bm['label']
        address=t_bm['address']
        
        if label==None or address==None:
            return '<html><meta http-equiv="refresh" content="3;url=addbm"> <body> <h3>Hi, %s<br/>operate failure</h3></body></html>' % user
        if not address.startswith('http://'):
            address = 'http://%s'%address
        
#        t_bm = dict(request.form)
        rst = None
        if 'delete' in request.form:
            # delete
            print 'delete ', label
            rst = db_delete_bmarks([t_bm])
        else:
            # edite
            
            rst = db_modify_bookmark(t_bm)
        if rst == None:
            return '<html><meta http-equiv="refresh" content="3;url=home"> <body> <h3>Hi, %s<br/>operate success</h3></body></html>' % user
        else:
            return '<html><meta http-equiv="refresh" content="3;url=home"> <body> <h3>Hi, %s<br/>operate failure %s</h3></body></html>' % (user,rst)
    else:
        user = None
        if 'username' in session:
            user = session['username']
            u = db_query_user(user)
            if u==None:
                user = None
        if user == None:
            print 'user None while add bookmark'
            return redirect(url_for('login'))
        bmarks = db_query_bmarks(user)
        for i in range(0, len(bmarks)):
            bmarks[i]['index']= i+1
        return render_template('bmarkManage.html', user=user, bookmarks=bmarks)

@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        user = request.form['userid']
        passwd = request.form['password']
        passwd2 = request.form['password2']
#        name = request.form['name']
        name = ''
        if user==None or passwd == None or passwd2==None:
            return 'Not illegal requst'
        if name== None:
            name = ''
        u = db_query_user(user)
        if not u==None:
            return '<html><meta http-equiv="refresh" content="3;url=register"> <body> <h3>USER [%s] exist already</h3></body></html>' % user
        if cmp(passwd,passwd2)!=0:
            return '<html><meta http-equiv="refresh" content="3;url=register"> <body> <h3>password verify failure</h3></body></html>'
        r = db_insert_user([user,name,passwd])
        if r==True:
            print 'insert user[%s] success'
            db_insert_bookmark([user,"eisp","http://eisp.idpbg.efoxconn.com"])
            db_insert_bookmark([user,"culture","http://culture.efoxconn.com"])
            session['username']=user
            return '<html><meta http-equiv="refresh" content="3;url=home"> <body> <h3>Hi, %s<br/>register success</h3></body></html>' % user
        else:
            print 'insert user[%s] failure'
            return '<html><meta http-equiv="refresh" content="5;url=register"> <body> <h3>register failure</br>%s</h3></body></html>' % r
    else:
        return render_template('register.html')


#@app.route('/setcookie', methods=['POST', 'GET'])
#def setcookie():
#    if request.method=='POST':
#        user= request.form['nm']
#        resp = make_response('''<html><body><a href="/getcookie">click to read the cookie</a></body></html>''')
#        resp.set_cookie('userID', user)
#        return resp
#
#@app.route('/getcookie')
#def getcookie():
#    name = request.cookies.get('userID')
#    return '<h1>welcome '+name+'</h1>'

if __name__ == "__main__":
    app.run(host='10.175.71.77', port=8088, debug=True)

"""
    Bookmark Hub -- save your bookmark & sharing with other people
    1. save button.
    2. manage page. create fold, edit and move BM.
    3. world BM, browse others' bookmark.

    """
