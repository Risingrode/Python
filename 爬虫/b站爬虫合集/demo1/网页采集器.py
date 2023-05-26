import requests

# ＵＡ伪装       反趴机制

if __name__ == '__main__':
    url = 'https://www.sogou.com/web'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Mobile Safari/537.36 Edg/104.0.1293.54"
    }
    # 处理url携带的参数：封装到字典中
    kw = input('enter a word:')
    param = {
        'query': kw
    }
    # 发起请求
    # 对指定的url发起的请求是携带参数的，并且请求过程中处理了参数
    response = requests.get(url=url, params=param, headers=headers)
    page_text = response.text
    fileName = kw + '.html'
    with open(f'./{fileName}', 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print(fileName, '保存成功！！！')
