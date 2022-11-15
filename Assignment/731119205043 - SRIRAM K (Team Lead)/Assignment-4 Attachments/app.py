from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
app=Flask(__name__)
app.secret_key = 'a'
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rkk02660;PWD=MjT4FnHjLsN6rpbn",' ',' ')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/regis')
def regis():
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=' '
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM User WHERE username = ? AND password = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Logged in successfully!'
            return render_template('welcome.html',msg=msg)
        else:
            return render_template('login.html')
        
@app.route('/register',methods=['GET','POST'])
def register():
        if request.method=='POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            sql = "SELECT * FROM User WHERE username = ?"
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print(account)
            if account:
                return '{}'.format("Account already exist!")            
            else:
                insert_sql="INSERT INTO user VALUES(?, ?, ?)"
                prep_stmt=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,username)
                ibm_db.bind_param(prep_stmt,2,email)
                ibm_db.bind_param(prep_stmt,3,password)
                ibm_db.execute(prep_stmt)
                msg="You have successfully registered"
                return render_template('login.html',msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True, threaded=True)
