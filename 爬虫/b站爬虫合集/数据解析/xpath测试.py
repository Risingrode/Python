
from lxml import etree

if __name__ == '__main__':
    #指定解析形式
    parser = etree.HTMLParser(encoding='gbk')
    # 实例化etree对象
    tree = etree.parse('彼岸桌面.html',parser=parser)
    # r=tree.xpath('/html/head/title')#返回值是一个对象
    # r = tree.xpath('/html//title')
    # r = tree.xpath('//div[@class="nav"]/a[3]/text()')[0]
    r = tree.xpath('//div[@class="nav"]/a[3]/@href')
    print(r)























