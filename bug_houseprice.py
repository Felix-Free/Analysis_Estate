'''
Author:xihe
Time:2024/07
'''


import requests
import random
import time
import csv
#from fake_useragent import UserAgent
from urllib.parse import urljoin
from lxml import etree

##创建文件对象
#a+表示以读写追加模式打开文件。文件指针位于文件末尾，可以读取和追加数据。如果文件不存在则创建新文件
f = open('E:/2024 Summer Semester/北京市安居客网房源信息.csv','a+',encoding='utf-8-sig',newline="")
csv_write = csv.DictWriter(f,fieldnames=['楼盘名','户型','面积','价格','区域位置','楼盘地址','建筑类型','产权年限','容积率','绿化率','规划户数','车位数','物业类型','物业管理费'])
csv_write.writeheader() #写入文件头

##设置请求头参数：User-Agent、cookie、referer
# ua = UserAgent() 可能无效导致空表
#建立有效ua池
'''
list = []
'''
headers = {
    #随机生成User-Agent
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    #网页的cookie
    "cookie": 'aQQ_ajkguid=81E01863-FB08-B973-81FB-SX0709142954; id58=CgAEEmaM2OMkeXNwFKD+Ag==; isp=true; id58=CrIW6maM2OSor3n5Sz+EAg==; 58tj_uuid=26e3059b-02f4-4bee-9586-11f1a417c0e0; als=0; xxzlclientid=3910e773-10e5-40a9-8a76-1720506597723; xxzlxxid=pfmx5T+D1pmVLap6kkQIozBUBImSi+Dj26R+rI186kSOGSBbNlkN4xYD5tdaCJ30wjh5; isp=true; wmda_uuid=2176bc3cfa0230db027f55ce78eb2967; wmda_new_uuid=1; wmda_visited_projects=%3B8788302075828; ajk-appVersion=; ctid=14; sessid=9F3B6085-5FDE-D505-2B34-7FAB2CE6996D; obtain_by=2; twe=2; xxzlcid=024207b924d94025b679f7ccb040db16; xxzl-cid=024207b924d94025b679f7ccb040db16; fzq_h=8e20a14d4bc4ba75619b5af2fd7d7dda_1720944167057_d1ff14422baa4d3693a4e8538cdadf66_47924975365868980499202394456594315563; wmda_session_id_8788302075828=1720962389986-6926441f-52ff-8a1b; ved_loupans=523013%3A526233%3A521885%3A526616%3A519195%3A514048%3A526443%3A520966%3A445007%3A495363%3A520968%3A456503%3A526398%3A521893; init_refer=https%253A%252F%252Fbj.fang.anjuke.com%252Floupan%252Fall%252F; new_uv=8; new_session=0; lp_lt_ut=e7e94e5eab3a27ccacec61974465f3e4; xxzl_cid=ff446844ea4c440c918f7b344c9a554d; xxzl_deviceid=/6u4VocYYq50cYyCB8Is0Fj3Zf12ZZvyaM2ysBHw2R/MtqvC8NQznj8BSFxAuluz; xxzlbbid=pfmbM3wxMDMyMnwxLjkuMXwxNzIwOTY0OTU4NDMxNTU1MTIyfDNPT1laejF1VWZINmFJUjFiZ0EyajNqZHBtQmdKZXZ6aENSLzFhOTQrWTA9fGI3ZGY0ZmI3Y2U0ZTc2MjVmZTZlYzhhMGI0NDA2MmNmXzE3MjA5NjQ5NTc5MzZfOWQxMDAyNmI3ZGMzNDY3ZWFhYWEwZDRlMWRjY2MwMjVfMjAzMjMyMjY3OXw2Mjg3ZjA5NDQ2OWNmMTQ3NWMxMGZhYmNlZGNjZjc1YV8xNzIwOTY0OTU3NzU0XzI1Ng==',
    #设置从何处跳转过来
    "referer": 'https://bj.fang.anjuke.com/?from=HomePage_TopBar',
}

## 解析一级页面函数
def get_link(url):
    try:
        text = requests.get(url=url, headers=headers).text
        html = etree.HTML(text)
        link = html.xpath('//*[@id="container"]/div[2]/div[1]/div[3]//div/@data-link')
        area = html.xpath('//*[@id="container"]/div[2]/div[1]/div[3]//div/a[3]/span[@class="building-area"]/text()')


    except requests.exceptions.RequestException as e:
         print(f"请求错误: {e}")
         return []

    return list(zip(link, area))

