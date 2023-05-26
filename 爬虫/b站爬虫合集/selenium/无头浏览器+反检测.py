from selenium import webdriver
from time import sleep
# 实现无可视化界面操作
from selenium.webdriver.edge.options import Options
edge_options = Options()
edge_options.add_argument('--headless')
edge_options.add_argument('--disable-gpu')

# 用来实现规避检测的
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
bro = webdriver.Edge(options=edge_options)
# 无可视化界面（无头浏览器）
bro.get('https://www.baidu.com')
print(bro.page_source)
sleep(2)
bro.quit()
