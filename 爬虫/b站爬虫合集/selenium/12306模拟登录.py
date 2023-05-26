import time
from chaojiying import Chaojiying_Client
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from PIL import Image
from selenium.webdriver import ActionChains

url = 'https://kyfw.12306.cn/otn/resources/login.html'
bro = webdriver.Edge()
bro.get(url)

userName = bro.find_element(By.ID, 'J-userName')
password = bro.find_element(By.ID, 'J-password')

userName.send_keys('18438173708')
password.send_keys('cw123456')

but = bro.find_element(By.ID, 'J-login')
but.click()
# 接下来进行验证码操作
bro.save_screenshot('code.jpg')  # 截屏
# 对图片进行裁剪 需要确定验证码左上角与右下角坐标
code_img_ele = bro.find_element(By.XPATH, '//*[@id="slide"]//img/@src')
location = code_img_ele.location  # 验证码左上角坐标
size = code_img_ele.size  # 验证码的长和宽
# 验证码图片左上角与右下角坐标
rangle = (
int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
print(rangle)
i = Image.open('./code.jpg')
code_img = 'code1.jpg'
frame = i.crop(rangle)
frame.save(code_img)
# 超级鹰进行验证码识别
chaojiying = Chaojiying_Client('rising', 'cw123456', '938145')
im = open('code1.jpg', 'rb').read()
code = chaojiying.PostPic(im, 9101)['pic_str']
# 如果获取的是好几个点坐标，需要分隔开，制成新列表
print(code)

input()
all_list = []
# 对验证码进行点击
for l in all_list:
    x = l[0]
    y = l[1]
    ActionChains(bro).move_to_element_with_offset(code_img_ele, x, y).click().perform()
    time.sleep(0.5)
bro.quit()
