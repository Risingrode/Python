from lxml import etree
import requests

if __name__ == '__main__':
    url='https://www.baidu.com/s?wd='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70'
    }
    Input ='广场舞'

    response = requests.get(url=url+Input, headers=headers)
    response.encoding='utf-8'
    page_text = response.text
    print(page_text)
