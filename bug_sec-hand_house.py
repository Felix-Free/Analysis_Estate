'''
Author:xihe
Time:2024/07
'''

import requests
import random
import time
import csv
#from fake_useragent import UserAgent
from lxml import etree

##创建文件对象
#a+表示以读写追加模式打开文件。文件指针位于文件末尾，可以读取和追加数据。如果文件不存在则创建新文件
f = open('E:/2024 Summer Semester/北京市安居客网二手房源信息.csv','a+',encoding='utf-8-sig',newline="")
csv_write = csv.DictWriter(f,fieldnames=['小区名称','小区地址','所属商圈','价格（元/m^2）','价格变化趋势','建造时间','容积率','绿化率','总户数','权属类别','物业类型','建筑类型','产权年限','供水供电','统一供暖','物业费','停车费','在售房源','在租房源'])
csv_write.writeheader() #写入文件头

##设置请求头参数：User-Agent、cookie、referer
# ua = UserAgent() 可能无效导致空表
'''
headers = {
    "user-agent": ua.random
}
'''
#建立有效ua池
'''
list = []
'''
headers = {
    #随机生成User-Agent
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    #网页的cookie
    "cookie": 'aQQ_ajkguid=81E01863-FB08-B973-81FB-SX0709142954; isp=true; id58=CrIW6maM2OSor3n5Sz+EAg==; 58tj_uuid=26e3059b-02f4-4bee-9586-11f1a417c0e0; als=0; xxzlclientid=3910e773-10e5-40a9-8a76-1720506597723; xxzlxxid=pfmx5T+D1pmVLap6kkQIozBUBImSi+Dj26R+rI186kSOGSBbNlkN4xYD5tdaCJ30wjh5; ajk-appVersion=; xxzlcid=024207b924d94025b679f7ccb040db16; xxzl-cid=024207b924d94025b679f7ccb040db16; ctid=14; lp_lt_ut=fe71475e46704a9d0f393860d2b55166; fzq_h=de8972af738f933cdd231f55b4907c60_1721041943089_efe6f65a43e246f2ac94000d94d84093_47924975365868980499202394456594315563; new_uv=18; sessid=60AC20B1-DBDF-44DE-A9A6-4A8B66500B83; ajk_member_verify=0erWyPdQkPhSU2cOPPAeqP%2FvuTjRr%2BIkYzgMyxsvizw%3D; ajk_member_verify2=MjkyNTAyMjYzfG9zeFFWQXd8MQ%3D%3D; twe=2; obtain_by=1; xxzlbbid=pfmbM3wxMDM0NnwxLjkuMHwxNzIxMDkyOTIzOTUxOTM2OTk2fFF1R1VxeGF3R3B2NzRiYVFMaDF6OVovUUZ2K1BRZWxWSkdmYXhmQ1plNUk9fDE3MTBmOWYwZmFiOGM0MTRmMTM5M2QzNGU3NTI0MzU4XzE3MjEwOTI5MjI2NDVfNDNkZTM5YThkYjE2NGUwMzg2NjA3MmVlMDQ0Zjk2YWZfMjAzMjMyMjY3OXxiYzEyNWJiNmRjZmUzNDZlNjkwNzYzMjE4M2ViNGIzOF8xNzIxMDkyOTIzMTMzXzI1NA==; xxzl_cid=024207b924d94025b679f7ccb040db16; xxzl_deviceid=hG6o4fBjYmDGzCL5Fgq9NbGMfhaOXRF70Am4paLfE4mUPjNYa3+5eGE5JgfB10J1; ajkAuthTicket=TT=120671f9edf924cfe0c3db3be00316c1&TS=1721092933431&PBODY=FNhni62h13c-vRILxiJNmczdo0a08-scxFbJRaNPXG491jvwc05QDjOqiEjHoJWpZfKoBS0KEBbp6cbyk8xniPj9WW8kGP23fu5bVUde4pOhrZZOELePnS9yWvjTDdoOH9Xd3_T7HnVVO7S52u-V3O46littTSjN8YQy6sP_ueQ&VER=2&CUID=twHg6rKFF-V2ls20ObipCBFWXp57TMBP; fzq_js_anjuke_ershoufang_pc=2d4b2c80955930a3b64f35673f558adb_1721092934921_24',
    #设置从何处跳转过来
    "referer": 'https://beijing.anjuke.com/sale/?'
}

