import requests
from bs4 import BeautifulSoup
import csv
from lxml import etree
import socket


SERVER_URL = 'http://www.a-hospital.com'
HOSPITAL_URL = '/w/全国医院列表'

def check_link(url):
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Cookie": "__utmz=118505753.1566788180.12.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=118505753; __utma=118505753.905048074.1564448522.1566885326.1566891827.19; __utmt=1; __utmb=118505753.12.10.1566891827",
               "Host": "www.a-hospital.com",
               "Upgrade-Insecure-Requests": "1"}
    try:
        r = requests.get(url, headers = headers)
        #print(r.text)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('********无法链接服务器！！！********')


def proxy_url(url):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("本机电脑名：", hostname)
    print("本机Ip：", ip)
    proxy_addr = "115.239.25.250:9999"

    proxies = {
        'http': 'http://125.123.137.255:9999',
        'https': 'https://115.239.25.250:9999',
    }

    url = 'https://httpbin.org/get'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "__utmz=118505753.1566788180.12.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=118505753; __utma=118505753.905048074.1564448522.1566885326.1566891827.19; __utmt=1; __utmb=118505753.12.10.1566891827",
        "Host": "www.a-hospital.com",
        "Upgrade-Insecure-Requests": "1"}
    try:
        r = requests.get(url, proxies=proxies, headers=headers, verify=False)
        print(r.text)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('********无法链接服务器！！！********')


def get_province(area_info):
    soup = BeautifulSoup(area_info, 'lxml')
    area = soup.find_all('p')
    for i in range(len(area)):
        if i % 2 == 1:
            url = area[i].find('a')
            if str(url) == 'None':
                print("no attrs...")
            else:
                out = open('hospital_city.csv', 'a', newline='', encoding='UTF-8')
                line = [url.text[:-4], url.get('href')]
                csv_write = csv.writer(out, dialect='excel')
                csv_write.writerow(line)


def writer_csv(file, line):
    out = open(file, 'a', newline='', encoding='UTF-8')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(line)


def reader_csv_list(file):
    data = []
    with open(file, encoding='UTF-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        csv_header = next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return data
    #birth_data = [[float(x) for x in row] for row in birth_data]  # 将数据从string形式转换为float形式
    #birth_data = np.array(birth_data)  # 将list数组转化成array数组便于查看数据结构


def get_city_dis_url(url):
    soup = check_link(SERVER_URL + url[1])

    html = etree.HTML(soup)
    icd_html = etree.tostring(html)
    html_data = html.xpath('//*[@id="bodyContent"]/p[2]')
    for i in html_data[0].findall('a'):
        line = [url[0], i.text, i.values()[0]]
        writer_csv('hospital_city_31.csv', line)


class TAG_TYPE(type):
    ADDR = "医院地址"
    LEVEL = "医院等级"
    TELE = "联系电话"
    JYFS = "经营方式"
    CZNO = "传真号码"
    WEB = "医院网站"
    EMAIL = "电子邮箱"
    ZDKS = "重点科室"


def get_hospital_info(url):
    print(SERVER_URL + url[2])
    soup = check_link(SERVER_URL + url[2])
    #soup = proxy_url(SERVER_URL + url[2])
    print(SERVER_URL + url[2])
    html = etree.HTML(soup)
    icd_html = etree.tostring(html)
    # 注意每个页面的不一定是ul[3]
    html_data = html.xpath('//*[@id="bodyContent"]/ul[3]')
    print(len(html_data[0].findall('li')))

    if(str(html_data[0].findall('li')[0].find('b')) == 'None'):
        print("页面特殊原因，进入另一个解析分支。。。")
        html_data = html.xpath('//*[@id="bodyContent"]/ul[4]')

    for i in html_data[0].findall('li'):
        if(str(i.find('b').find('a')) == 'None'):
            print("医院名称不按规定tag标识做特殊处理")
            hos_name = i.find('b').text
        else:
            hos_name = i.find('b').find('a').text

        details = i.find('ul').findall('li')
        hos_info = ['','','','','','','','']
        for detail in details:
            tag_name = detail.find('b').text
            tag_value = etree.tounicode(detail)[16:-6]

            if(tag_name == TAG_TYPE.ADDR):
                hos_info[0] = tag_value
            elif(tag_name == TAG_TYPE.LEVEL):
                hos_info[1] = tag_value
            elif(tag_name == TAG_TYPE.TELE):
                hos_info[2] = tag_value
            elif(tag_name == TAG_TYPE.CZNO):
                hos_info[3] = tag_value
            elif(tag_name == TAG_TYPE.EMAIL):
                hos_info[4] = tag_value
            elif (tag_name == TAG_TYPE.JYFS):
                hos_info[5] = tag_value
            elif(tag_name == TAG_TYPE.ZDKS):
                hos_info[6] = tag_value
            elif (tag_name == TAG_TYPE.WEB):
                hos_info[7] = "医学百科网"

        line = [url[0], url[1], hos_name, hos_info]
        print(line)
        writer_csv('hospital_info.csv', line)


if __name__ ==  '__main__':
    urli = []
    city_csv = 'hospital_city.csv'
    city_list = 'hospital_city_31_OK.csv'

    #area_info = check_link(SERVER_URL + HOSPITAL_URL)
    #已经获取到了各省份的医院列表清单
    #get_province(area_info)
    '''urli = reader_csv_list(city_csv)
    print(urli)
    for url in urli:
        get_city_dis_url(url)
        time.sleep(5)

    hos_urls = reader_csv_list(city_list)
    for hos_url in hos_urls:
        print(hos_url)
        #hos_url = ['测试市','测试区县','/w/%E6%97%A0%E9%94%A1%E5%B8%82%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8']
        get_hospital_info(hos_url)
        time.sleep(2)'''
