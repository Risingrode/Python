from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.baidu.com/')

ele = driver.find_element_by_id('kw')
ele.send_keys('易烊千玺')
sleep(1)
ele.send_keys(Keys.BACK_SPACE)
sleep(1)
# 组合键 Ctrl + a 全选 ，注意这里的组合键都是小写
ele.send_keys(Keys.CONTROL, 'a')
sleep(1)
ele.send_keys(Keys.CONTROL, 'x')
sleep(1)
ele.send_keys(Keys.CONTROL, 'v')
sleep(3)

driver.quit()
