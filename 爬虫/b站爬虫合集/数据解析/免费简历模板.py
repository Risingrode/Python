import requests
from lxml import etree

if __name__ == '__main__':
    url = ' https://sc.chinaz.com/jianli/free.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    page_text = response.text
    tree = etree.HTML(page_text)
    List = tree.xpath('//div[@id="main"]/div/div/a/@href')
    for li in List:
        li_url = 'https:' + li
        response2 = requests.get(url=li_url, headers=headers)
        response2.encoding = 'utf-8'
        page_text2 = response2.text
        tree2 = etree.HTML(page_text2)
        rec = tree2.xpath('//ul[@class="clearfix"]/li[1]/a/@href')[0]
        recName = tree2.xpath('//h1/text()')
        # print(rec,recName)
        recourse = requests.get(url=rec, headers=headers).content
        Path = './免费简历模板/' + str(recName[0]+'.rar')
        with open(Path, 'wb') as fp:
            fp.write(recourse)
        print(recName, '下载成功！')
