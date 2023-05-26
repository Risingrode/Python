import json

import requests

if __name__ == '__main__':
    # 1
    post_url = 'https://fanyi.baidu.com/sug'
    # 2
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Mobile Safari/537.36 Edg/104.0.1293.54"
    }
    # 3
    word=input("enter a word:")
    data = {
        'kw': word
    }
    # 4
    response = requests.post(url=post_url, data=data, headers=headers)
    # 5获取响应工具
    obj_data = response.json()
    print(obj_data)
    # 持久化存储
    fileName=str(word)+'.json'
    fp = open(fileName, 'w', encoding='utf-8')
    json.dump(obj_data, fp=fp, ensure_ascii=False)
    print('over!')
