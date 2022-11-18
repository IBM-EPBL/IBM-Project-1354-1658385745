from flask import Flask,render_template,request,redirect,url_for,session
from flask_mail import Mail, Message
from newsapi import NewsApiClient
import ibm_db
import re
app=Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '********@gmail.com'
app.config['MAIL_PASSWORD'] = '*******'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'a'
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=*******;PWD=**********",' ',' ')
global newsresource

@app.route('/')
def home():
        return render_template('login.html')

@app.route('/signup')
def signup():
        return render_template('signup.html')

@app.route('/forgot')
def forgot():
        return render_template('forgot.html')

@app.route('/dashboard')
def dashboard():
        if(session['loggedin']==True):
                return render_template('dashboard.html',username=session['fullname'])
        return render_template('login.html')       
    
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
                if account:
                        session['loggedin'] = True
                        session['id'] = account['USERNAME']
                        userid=  account['USERNAME']
                        session['username'] = account['USERNAME']
                        session['fullname']=account['FULLNAME']
                        session['email'] = account['EMAIL']
                        msg = 'Logged in successfully !'
                        return render_template('dashboard.html',username=session['fullname'])
                else:
                        msg = 'Incorrect username / password !'
                return render_template('login.html',msg=msg)
        
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
                        msg="Email id already exist!"                     
                elif userexist:
                        msg="Username id already exist!"
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
                return render_template('signup.html',msg=msg)
            
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
                        msg="Login credentials sent to your mail succcessfully....."
                        email='   '
                        return render_template('login.html',msg=msg)
                else:
                        msg="Email id not found."
                        return render_template('forgot.html',msg=msg)
        
@app.route('/news',methods=['GET','POST'])
def news():
        newsapi = NewsApiClient(api_key="*************")
        if request.method == 'POST':
                if(request.form['newsresource']=="google"):
                        newsresource="google-news-in"
                        msg="GOOGLE NEWS"
                elif(request.form['newsresource']=="bbc"):
                        newsresource="bbc-news"
                        msg="BBC NEWS"
                elif(request.form['newsresource']=="toi"):
                        newsresource="the-times-of-india"
                        msg="Times of India"
                elif(request.form['newsresource']=="abc"):
                        newsresource="abc-news"
                        msg="ABC NEWS"
        topheadlines = newsapi.get_top_headlines(sources=newsresource) 
        articles = topheadlines['articles'] 
        news = []
        author = []
        publishedAt=[]
        desc=[]
        img = []
        content=[]
        url=[]
        for i in range(len(articles)):
                myarticles = articles[i]
                news.append(myarticles['title'])
                author.append(myarticles['author'])
                publishedAt.append(myarticles['publishedAt'])
                desc.append(myarticles['description'])
                img.append(myarticles['urlToImage'])
                content.append(myarticles['content'])
                url.append(myarticles['url'])
                mylist = zip(news, author,publishedAt, desc,img,content,url)
        return render_template('news.html', context = mylist)

@app.route('/logout')
def logout():
        session['loggedin']=False
        session.pop('id', None)
        session.pop('username', None)
        msg="Logged out successfully......"
        return render_template('login.html',msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
