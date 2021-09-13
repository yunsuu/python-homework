from flask import Flask
import requests
import json
import multiprocessing
import sqlite3

app = Flask(__name__)

def sendMail(headers, mails, apiUrl):
    while True:
        response = requests.post(apiUrl, data=mails, headers=headers)
        result = json.loads(response.text)
        print(result['status'])
        if result['status'] == 'success':
            return True


# 한개 이메일 보내기
@app.route("/sendmail")
def sendMailApi():

    apiUrl = 'http://python.recruit.herrencorp.com/api/v1/mail'

    headers = {'Authorization': 'herren-recruit-python', 'Content-Type': 'application/x-www-form-urlencoded'}
    mail={
	"mailto": "mail recever1",
	"subject": "mail title",
	"content": "massage"
}
    response = sendMail(headers=headers, mails=mail, apiUrl=apiUrl)

    return "<p>Hello, World!</p>"

# 다중 이메일 보내기
@app.route("/sendmails")
def sendMailsApi():
    # conn = sqlite3.connect('mydb.db')
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM users")
    # rows = cur.fetchall()

    apiUrl = 'http://python.recruit.herrencorp.com/api/v1/mail'

    headers = {'Authorization': 'herren-recruit-python', 'Content-Type': 'application/x-www-form-urlencoded'}
    mails=[{
	"mailto": "mail recever1",
	"subject": "mail title",
	"content": "massage"
}, {
	"mailto": "mail recever2",
	"subject": "mail title",
	"content": "massage"
}, {
	"mailto": "mail recever3",
	"subject": "mail title",
	"content": "massage"
}]
    # response = sendMail(headers=headers, mails=data, apiUrl=apiUrl)

    processes = []
    
    for mail in mails:
        process = multiprocessing.Process(target=sendMail, args=(headers, mail, apiUrl))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return "<p>Hello, World!</p>"

@app.route("/")
def hello_world():
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    print(rows)
    return "<p>Hello, World!</p>"