# 将验证码图片下载到本地
import requests
from lxml import etree
from chaojiying import Chaojiying_Client

# 封装识别验证码图片的函数
if __name__ == '__main__':
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63 '
    }
    session = requests.session()
    page_tetx = requests.get(url=url, headers=headers).text
    # 解析验证码图片img中的src属性
    tree = etree.HTML(page_tetx)
    # 获得验证码图片
    img_src = 'https://so.gushiwen.cn' + tree.xpath('//img[@id="imgCode"]/@src')[0]
    # print(img_src)
    img_data = requests.get(url=img_src, headers=headers).content
    with open('./code.jpg', 'wb') as fp:
        fp.write(img_data)
    # 调用打码平台的示例代码进行识别
    chaojiying = Chaojiying_Client('rising', 'cw123456', '938145')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('code.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    # print(chaojiying.PostPic(im, 1902))  # 1902 其返回机制是一个json类型
    code = chaojiying.PostPic(im, 1902)['pic_str']

    # 以下是登录
    data = {

        'from': 'http://so.gushiwen.cn/user/collect.aspx',
        'email': '3185087246@qq.com',
        'pwd': 'cw123456',
        'code': code,
        'denglu': '登录',
    }

    response = session.post(url=url, headers=headers, data=data)

    status = response.status_code
    print('状态码是：', status)
    main_text = response.text
    # print(main_text)
    # tree1=etree.HTML(main_text)
    # 爬取当前用户主页数据

    # 模拟登录成功
    detail_url = 'https://so.gushiwen.cn/user/collect.aspx'
    detail_text = session.get(url=detail_url, headers=headers).text
    with open('./gushiwen.html', 'w', encoding='utf-8') as fp:
        fp.write(detail_text)
