import AppCore
import platforms.bili as bilibili
import platforms.nyato as nyato
import output
import threading
import os
import json
import time
import argparse

def output_arg(str):
    print(str)
    return json.loads(str)

parser = argparse.ArgumentParser(description='漫展爬虫')
parser.add_argument('-load', action='store_true', default=False)
parser.add_argument('-analyse', action='store_true', default=True)
parser.add_argument('-output', nargs='+', default=['print'])
parser.add_argument('-area', type=int, default=370000)
args = parser.parse_args()

AppCore.init()
dataList = []

def getDataFromInternet():

    class RunThread(threading.Thread):
        def __init__(self, platform):
            threading.Thread.__init__(self)
            self.platform=platform
        def run(self):
            global dataList
            data = self.platform.get(AppCore,area=args.area)
            if(data): dataList.append(data)


    bilibiliThread = RunThread(bilibili)
    nyatoThread = RunThread(nyato)

    bilibiliThread.start()
    nyatoThread.start()

    bilibiliThread.join()
    nyatoThread.join()

    if(len(dataList[0])<len(dataList[1])):
        temp = dataList[0]
        dataList[0]=dataList[1]
        dataList[1]=temp

    try:
        with open('shows', 'w') as file:
            file.write(json.dumps(dataList))
    except Exception as e:
        pass

if(not args.load):
    try:
        with open('shows', 'r') as file:
            dataList = json.loads(file.read())
    except Exception as e:
        getDataFromInternet()
else: 
    getDataFromInternet()

if(args.analyse):
    finalShows = AppCore.fliterShow(dataList)
    output.output(finalShows,args.output)

input('任意键退出')