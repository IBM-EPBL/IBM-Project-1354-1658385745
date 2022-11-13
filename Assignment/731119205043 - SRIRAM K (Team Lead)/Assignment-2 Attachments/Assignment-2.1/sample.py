from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		user_name = request.form['userName']
		email_id = request.form['emailId']
		phone_number = request.form['phoneNumber']
		return '{}{}{}{}{}{}'.format("<center><h1>Your user name is: ",user_name,"</h1><br><br><h2>Your email-id is: ",email_id,"</h2><br><br><h3>Your phone number is: ",phone_number,"</h3></center>")

if __name__ == '__main__':
	app.run('127.0.0.1',3890)
