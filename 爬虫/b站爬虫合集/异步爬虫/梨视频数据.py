import requests
from lxml import etree
import re
from multiprocessing.dummy import Pool

'''
注意：由于有反爬机制，该项目运行不了
'''


# 线程池处理的是阻塞且耗时的操作

url = 'https://www.pearvideo.com/category_1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
}
page_text = requests.get(url=url, headers=headers).text
tree = etree.HTML(page_text)
video_list = tree.xpath('//ul[@id="listvideoListUl"]//li')
urls = []  # 存储所有视频链接    和名字
for li in video_list:
    detail_url = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
    video_name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'
    print(video_name, detail_url)
    detail_page = requests.get(url=detail_url, headers=headers).text
    # 从详情页中解析视频地址
    # input()#用于暂停
    ex = 'src=(.*?)></video>'
    video_url = re.findall(ex, detail_page)
    packet = {
        'name': video_name,
        'url': video_url
    }
    urls.append(packet)


def get_video(dic):
    print(dic['name'], '该视频正在下载')
    video_src = requests.get(url=dic['url'], headers=headers).content
    with open('./梨视频/' + dic['name'], 'wb') as fp:
        fp.write(video_src)
        print(dic['name'], '该视频下载成功')


# 使用线程池对数据进行请求
pool = Pool(len(urls))
pool.map(get_video, urls)

pool.close()
pool.join()
