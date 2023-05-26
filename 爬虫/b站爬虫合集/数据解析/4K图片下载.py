import requests
from lxml import etree

if __name__ == '__main__':
    url = 'https://pic.netbian.com/4kmeinv/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = 'gbk'
    page_all = response.text
    tree = etree.HTML(page_all)
    page_list = tree.xpath('//div[@class="page"]/a/@href')
    page = 2
    for pageurl in page_list:
        count = 1
        response = requests.get(url='https://pic.netbian.com' + pageurl, headers=headers)
        response.encoding = 'gbk'
        page_text = response.text
        treep = etree.HTML(page_text)
        beauty_list = treep.xpath('//div[@class="slist"]/ul/li')
        for li in beauty_list:
            imgSrc = 'https://pic.netbian.com' + li.xpath('./a/img/@src')[0]
            imgName = li.xpath('./a/img/@alt')[0] + '.jpg'
            print(imgName, imgSrc)
            res = requests.get(url=imgSrc, headers=headers).content
            imgPath = './4k美女/' + imgName
            with open(imgPath, 'wb') as fp:
                fp.write(res)
            count += 1
            print('第{}页,第{}张照片下载成功！'.format(page, count))
        if count ==20:break # 下载20张即可
        page += 1
