import requests
from lxml import etree
import csv
import json

xpath1='//main/article/header/a[1]/@href'
xpath2='/html/body/div[2]/div[2]/ul/li[3]/span[2]/text()'

fp=open('map.csv','wt',newline='',encoding='utf-8')
writer=csv.writer(fp)
writer.writerow(('address','longitude','latitude'))

header={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
    }

def get_user_url(url):
    url_part='https://www.qiushibaike.com'
    res=requests.get(url,headers=header)
    selector=etree.HTML(res.text)
    url_infos=selector.xpath(xpath1)
    for url_info in url_infos:
        if url_info!=None:
            get_user_address(url_part+url_info)
        else:
            pass

def get_user_address(url):
    print(url)
    if url.find('user')!=-1:
        res=requests.get(url,headers=header)
        selector=etree.HTML(res.text)
        if selector.xpath(xpath2):
            address=selector.xpath(xpath2)
            get_geo(address[0].split('·')[0])
        else:
            pass
    else:
        pass

def get_geo(address):
    par={'address':address,'key':'cb649a25c1f81c1451adbeca73623251'}
    api='http://restapi.amap.com/v3/geocode/geo'
    res=requests.get(api,par)
    json_data=json.loads(res.text)
    try:
        geo=json_data['geocodes'][0]['location']
        longitude=geo.split(',')[0]
        latitude=geo.split(',')[1]
        writer.writerow((address,longitude,latitude))
    except IndexError:
        pass

if __name__=='__main__':
    urls=['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for i in range(1,36)]
    for url in urls:
        get_user_url(url)
    