import urllib.request
import re

# 定义图片网站URL和要下载图片的网页URL
image_site_url = 'https://pixabay.com/'
image_page_url = 'https://pixabay.com/images/search/nature/'

headers = {
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"
}

# 打开网页并获取网页内容
request = urllib.request.Request(image_page_url, headers=headers)
response = urllib.request.urlopen(request)
html = response.read().decode('utf-8')

# 使用正则表达式匹配图片链接
image_links = re.findall('<img.*?src="(.*?)".*?>', html)

# 遍历图片链接列表，下载图片并保存到本地文件
for link in image_links:
    # 拼接图片链接的完整URL
    if not link.startswith('http'):
        link = image_site_url + link

    # 获取图片文件名并保存到本地文件
    filename = link.split('/')[-1]

    # urllib.request.urlretrieve(link, filename)

    print('下载图片 %s 成功' % filename)