## 解析二级页面函数
def parse_message(url,area):
    dict_result = {'楼盘名':'-','户型':'-','面积':'-','价格':'-','区域位置':'-','楼盘地址':'-','建筑类型':'-',
                   '产权年限':'-','容积率':'-','绿化率':'-','规划户数':'-','车位数':'-','物业类型':'-','物业管理费':'-'}
    try:
        text = requests.get(url=url, headers=headers).text
        html = etree.HTML(text)

        dict_result['户型'] = safe_xpath_extract_2(html,'//*[@id="container"]/div[1]/div[2]/div[1]/dl/dd[4]/div//a/text()')
        dict_result['价格'] = safe_xpath_extract_2(html,'//*[@id="container"]/div[1]/div[2]/div[1]/dl/dd[1]/p//text()')

        # 需要点击链接才能获取更详细信息
        link_to_click = html.xpath('//*[@id="header"]/div[3]/div/ul/li[2]/a/@href')
        if link_to_click:
            new_url = urljoin(url, link_to_click[0])
            new_text = requests.get(url=new_url, headers=headers).text
            new_html = etree.HTML(new_text)

            # 解析新页面获取所需信息
            dict_result['楼盘名'] = safe_xpath_extract(new_html,
                                                       '//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[div[contains(text(),"楼盘名称")]]/div[2]/a/text()')
            dict_result['物业类型'] = safe_xpath_extract(new_html,
                                                         '//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[div[contains(text(),"物业类型")]]/div[2]/text()')
            dict_result['区域位置'] = safe_xpath_extract(new_html,
                                                         '//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[div[contains(text(),"区域位置")]]/div[2]/text()')
            dict_result['楼盘地址'] = safe_xpath_extract(new_html,
                                                         '//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[div[contains(text(),"楼盘地址")]]/div[2]/text()')
            dict_result['建筑类型'] = safe_xpath_extract(new_html,
                                                         '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"建筑类型")]]/div[2]/text()')
            dict_result['产权年限'] = safe_xpath_extract(new_html,
                                                         '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"产权年限")]]/div[2]/text()')
            dict_result['容积率'] = safe_xpath_extract(new_html,
                                                       '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"容积率")]]/div[2]/text()')
            dict_result['绿化率'] = safe_xpath_extract(new_html,
                                                       '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"绿化率")]]/div[2]/text()')
            dict_result['规划户数'] = safe_xpath_extract(new_html,
                                                         '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"规划户数")]]/div[2]/text()')
            dict_result['车位数'] = safe_xpath_extract(new_html,
                                                       '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"车位数")]]/div[2]/text()')
            dict_result['物业管理费'] = safe_xpath_extract(new_html,
                                                           '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[div[contains(text(),"物业管理费")]]/div[2]/text()')

        dict_result['面积'] = area

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
'''
# 主函数
C = 1
k = 1  # 爬取房源条数
print("************************第1页开始爬取************************")
# 第一页URL
url = 'https://bj.fang.anjuke.com/?from=HomePage_TopBar'
# 解析一级页面函数,函数返回详情页URL、价格、面积、户型
link = get_link(url)
list_result = []  # 将字典数据存入到列表中
for j in link:
    try:
        # 解析二级页面函数，分别传入详情页URL和均价两个参数
        result = parse_message(j[0],j[1])
        list_result.append(result)
        print("已爬取{}条数据".format(k))
        k = k + 1  # 控制爬取的小区数
        time.sleep(round(random.randint(5, 10), C))  # 设置睡眠时间间隔
    except Exception as err:
        print("-----------------------------")
        print(err)
# 保存数据到文件中
save_csv(list_result)
print("************************第1页爬取成功************************")
'''
## main code
C = 1
k = 1  # 爬取房源条数

# 多页爬取
for i in range(1, 11):  # 每页60个小区，600个
    print("************************" + "第%s页开始爬取" % i + "************************")
    url = 'https://bj.fang.anjuke.com/loupan/all/p{}/'.format(i)

    # 解析一级页面函数,函数返回详情页URL和均价
    link = get_link(url)
    list_result = []  # 定义一个列表，存放每个小区字典数据

    for j in link:
        try:
            # 解析二级页面函数，分别传入详情页URL和均价两个参数
            result = parse_message(j[0], j[1])
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
