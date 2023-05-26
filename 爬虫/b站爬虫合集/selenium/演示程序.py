from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By

bro = webdriver.Edge()
bro.get('https://www.taobao.com/')

# 标签定位
search_input = bro.find_element(By.ID, 'q')
# 标签交互
search_input.send_keys('iphone')

#执行一组js程序
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(2)
# 点击搜索按钮
btn = bro.find_element(By.CLASS_NAME, 'btn-search')
btn.click()

bro.get('https://baidu.com')
sleep(2)
#回退
bro.back()
#前进
bro.forward()

sleep(5)
#关闭当前网页
bro.quit()
