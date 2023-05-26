import requests
import json

if __name__ == '__main__':
    url = "https://movie.douban.com/j/chart/top_list"
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action': '',
        'start': '0',  # 从数据库中第start个电影开始取
        'limit': '20',  # 一次取20个
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    response = requests.get(url=url, params=param, headers=headers)
    list_data = response.json()
    fp = open('./douban.json', 'w', encoding='utf-8')
    json.dump(list_data, fp=fp, ensure_ascii=False)
    print("over!!!")
