from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
bro = webdriver.Edge()
bro.get('https://qzone.qq.com/')
bro.switch_to.frame('login_frame')
div = bro.find_element(By.ID, 'switcher_plogin')
div.click()#只能对获得的标签进行点击

userName=bro.find_element(By.ID,'u')
password=bro.find_element(By.ID,'p')
sleep(1)
userName.send_keys('3377078894')
sleep(1)
password.send_keys('12345678')
sleep(1)
btn=bro.find_element(By.ID,'login_button')
btn.click()
sleep(3)
bro.quit()

