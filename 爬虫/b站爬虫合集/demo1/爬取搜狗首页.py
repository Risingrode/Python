import requests

if __name__=="__main__":
    url="https://www.sogou.com/"
    response=requests.get(url)

    print("响应码是：",response.status_code)
    #text返回的是字符串形式的数据
    page_text=response.text
    with open('sougou.html', 'w', encoding='utf-8')  as f:
        f.write(page_text)
#   ctrl+alt+l  格式化代码
















