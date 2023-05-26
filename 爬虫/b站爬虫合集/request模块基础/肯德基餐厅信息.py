import requests

if __name__ == '__main__':
    url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword"
    data = {
        'cname': '',
        'pid': '',
        'keyword': '北京',
        'pageIndex': '1',#页码
        'pageSize': '10',#总共几页
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    response = requests.post(url=url, data=data, headers=headers)
    list_data = response.text

    with open('./kfc.json', 'w', encoding='utf-8') as f:
        f.write(list_data)

    print("over!!!")
