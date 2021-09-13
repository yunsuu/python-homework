from flask import Flask, request
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


# 유저목록 조회 
@app.route("/userlist")
def getUserListRouter():
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    query = "SELECT * FROM users"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    result = []
    print(rows)
    for row in rows:
        result.append({'name': row[1], 'email': row[2]})
    return {
        'status': 'success',
        'result': result,
    }

# 유저목록 추가 (미완성)
@app.route("/adduser", methods=['POST'])
def postAddUserRouter():
    userName = request.form['name']
    userEmail = request.form['email']

    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    query = """INSERT INTO users(name, email) VALUES ('%s', '%s') 
    WHERE NOT EXISTS (SELECT * FROM users WHERE email='%s')""" % (userName, userEmail, userEmail)
    cur.execute(query)
    conn.commit()
    conn.close()
    return {
        'status': 'success',
    }

# 유저목록 변경
@app.route("/updateuser", methods=['PUT'])
def putUpdateUserRouter():
    userName = request.form['name']
    userEmail = request.form['email']
    newName = request.form['newName']
    newEmail = request.form['newEmail']

    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    query = """UPDATE users SET name='%s', email='%s'
WHERE name='%s' AND email='%s'""" % (newName, newEmail, userName, userEmail)
    cur.execute(query)
    print(cur.rowcount)
    if cur.rowcount > 0:
        conn.commit()
        conn.close()
        return {
            'status': 'success',
        }
    else:
        return {
            'status': 'fail',
        }

# 유저목록 삭제
@app.route("/deleteuser", methods=['DELETE'])
def deleteUserRouter():
    userName = request.form['name']
    userEmail = request.form['email']

    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()

    query = "DELETE FROM users WHERE name='%s' AND email='%s'" % (userName, userEmail)
    cur.execute(query)
    print(cur.rowcount)
    if cur.rowcount > 0:
        conn.commit()
        conn.close()
        return {
            'status': 'success',
        }
    else:
        conn.close()
        return {
            'status': 'fail',
        }

# 한개 이메일 보내기
#post
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
# post
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