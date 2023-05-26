import requests
import re
import os

if __name__ == '__main__':
    #创建文件夹
    if not os.path.exists('./糗图'):
        os.mkdir('./糗图')
    url = 'https://tieba.baidu.com/f?kw=%F4%DC%CA%C2%B0%D9%BF%C6&fr=ala0&tpl=5&dyTabStr=MCwzLDIsNiwxLDQsNSw3LDgsOQ%3D%3D'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    response = requests.get(url=url, headers=headers)
    text = response.text
    ex = '<img .*? src="(.*?)" attr="70385" data-original=".*?">'
    imgSrc = re.findall(ex, text, re.S)
    print(imgSrc)

    '''
    for src in imgSrc:
        #拼接url
        src='https:'+src
        img_data=requests.get(url=src,headers=headers).content
        #生成图片名称     用/分隔开,选取倒数第一个字符串作为名字
        img_name=src.split('/')[-1]
        imgPath='./糗图'+img_name
        with open(imgPath,'wb',)as fp:
            fp.write(img_data)
            print(img_name,'ok!')
    '''




