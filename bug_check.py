'''
Author:xihe
Time:2024/07
'''
import json

import requests
import random
import time
import csv
from fake_useragent import UserAgent
from urllib.parse import urljoin
from lxml import etree
from lxml import html
from urllib import parse
##设置请求头参数：User-Agent、cookie、referer
ua = UserAgent()
headers = {
    #随机生成User-Agent
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    #网页的cookie
    "cookie": 'aQQ_ajkguid=81E01863-FB08-B973-81FB-SX0709142954; isp=true; id58=CrIW6maM2OSor3n5Sz+EAg==; 58tj_uuid=26e3059b-02f4-4bee-9586-11f1a417c0e0; als=0; xxzlclientid=3910e773-10e5-40a9-8a76-1720506597723; xxzlxxid=pfmx5T+D1pmVLap6kkQIozBUBImSi+Dj26R+rI186kSOGSBbNlkN4xYD5tdaCJ30wjh5; ajk-appVersion=; xxzlcid=024207b924d94025b679f7ccb040db16; xxzl-cid=024207b924d94025b679f7ccb040db16; ctid=14; lp_lt_ut=fe71475e46704a9d0f393860d2b55166; fzq_h=de8972af738f933cdd231f55b4907c60_1721041943089_efe6f65a43e246f2ac94000d94d84093_47924975365868980499202394456594315563; new_uv=18; sessid=60AC20B1-DBDF-44DE-A9A6-4A8B66500B83; ajk_member_verify=0erWyPdQkPhSU2cOPPAeqP%2FvuTjRr%2BIkYzgMyxsvizw%3D; ajk_member_verify2=MjkyNTAyMjYzfG9zeFFWQXd8MQ%3D%3D; twe=2; obtain_by=1; xxzlbbid=pfmbM3wxMDM0NnwxLjkuMHwxNzIxMDkyOTIzOTUxOTM2OTk2fFF1R1VxeGF3R3B2NzRiYVFMaDF6OVovUUZ2K1BRZWxWSkdmYXhmQ1plNUk9fDE3MTBmOWYwZmFiOGM0MTRmMTM5M2QzNGU3NTI0MzU4XzE3MjEwOTI5MjI2NDVfNDNkZTM5YThkYjE2NGUwMzg2NjA3MmVlMDQ0Zjk2YWZfMjAzMjMyMjY3OXxiYzEyNWJiNmRjZmUzNDZlNjkwNzYzMjE4M2ViNGIzOF8xNzIxMDkyOTIzMTMzXzI1NA==; xxzl_cid=024207b924d94025b679f7ccb040db16; xxzl_deviceid=hG6o4fBjYmDGzCL5Fgq9NbGMfhaOXRF70Am4paLfE4mUPjNYa3+5eGE5JgfB10J1; ajkAuthTicket=TT=120671f9edf924cfe0c3db3be00316c1&TS=1721092933431&PBODY=FNhni62h13c-vRILxiJNmczdo0a08-scxFbJRaNPXG491jvwc05QDjOqiEjHoJWpZfKoBS0KEBbp6cbyk8xniPj9WW8kGP23fu5bVUde4pOhrZZOELePnS9yWvjTDdoOH9Xd3_T7HnVVO7S52u-V3O46littTSjN8YQy6sP_ueQ&VER=2&CUID=twHg6rKFF-V2ls20ObipCBFWXp57TMBP; fzq_js_anjuke_ershoufang_pc=2d4b2c80955930a3b64f35673f558adb_1721092934921_24',
    #设置从何处跳转过来
    "referer": 'https://beijing.anjuke.com/sale/?',
}

# 示例页面的 URL
url = 'https://beijing.anjuke.com/community/view/53107'


# 发起请求获取页面内容
response = requests.get(url=url,headers=headers)
response.encoding = 'utf-8'
content = response.content

print('Status Code:', response.status_code)  # 输出状态码

# 使用 lxml 解析 HTML
tree = html.fromstring(content)

# 使用 XPath 选取元素

elements_list = tree.xpath('//*[@id="__layout"]/div/div[2]/div[2]/div/h1/text()')
elements = ''.join(elements_list).strip()
results = elements.encode('iso-8859-1').decode('utf-8')
#link = tree.xpath('//*[@id="__layout"]/div/section/section[3]/section/div[2]//a/@href')
# 打印选取到的元素
print(results)

f = open('E:/2024 Summer Semester/北京市安居客网二手房源信息.csv','w',encoding='utf-8-sig',newline="")
csv_write = csv.DictWriter(f,fieldnames=['小区名称', '小区地址', '所属商圈', '价格（元/m^2）', '价格变化趋势',
                                              '建造时间', '容积率', '绿化率', '总户数', '权属类别',
                                              '物业类型', '建筑类型', '产权年限', '供水供电',
                                              '统一供暖', '物业费', '停车费', '在售房源', '在租房源'])
csv_write.writeheader() #写入文件头
