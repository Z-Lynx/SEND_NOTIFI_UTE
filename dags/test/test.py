from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import sys
import os
from datetime import datetime, timedelta

os.system("cd /opt/airflow/dags/test")
sys.path.append('dags/test')

from getTKB import autoSendMail
def sendMail():
    autoSendMail()
    
default_args = {
        'owner': 'UTE_THONG_BAO_V1',
        'start_date': datetime(2019, 5, 16)
        }
dag = DAG('UTE_THONG_BAO_V1', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False)
t1 = BashOperator(
    task_id='crawl data thong bao',
    bash_command='cd /opt/airflow/dags/test && scrapy crawl thongbao',
    dag=dag)

t2 = PythonOperator(
    task_id='send mail',
    python_callable = sendMail,
    provide_context=True,
    dag = dag
)

t2 >> t1