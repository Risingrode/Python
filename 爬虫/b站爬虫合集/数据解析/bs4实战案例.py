# 需求：爬取三国演义小说的章节，标题，内容
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63'
    }
    page_text = requests.get(url=url, headers=headers).content
    # 实例化
    soup = BeautifulSoup(page_text, 'lxml')

    list_tit = soup.select('.book-mulu > ul > li >a')

    fp = open('./三国演义.txt', 'w', encoding='utf-8')
    for x in list_tit:
        title = x.string    #直系
        detail = 'https://www.shicimingju.com' + x['href']
        # 对详情页发起请求
        detail_text = requests.get(url=detail, headers=headers).content
        soup1 = BeautifulSoup(detail_text, 'lxml')
        main_text = soup1.find('div', class_='chapter_content')
        div_text = main_text.text

        fp.write(title + ':' + div_text + '\n')
        print(title, '爬取成功！')
