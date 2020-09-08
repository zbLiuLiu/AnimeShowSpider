import time
import jieba

def _replace(str,char,arr):
    for item in arr:
        str.replace(item,char)
    return str

def target(doc):
    list = []
    for item in doc:
        list.append(test(item))
    return list

def test(item):
    result = [
        item['location']['province'],
        item['location']['city'],
        item['location']['district']
    ]
    replaceArray=['·','-','_','+','=','【','】','（','）','[',']','(',')']
    replaceArray+=result
    result+=[word for word in jieba.cut(_replace(item['name'].strip(),'',replaceArray),cut_all=False,HMM=True)]
    if(item['start_time']):
        timeArray = time.localtime(item['start_time'])
        timeText = time.strftime("%Y-%m-%d", timeArray)
        result.append(timeText)
    return result