## 解析一级页面函数
def get_link(url):
    try:
        text = requests.get(url=url, headers=headers).content
        html = etree.HTML(text)
        link = html.xpath('//*[@id="__layout"]/div/section/section[3]/section/div[2]/a/@href')

    except requests.exceptions.RequestException as e:
         print(f"请求错误: {e}")
         return []

    return link

def parse_message(url):
    dict_result = {'小区名称': '', '小区地址': '', '所属商圈': '', '价格（元/m^2）': '', '建造时间': '',
                   '容积率': '', '绿化率': '', '总户数': '', '权属类别': '', '物业类型': '', '建筑类型': '',
                   '产权年限': '','供水供电': '', '统一供暖': '', '物业费': '', '停车费': '', '在售房源': '','在租房源': '',}
    try:
        text = requests.get(url=url, headers=headers).text
        html = etree.HTML(text)

        # 解析新页面获取所需信息
        dict_result['小区名称'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[2]/div/h1/text()')
        dict_result['小区地址'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[2]/div/p/text()')
        dict_result['所属商圈'] = safe_xpath_extract(html, '//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[10]/div[2]/div[1]/text()')
        dict_result['价格（元/m^2）'] = safe_xpath_extract(html, '//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/span[1]/text()')
        dict_result['建造时间'] = safe_xpath_extract(html, '//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[1]/text()')
        dict_result['容积率'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[7]/div[2]/div[1]/text()')
        dict_result['绿化率'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[8]/div[2]/div[1]/text()')
        dict_result['总户数'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div[1]/text()')
        dict_result['权属类别'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[1]/text()')
        dict_result['物业类型'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]/text()')
        dict_result['建筑类型'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[9]/div[2]/div[1]/text()')
        dict_result['产权年限'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div[1]/text()')
        dict_result['供水供电'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[12]/div[2]/div[1]/text()')
        dict_result['统一供暖'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[11]/div[2]/div[1]/text()')
        dict_result['物业费'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[14]/div[2]/div[1]/text()')
        dict_result['停车费'] = safe_xpath_extract(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[15]/div[2]/text()')
        dict_result['在售房源'] = safe_xpath_extract_2(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[3]/div[1]/a//i/text()')
        dict_result['在租房源'] = safe_xpath_extract_2(html,'//*[@id="__layout"]/div/div[2]/div[3]/div[2]/div[1]/div[3]/div[2]/a//i/text()')

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        dict_result = None

    except Exception as e:
        print(f"解析页面出错: {e}")
        dict_result = None

    return dict_result

def safe_xpath_extract(html_tree, xpath_expression):
    try:
        result = html_tree.xpath(xpath_expression)
        if result:
            return result[0].strip()
        else:
            return '-'
    except:
        return '-'

def safe_xpath_extract_2(html_tree, xpath_expression):
    try:
        result = html_tree.xpath(xpath_expression)
        if result:
            return ''.join(result).strip()
        else:
            return '-'
    except:
        return '-'

## 将数据读取到csv文件中
def save_csv(result):
    for row in result:
        if row is not None:
            csv_write.writerow(row)

## main code
C = 1
k = 1  # 爬取房源条数

# 多页爬取
for i in range(1, 31):  # 每页25个小区，共50页，共1250个数据
    print("************************" + "第%s页开始爬取" % i + "************************")
    url = 'https://beijing.anjuke.com/community/p{}/'.format(i)

    # 解析一级页面函数,函数返回详情页URL和均价
    link = get_link(url)
    list_result = []  # 定义一个列表，存放每个小区字典数据

    for j in link:
        try:
            # 解析二级页面函数，分别传入详情页URL和均价两个参数
            result = parse_message(j)
            list_result.append(result)  # 将字典数据存入到列表中
            print("已爬取{}条数据".format(k))
            k = k + 1  # 控制爬取的小区数
            time.sleep(round(random.randint(1, 3), C))  # 设置睡眠时间间隔,控制两级页面访问时间
        except Exception as err:
            print("-----------------------------")
            print(err)

    # 保存数据到文件中
    save_csv(list_result)
    time.sleep(random.randint(1, 3))  # 设置睡眠时间间隔,控制一级页面访问时间

    print("************************" + "第%s页爬取成功" % i + "************************")
