from flask import Flask,render_template,request,redirect,url_for,session
from flask_mail import Mail, Message
import ibm_db
import re
app=Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cad.newstracker@gmail.com'
app.config['MAIL_PASSWORD'] = '**********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'a'
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=******;PWD=********",' ',' ')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=' '
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM NTAAC WHERE username = ? AND password = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template('dashboard.html')
        else:
            return render_template('login.html')
        
@app.route('/register',methods=['GET','POST'])
def register():
        if request.method=='POST':
            fullname = request.form['fullname']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            queryone = "SELECT * FROM NTAAC WHERE username = ? "
            stmtone = ibm_db.prepare(conn,queryone)
            ibm_db.bind_param(stmtone,1,username)
            ibm_db.execute(stmtone)
            userexist = ibm_db.fetch_assoc(stmtone)
            querytwo = "SELECT * FROM NTAAC WHERE email = ? "
            stmtwo = ibm_db.prepare(conn,querytwo)
            ibm_db.bind_param(stmtwo,1,email)
            ibm_db.execute(stmtwo)
            emailexist = ibm_db.fetch_assoc(stmtwo)
            if emailexist:
                return render_template('signup.html')
            if userexist:
                return render_template('signup.html')
            else:
                insert_sql="INSERT INTO NTAAC VALUES(?, ?, ?, ?)"
                prep_stmt=ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,fullname)
                ibm_db.bind_param(prep_stmt,2,email)
                ibm_db.bind_param(prep_stmt,3,username)
                ibm_db.bind_param(prep_stmt,4,password)
                ibm_db.execute(prep_stmt)
                msg = Message('CAD-NEWSTRACKER Account Created Successfully',sender ='cad.newstracker@gmail.com',recipients = [email]) 
                msg.body = ("Welcome to CAD-NEWSTRACKER, your account was successfully registered with us."+"\n\n\n"+"Your login credentials are:"+"\n\n"+"Username: "+username+"\n"+"Password: "+password+"\n\n\n"+"Happy Reading........"+"\n\n\n\n"+"With regard,"+"\n"+"CAD-NEWSTRACKER")
                mail.send(msg)
                return render_template('newaccount.html')
            
@app.route('/recover',methods=['GET','POST'])
def recover():
        if request.method=='POST':
            email = request.form['email']
            query = "SELECT * FROM NTAAC WHERE email = ? "
            stmt = ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,email)
            ibm_db.execute(stmt)
            emailexist = ibm_db.fetch_assoc(stmt)
            if emailexist:
                queryone=("SELECT * FROM NTAAC WHERE EMAIL =?")
                stmtone = ibm_db.prepare(conn,queryone)
                ibm_db.bind_param(stmtone,1,email)
                ibm_db.execute(stmtone)
                credentials = ibm_db.fetch_assoc(stmtone)
                username=str(credentials['USERNAME'])
                password=str(credentials['PASSWORD'])
                msg = Message('CAD-NEWSTRACKER Login Credentials',sender ='cad.newstracker@gmail.com',recipients = [email]) 
                msg.body = ("Request for sending your login credentials was completed successfully."+"\n\n\n"+"Your login credentials are:"+"\n\n"+"Username: "+username+"\n"+"Password: "+password+"\n\n\n"+"Happy Reading........"+"\n\n\n\n"+"With regard,"+"\n"+"CAD-NEWSTRACKER")
                mail.send(msg)
                return render_template('login.html')
            else:
                return render_template('forgot.html')                

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True, threaded=True)
