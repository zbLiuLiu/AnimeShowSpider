import pandas as pd
import time
import os
from prettytable import PrettyTable

file = {
    'path':'',
    'name':'output'
}

fileName = ''

def _check_path():
    global file
    if (len(file['path'])==0): return
    if (not os.path.isdir(file['path'])):
        os.makedirs(file['path'])

def _print(header,data):
    table = PrettyTable(header)
    for item in data:
        table.add_row(item)
    print(table)

def _csv(header,data):
    global fileName
    _check_path()
    table=pd.DataFrame(columns=header,data=data)
    table.to_csv(fileName+'.csv')

def _excel(header,data):
    global fileName
    _check_path()
    table=pd.DataFrame(columns=header,data=data)
    table.to_excel(fileName+'.xls', sheet_name='Sheet1')

def _excel2010(header,data):
    global fileName
    _check_path()
    table=pd.DataFrame(columns=header,data=data)
    table.to_excel(fileName+'.xlsx', sheet_name='Sheet1')

def output(inputData,request):
    global file
    global fileName
    fileName = file['path']+file['name']+' - '+time.asctime( time.localtime(time.time())).replace(':','_').replace(' ','_')
    header = ['漫展名称','意向人数','地址','开始时间','结束时间','网址']
    data = []
    for show in inputData:
        data.append([show['name'],show['wish'],' '.join([show['location'][key] for key in ['province','city','district','name']]),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(show['start_time'])),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(show['end_time'])),show['url']])
    
    if('print' in request): _print(header,data)
    if('csv' in request): _csv(header,data)
    if('excel' in request): _excel(header,data)
    if('excel2010' in request): _excel2010(header,data)
    