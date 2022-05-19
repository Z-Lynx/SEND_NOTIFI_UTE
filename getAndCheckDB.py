from tabnanny import check
import mysql.connector
import smtplib
import os
import os
EMAIL_USER = "lynnbotdaotao@gmail.com"
EMAIL_PASS = "Kutega123@"
MYSQL_HOST = "172.20.0.1"
MYSQL_DB = "DAOTAO"
MYSQL_TABLE = "THONGBAO"
MYSQL_USER ="root"
MYSQL_PASSWORD = "airflow"
MYSQL_PORT = 3306
MYSQL_UPSERT = False
MYSQL_RETRIES = 3
MYSQL_CLOSE_ON_ERROR = True
MYSQL_CHARSET = 'utf8'

mydb = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DB
)

def check_notification(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM THONGBAO ORDER BY ID DESC LIMIT 5")
    myresult = mycursor.fetchall()
    for x in myresult:
        old_id,_,_ = x
        print(old_id)
        if int(id)== old_id:
            return True
    return False

def check_title(id,id_text):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM THONGBAO ORDER BY ID DESC LIMIT 80")
    myresult = mycursor.fetchall()
    for x in myresult:
        _,title,content = x
        if id in title or id_text in title:
            return True, title, content
    return False,_,_

def send_mail(reciver,title,content):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            subj = f"BOT DAOTAO PRO VJP 8212 EZ BY LYNN <> {title}"
            body = f"{content}"
            message  = f'Subject: {subj}\n\n{body}'
            server.sendmail(EMAIL_USER, reciver, message)
            server.close()
            print ('successfully sent the mail')
    except:
        print ("failed to send mail")

