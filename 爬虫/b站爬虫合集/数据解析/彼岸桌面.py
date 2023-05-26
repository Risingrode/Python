import requests
import re
import os

if __name__ == '__main__':
    url = 'http://www.netbian.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    # content返回的是二进制形式的图片数据
    # text字符串    json对象
    page_str = 'http://www.netbian.com/index_%d.htm'
    for page in range(2,8):
        if not os.path.exists('./彼岸桌面/{}'.format(page)):
            os.mkdir('./彼岸桌面/{}'.format(page))
        new_url = format(page_str % page)
        response = requests.get(url=new_url, headers=headers)
        response.encoding = 'gbk'  # 指定编码方式
        #   re.S多行匹配    re.M单行匹配
        data = str(response.text)

        sc = '<li>.*?<img src="(.*?)" alt.*?</li>'
        List = re.findall(sc, data, re.S)
        count = 0
        for img in List:
            imgPicture = requests.get(url=img, headers=headers).content
            imgPath = './彼岸桌面/%d/' % page + str(count) + '.jpg'
            with open(imgPath, 'wb') as fp:
                fp.write(imgPicture)
                print('第{}页，第{}张图片下载完成！'.format(page, count))
                count += 1
