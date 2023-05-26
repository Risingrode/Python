from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 把本地的html文档加载到该对象中
    fp = open('./彼岸桌面.html', 'r', encoding='gbk')
    soup = BeautifulSoup(fp, 'lxml')
    # print(soup)
    # soup 后面可以跟标签
    # print(soup.a)
    # print(soup.find('a'))#相当于soup.a
    # print(soup.find('div',class_='tabs_content'))#属性定位  也可以是其它属性
    # print(soup.find_all('a'))
    # print(soup.select('.bd'))
    # print(soup.select('.list>ul>li>a')[1])#第二个a标签
    # print(soup.select('.list>ul a')[1].text)
    # 以下两个为了展示string 与 text 的区别
    print(soup.select('.list>ul>li>a')[1].string)
    print(soup.select('.list>ul>li>a')[1].text)

    # 直接获取属性值
    print(soup.select('.list>ul a')[1]['href'])



