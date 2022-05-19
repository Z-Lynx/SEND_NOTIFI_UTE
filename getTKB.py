import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
from datetime import datetime, timedelta
from getAndCheckDB import *


def getTBK(mSV_Account):
    payload = {"maSV":mSV_Account}
    r = requests.Session()
    utf_8 = r.get('http://daotao.ute.udn.vn/svtkb.asp')
    page = r.post('http://daotao.ute.udn.vn/svtkb.asp',data=payload)
    page.encoding  = utf_8.apparent_encoding
    soup = BeautifulSoup(page.content,'html.parser')
    table_body = soup.select_one("#inner-column-container > div:nth-child(2) table:nth-of-type(1)")
    datas=[]
    rows = table_body.find_all('tr')
    name = soup.select("#inner-column-container > div:nth-of-type(2) p")[0].text.split('\n')[3].replace('&nbsp','').split(':')[-1]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        datas.append([ele for ele in cols if ele]) 

    return name,datas

def sendEmail(data):
    print(data[0],data[1])
    status,title,content= check_title(data[1],data[2])
    if status:
        send_mail(str(data[0])+"@sv.ute.udn.vn",title,content)

def autoSendMail():
    if os.path.exists('dags/test/data.csv'):
        df = pd.read_csv('dags/test/data.csv')
        df.apply(sendEmail,axis=1)
        print("[+] DONE SEND MAIL !!")
    else:
        print("[!] DATA CLEAR !!")

#autoSendMail()