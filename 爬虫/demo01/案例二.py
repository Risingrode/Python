import re,time
import requests

count = 0
while count < 10:
    url = "https://pic.netbian.com/4kmeinv/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Mobile Safari/537.36 Edg/104.0.1293.54"
    }
    response = requests.get(url, headers=headers)
    html = response.text
    urls = re.findall('<img src = "(.*?).jpg" alt =".*?" /><b>', html)
    for url1 in urls:
        with open("D:\\Python\\爬虫\\demo01\\pictures" + str(count) + ".jpg", "wb") as f:
            res = requests.get(url1, headers=headers)
            f.write(res.content)
            print(f"正在下载第{count + 1}张图片")
            count += 1
        time.sleep(0.5)


