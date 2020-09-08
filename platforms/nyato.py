import random
import time
import traceback
from bs4 import BeautifulSoup
# from html.parser import HTMLParser

# class NyatoParser(HTMLParser):
#     def __init__(self):
#         HTMLParser.__init__(HTMLParser)
#         self.numPages=1
#         self.result=[]
    
#     def handle_starttag(self, tag, attrs):


AppCore=None
def _loadNyato(page,area):
    time.sleep(random.randint(1,10))
    soup = BeautifulSoup(AppCore.request('https://www.nyato.com/manzhan/p'+str(area)+'?p='+str(page)),features='html.parser')
    result =  []
    for node in soup.find_all("li", class_="fl bg1 bordercolor boxsizing radius hidden cursor-bg"):
        time.sleep(random.randint(1,5))
        url = node.find("a", class_="fl cursor liti f16 line25 h50 hidden").attrs['href']
        detailSoup = BeautifulSoup(AppCore.request(url),features='html.parser')
        wish = detailSoup.find("div",class_="fr h40 line40 f12 s6")
        detailSoup = detailSoup.find("div",class_="w1200 ccbg expo-main pt10 pb20").find("div",class_="w720 fr")
        location = detailSoup.find("span",class_="fl mr10").get_text().replace('\n','').split(' ')
        times = detailSoup.find_all("div",class_="h25 line25 s6 f14 w100s mb10")[1].get_text().replace('\n','').split(' - ')
        saleFlag = '预售中'
        isFree = False
        price = ''.join(list(filter(str.isdigit,detailSoup.find("b",class_="f40").get_text().replace('\n',''))))
        startTime=None
        endTime=None
        if(len(price) == 0):
            price = 0
            isFree = True
        if(times[0]=='延期待定'):
            saleFlag = '延期中'
        elif (times[0]=='待定'):
            pass
        else:
            startTime = int(time.mktime(time.strptime(times[0], "%Y-%m-%d %H:%M")))
            endTime = int(time.mktime(time.strptime(times[1], "%Y-%m-%d %H:%M")))
        if(detailSoup.find("strong",class_="center fl f24")): saleFlag = detailSoup.find("strong",class_="center fl f24").get_text()
        result.append(
            {
                'name': detailSoup.find("h2",class_="f24 s5 mb5 w100s line50 bg-tit weight").get_text().replace('\n',''),
                'location': {
                    'province':location[0],
                    'city':location[1],
                    'district':location[2],
                    'name':location[3],
                    'address_detail':location[3]
                },
                'start_time':  startTime,
                'end_time':  endTime,
                'price_low': int(price),
                'sale_flag': saleFlag,
                'wish': int(''.join(list(filter(str.isdigit,wish.get_text().replace('\n',''))))),
                'is_free': isFree,
                'is_price': not isFree,
                'url': url,
                'platform':'nyato'
            }
        )
    numPages = soup.find("div",class_="cc w100s h50 page").find_all("a")
    numPages = int(''.join(list(filter(str.isdigit,numPages[len(numPages)-2].get_text().replace('\n','')))))
    data = {
        'result':result,
        'numPages':numPages
    }
    # print(data)
    return data

def get(core,settedNumPages=None,area=0):
    global AppCore
    if(area==-1): area=0
    AppCore=core
    print('正在从喵特获取展会信息...')
    numPages=settedNumPages or 1
    data=[]
    page=0
    while page<=numPages:
        try:
            result=_loadNyato(page+1,area)
            if((not settedNumPages) or settedNumPages>result['numPages']): numPages=result['numPages']
            print('正在从喵特获取展会信息...(%d/%d)'%(page+1,numPages))
            data+=result['result']
        except Exception as e:
            traceback.print_exc()
            print('第%d页加载失败'%(page+1))
        page+=1
    return data