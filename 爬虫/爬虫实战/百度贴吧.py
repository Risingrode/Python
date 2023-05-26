import json
import requests
import os
from lxml import etree

if __name__ == '__main__':
    url = 'https://tieba.baidu.com/hottopic/browse/topicList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding='utf-8'
    page_text = response.json()
    tree=etree.JSON(page_text)
    x=json.dumps(page_text)
    print(x)
    if not os.path.exists('./json文件'):
        os.mkdir('./json文件')
    with open('./json文件/baidu.text', 'w', encoding='utf-8') as fp:
        fp.write(str(page_text))
    # list=tree.xpath('./')
    list=tree.xpath('data')
    print(list)