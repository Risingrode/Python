import requests
from lxml import etree

# 需求：爬取58二手房中的数据
if __name__ == '__main__':
    url = 'https://www.58.com/ershoufang/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    page_text = requests.get(url=url, headers=headers).text
    # 数据解析
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="cleft"]//tr')
    fp=open('./xpath案例/58同城.txt','w',encoding='utf-8')
    for li in li_list:
        #img_url = li.xpath('//a/img/@src')
        home_text = li.xpath('./td/text()')
        #print(home_text)
        fp.write(str(home_text)+'\n')
    print('成功！')