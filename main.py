
from fastapi import FastAPI, Request,Form,status,BackgroundTasks
import time
import pandas as pd
import os
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List
from getTKB import getTBK
app = FastAPI()
app.mount(
    "/src",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "src"),
    name="src",
)
data_send_mail = []

def save_csv(data):
    print(data)
    if data:
        if os.path.exists('dags/test/data.csv'):
            print('a1')
            df = pd.read_csv('dags/test/data.csv')
            df2 = pd.DataFrame(data)
            df3 = df.append(df2)
            df3.to_csv('dags/test/data.csv',index= False)
        else:
            print('a')
            df2 = pd.DataFrame(data)
            df2.to_csv('dags/test/data.csv',index= False)

        
        df3 = pd.read_csv('dags/test/data.csv')
        df3 = df3.drop_duplicates(subset=['msv','id'])
        df3.to_csv('dags/test/data.csv',index= False)

    
templates = Jinja2Templates(directory="templates")

@app.get("/index/",response_class=HTMLResponse)
def index(request:Request):
    global data_send_mail
    data_send_mail = []
    datas =[]
    nameMSV = ""
    content = {'request': request,"datas" : datas,"name":nameMSV}
    return templates.TemplateResponse("index.html",content)

 
@app.get("/index/{name}",response_class=HTMLResponse)
def index(request:Request,name= "None"):
    try:
        global data_send_mail
        save_csv(data_send_mail)
        if name == "None":
            datas =[]
        else:
            try:
                nameMSV,datas = getTBK(name)
                content = {'request': request,"datas" : datas,"name":nameMSV,"id":name,"notifi":data_send_mail}
                data_send_mail = []
                return templates.TemplateResponse("index.html",content)
            except:
                return JSONResponse({"ERROR": "SAI MÃ SINH VIÊN", "Error Code":500}, status_code=500)
    except:
        return JSONResponse({"ERROR": "Bạn chưa nhập MSV !!", "Error Code":500}, status_code=500)

@app.post("/index/")
def index_form(request: Request,name : str = Form(...)):
    redirect_url = request.url_for('index')
    redirect_url += name
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER) 
   


@app.post("/checkbox")
def indexcheckbox(request: Request, val:List[str] = Form(...),id = Form(...)):
    global data_send_mail
    data_send_mail = []
    k = [x.split(',') for x in val]
    for x,y in k:
        data_send_mail.append({
            "msv" : id,
            "id" : x,
            "id_text":y ,
        })
    redirect_url = request.url_for('index')
    redirect_url += id
    try:
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER) 
    except:
        return JSONResponse({"ERROR": "Bạn chưa tích data để nhận thông báo !!", "Error Code":500}, status_code=500)
