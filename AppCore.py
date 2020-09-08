import urllib.request
import os
import time
import json
import urllib.parse
import gzip
import traceback
import urllib.error
import copy
import sameShowJudgement.pretreatment
import sameShowJudgement.coupon
import sameShowJudgement.analyse

wait=1
cookies={}

def request(url,debug=False):
    try:
        global wait
        global cookies
        parsed_tuple = urllib.parse .urlsplit(url)
        requestHeaders={
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'authority':parsed_tuple.netloc,
            'method':'get',
            'scheme':parsed_tuple.scheme,
            'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,yue-HK;q=0.5,yue;q=0.4,ja-JP;q=0.3,ko-KR;q=0.2,ko;q=0.1,ii-CN;q=0.1,ii;q=0.1,zh-TW;q=0.1',
            'cookie': cookies.get(parsed_tuple.netloc,""),
            'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        request=urllib.request.Request(url=url,headers=requestHeaders)
        if(debug): 
            print(requestHeaders)
            print('[AppCore] Request to '+request.full_url+':')
        response=urllib.request.urlopen(request)
        data = response.read()
        if(response.headers['Content-Encoding']=='gzip'): data=gzip.decompress(data).decode(response.headers.get_content_charset())
        else: data = data.decode(response.headers.get_content_charset())
        if(response.getheader('Set-Cookie') != None): cookies[parsed_tuple.netloc]=response.getheader('Set-Cookie')
        
        if(debug): 
            print('[AppCore]     Status: '+str(response.status))
            print('[AppCore]     Request Headers: ')
            for header in request.headers:
                print('[AppCore]        '+str(header)+': '+str(request.headers[header]))
            print('[AppCore]     Response Headers: ')
            for header in response.headers:
                print('[AppCore]        '+str(header)+': '+str(response.headers[header]))
            print('[AppCore]     Data')
            print('[AppCore]        '+str(data))
        
        try:
            data=json.loads(data)
        except Exception as e:
            pass
        time.sleep(wait)
        return data
    except urllib.error.URLError as e: 
        if(debug): 
            print('[AppCore]     URL ERROR: '+str(e.reason))
        raise e
    except urllib.error.HTTPError as e: 
        if(debug): 
            print('[AppCore]     HTTP ERROR: '+str(e.code)+' '+str(e.reason))
            for header in e.headers:
                print('[AppCore]        '+str(header)+': '+str(request.headers[header]))
        raise e

def init(waitingTime=1):
    global wait
    os.system('cls')
    print('漫展爬虫')
    wait=waitingTime
    time.sleep(wait)

def fliterShow(shows,debug=False):
    shows=copy.deepcopy(shows)
    target = sameShowJudgement.pretreatment.target(shows[0])
    sameShowJudgement.analyse.build(sameShowJudgement.coupon.build(target),sameShowJudgement.coupon.dictionary)
    for item in shows[1]:
        result = sameShowJudgement.analyse.analyse(sameShowJudgement.coupon.test(sameShowJudgement.pretreatment.test(item)))
        if(result[0][1]>=0.7):
            if(item['platform']=='nyato'): shows[1].remove(item)
            else: shows[0].pop(result[0][0])
        if(debug):
            print('----------------')
            print(item['name'])
            for i in range(0,10):
                print(' '+shows[0][result[i][0]]['name']+' - '+str(result[i][1]*100)+'%')
    if(debug): print('----------------')
    shows[0]+=shows[1]
    return shows[0]