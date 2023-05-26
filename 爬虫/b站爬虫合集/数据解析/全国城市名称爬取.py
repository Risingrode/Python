import requests
from lxml import etree

if __name__ == '__main__':
    url = 'https://www.aqistudy.cn/historydata'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    response = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response)
    # list_top = tree.xpath('//div[@class="bottom"]/ul/li')
    # allCity = []
    # for top in list_top:
    #     top_city = top.xpath('./a/text()')[0]
    #     allCity.append(top_city)
    # list_city = tree.xpath('//div[@class="bottom"]/ul/div[2]/li')
    # for city in list_city:
    #     CName = city.xpath('./a/text()')[0]
    #     allCity.append(CName)
    # print(allCity)
    # print(len(allCity))

    #方法二：两种xpath模式合并
    #解析到热门城市与所有城市的a标签
    # 热门：div/ul/li/a    全部：div/ul/div[2]/li/a
    a_list=tree.xpath('//div[@class="bottom"]/ul/li/a | //div[@class="bottom"]/ul/div[2]/li/a')
    all_city=[]
    for a in a_list:
        city=a.xpath('./text()')
        all_city.append(city)
    print(all_city)
    print(len(all_city))
