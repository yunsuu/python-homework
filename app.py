from flask import Flask, request
import requests
import json
import multiprocessing
import sqlite3

app = Flask(__name__)


apiUrl = 'http://python.recruit.herrencorp.com/api/v1/mail'
apiUrl2 = 'http://python.recruit.herrencorp.com/api/v2/mail'


headers = {'Authorization': 'herren-recruit-python', 'Content-Type': 'application/x-www-form-urlencoded'}
headers2 = {'Authorization': 'herren-recruit-python', 'Content-Type': 'application/json'}

def sendMail(headers, mail, apiUrl):
    while True:
        response = requests.post(apiUrl, data=mail, headers=headers)
        result = json.loads(response.text)
        print(result['status'])
        if result['status'] == 'success':
            return True


# 유저목록 조회 
@app.route("/user-list")
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
@app.route("/add-user", methods=['POST'])
def postAddUserRouter():
    try: 
        userName = request.form['name']
        userEmail = request.form['email']
        conn = sqlite3.connect('mydb.db')
        cur = conn.cursor()
        query = """INSERT INTO users(name, email) VALUES ('%s', '%s') 
""" % (userName, userEmail)
        cur.execute(query)
        conn.commit()
        conn.close()
        return {
            'status': 'success',
        }
    except sqlite3.Error as error:
        errorMssage = ' '.join(error.args)
        print(errorMssage)
        print('SQLite error: %s' % (errorMssage))
        if errorMssage == 'UNIQUE constraint failed: users.email':
            return {
                'status': 'fail',
                'msg' : "sqlite error : 등록된 email이 있습니다. 새로운 이메일로 등록해주세요."
            }
        else:
            return {
                'status': 'fail',
                'msg' : "sqlite error!!!ß"
            }            

# 유저목록 변경
@app.route("/update-user", methods=['PUT'])
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
@app.route("/delete-user", methods=['DELETE'])
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
@app.route("/send-mail", methods=['POST'])
def postSendMailRouter():
    mailto = request.form['mailto']
    subject = request.form['subject']
    content = request.form['content']

    mail={
	"mailto": mailto,
	"subject": subject,
	"content": content
}
    try:    
        if 'gamil.com' in mail['mailto'] or 'naver.com' in mail['mailto']:
            response = sendMail(headers2, json.dumps(mail), apiUrl2)
        else:
            response = sendMail(headers, mail, apiUrl)
        if response == True:
            return {
                'status': 'success',
            }
        else:
            return {
                'status': 'fail',
            }
    except:
        return {
            'status': 'fail',
        }

# 다중 이메일 보내기
# post
@app.route("/send-mails-to-all", methods=['POST'])
def postSendMailsRouter():
    subject = request.form['subject']
    content = request.form['content']

    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    print(rows)
    conn.close()
    mails = []
    for row in rows:
        userEmail = row[2]
        mails.append({
	"mailto": userEmail,
	"subject": subject,
	"content": content
})

    # response = sendMail(headers=headers, mails=data, apiUrl=apiUrl)

    try:
        processes = []
        for mail in mails:
            # process = multiprocessing.Process(target=sendMail, args=(headers, mail, apiUrl))
            # process = multiprocessing.Process(target=sendMail, args=(headers2, json.dumps(mail), apiUrl2))
            if 'gamil.com' in mail['mailto'] or 'naver.com' in mail['mailto']:
                process = multiprocessing.Process(target=sendMail, args=(headers2, json.dumps(mail), apiUrl2))
                print(' 구글이나 네이버!')
            else:
                process = multiprocessing.Process(target=sendMail, args=(headers, mail, apiUrl))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        return {
                'status': 'success',
            }
    except:
        return {
                'status': 'fail',
            }

@app.route("/")
def getRootRouter():
    return "<p>서버가 정상적으로 켜졌습니다!</p>"