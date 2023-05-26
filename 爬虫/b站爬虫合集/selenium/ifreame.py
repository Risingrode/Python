from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
# ******用于拖放东西
bro = webdriver.Edge()
bro.get('')
# 如果定位的标签是存在于iframe标签中的，则必须进行以下操作在进行标签定位
bro.switch_to.frame('')  # 先切换浏览器标签定位的作用域
div = bro.find_element(By.ID, '')

# 动作链
action = ActionChains(bro)
# 点击长按指定标签
action.click_and_hold(div)
for i in range(5):
    # .perform() 表示立即执行动作链操作
    action.move_by_offset(17, 0).perform()
    sleep(3)
# 释放动作链
action.release()
bro.quit()
