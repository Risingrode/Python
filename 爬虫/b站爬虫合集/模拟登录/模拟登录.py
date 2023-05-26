import requests
from lxml import etree
from ..验证码识别.chaojiying import Chaojiying_Client
# 如何模拟登录
# 验证码识别
# 先人工进入，然后获取data表单
# 可以用data进行登录

if __name__ == '__main__':
    url = ''
    headers = {

    }
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    # 获取验证码图片
    code_img_src = tree.xpath('')
    code_img_data = requests.get(url=code_img_src, headers=headers).content
    with open('./code.jpg', 'wb') as fp:
        fp.write(code_img_data)
    # 状态码用于运行是否成功
