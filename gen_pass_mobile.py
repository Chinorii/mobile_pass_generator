# coding=utf-8
import requests
from lxml import etree
# mob_field=['134','135','136','137','138','139','147','150','151','152','157','158','159','187','188','182','183','184','178','198','130','131','132','145','155','156','176','176','185','186','166','146','133','153','149','173','177','180','181','189']

def get_headers():
    h = {
        "Host": "www.hiphop8.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-type": "application/json,charset=gb2312"
    }
    return h

def crawl_province():
    headers = get_headers()
    province_url="http://www.hiphop8.com/all.html"
    resp = requests.get(province_url,headers=headers)
    html = resp.content.decode('gb2312')
    page = etree.HTML(html)
    province_ele = page.xpath("//span/a/text()")
    for province in province_ele:
        print(province, end='\t')
    province_name = input("\nInput province name:").strip()
    if province_name != '':
        # //span/a[text()='北京']/../../following-sibling::ul/li/a/text()
        citypath=f"//span/a[text()='{province_name}']/../../following-sibling::ul[1]/li/a/text()"
        cities = page.xpath(citypath)
        if len(cities) != 0:
            for city in cities:
                print(city, end='\t')
            city = input("\nPrint city name, enter 'all' to generate all city:").strip()
            if city == 'all':
                cityurls_xpath = f"//span/a[text()='{province_name}']/../../following-sibling::ul[1]/li/a/@href"
                cityurls = page.xpath(cityurls_xpath)
                if len(cityurls) >0:
                    generate_phone_pass(cityurls)
            if city != '':
                cityurl_xpath=f"//span/a[text()='{province_name}']/../../following-sibling::ul[1]/li/a[text()='{city}']/@href"
                cityurl = page.xpath(cityurl_xpath)
                if len(cityurl) > 0:
                    generate_phone_pass(cityurl)
        else:
            print("City does not exist!")

def crawl_phone_head(cityurl):
    headers = get_headers()
    resp = requests.get(cityurl)
    html = resp.content.decode('gb2312','ignore')
    page = etree.HTML(html)
    phone_head_xpath = "//ul/li/a/text()"
    phone_head = page.xpath(phone_head_xpath)
    return phone_head


def generate_phone_pass(urls):
    filepath = input("\nInput file out path:")
    for url in urls:
        print(f"\nGenerating password from {url}...")
        phone_head_list = crawl_phone_head(url)
        # print(phone_head_list)
        with open(filepath,'a') as f:
            for phone_head in phone_head_list:
                for i in range(0,10000):
                    phonenum = phone_head + str("%04d" % i)+"\n"
                    f.write(phonenum)
                f.flush()
            
def start():
    crawl_province()

start()