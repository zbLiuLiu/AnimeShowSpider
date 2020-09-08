import random
import time
import traceback

AppCore=None
def _loadBili(page,version,pagesize,area):
    time.sleep(random.randint(1,10))
    response = AppCore.request('https://show.bilibili.com/api/ticket/project/listV2?version='+str(version)+'&page='+str(page)+'&pagesize='+str(pagesize)+'&area='+str(area)+'&filter=&platform=web&p_type=%E5%85%A8%E9%83%A8%E7%B1%BB%E5%9E%8B')['data']
    numPages = response['numPages']
    shows = response['result']
    result = []
    for show in shows:
        try:
            time.sleep(random.randint(1,5))
            url = 'https://show.bilibili.com/api/ticket/project/get?version='+str(version)+'&id='+str(show['id'])
            detail = AppCore.request(url)['data']
            result.append(
                {
                    'name':detail['name'],
                    'location':{
                        'province':detail['venue_info']['province_name'],
                        'city':detail['venue_info']['city_name'],
                        'district':detail['venue_info']['district_name'],
                        'name':detail['venue_info']['name'],
                        'address_detail':detail['venue_info']['address_detail']
                    },
                    'start_time': detail['start_time'],
                    'end_time': detail['end_time'],
                    'price_low': detail['price_low'],
                    'price_high': detail['price_high'],
                    'sale_flag': detail['sale_flag'],
                    'wish': detail['wish_info']['count'],
                    'is_free': detail['is_free'],
                    'is_price': detail['is_price'],
                    'url': 'https://show.bilibili.com/platform/detail.html?id='+str(show['id']),
                    'platform':'bilibili'
                }
            )
        except Exception as e:
            traceback.print_exc()
    data = {
        'result':result,
        'numPages':numPages
    }
    # print(data)
    return data

def get(core,settedNumPages=None,version=134,pagesize=16,area=-1):
    global AppCore
    if(area==0): area=-1
    AppCore=core
    print('正在从哔哩哔哩会员购获取展会信息...')
    numPages=settedNumPages or 1
    data=[]
    page=0
    while page<numPages:
        try:
            result=_loadBili(page+1,version,pagesize,area)
            if((not settedNumPages) or settedNumPages>result['numPages']): numPages=result['numPages']
            print('正在从哔哩哔哩会员购获取展会信息...(%d/%d)'%(page+1,numPages))
            data+=result['result']
        except Exception as e:
            traceback.print_exc()
            print('第%d页加载失败'%(page+1))
        page+=1
    return data