import json
import requests

if __name__ == '__main__':
    # 批量获取id值
    url='http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?hKHnQfLv=5zQGaki_HH0kdiM2oElr03uIcIM_04EryxwKoKjCGmxPc_Y44tAtOzndrL8n8uYezTKTUnX1UtfX3lQDIdIlhQ1BVdNmeIv9ALnYllxpATOlFQ5HNcBP16uIw1IIqPOMBsO1vrd3AxQPbAIXPnrTNQvLC8yjAsKMC8irmx.kXQVxVIIz2wDgoU7XbSjwTTP5f0TgBMNgH9fsB07DV2ygie58_0EUK69xYzXwgz988Ef5RDeJ7BeLwfvovH2KswygwPSPzR9SOUEa1svXGGUHVvWZf3veBSpQ7vMYPSvSx30A&8X7Yi61c=41YwsrOpkTjNbuAE6MgmZ8UK._Dm3A2TpyxjmfN7xJcoCEJPDs3IlJiPt2Xlu9ZLjpJYMVyrXaOc8GjcR6sOXmVla8TgO8tkoXqWHYreDRc16PU1lMMoYrJn96TkyxtDZ'
    #分页操作
    count=0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    id_list = []
    while count<6:#计算前六页
        data = {
            'on': 'true',
            'page': str(count),
            'pageSize': '15',
            'productName': '',
            'conditionType': '1',
            'applyname': '',
            'applysn': '',
        }
        response = requests.post(url=url, data=data, headers=headers)
        page_text = response.text
        print(page_text)
        count+=1
        '''
        for id in page_text['list']:
            id_list.append(id['ID'])

    # 获取企业详情
    all_list_detail = []
    post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portal/dzpz.jsp'
    for id in id_list:
        data = {
            'id': id
        }
        detail = requests.post(url=post_url, headers=headers, data=data).json()
        print(detail, end='-----------------------------')
        all_list_detail.append(detail)

    fp = open('allDetail.json', 'w', encoding='utf-8')
    json.dump(all_list_detail, fp=fp, ensure_ascii=False)
    print('存储成功!!!')

'''






















