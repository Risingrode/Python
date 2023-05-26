from tkinter import *
from PIL import Image, ImageTk
from pymediainfo import MediaInfo
import IPython.display as ipd
from pygame import mixer
import threading
import pygame
import time
import requests
import json
import re
import os
# 无效

def music(name):
    url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=62115878671550904&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={name}&g_tk=5381&jsonpCallback=MusicJsonCallback2806001545440244&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    json_list = requests.get(url).text
    res = re.compile(r"MusicJsonCallback.*?{(.*)}", re.S)
    content = re.findall(res, json_list)
    content_1 = '{' + content[0] + '}'
    dict_content = json.loads(content_1)
    keyword = dict_content["data"]["keyword"]
    list_all = dict_content["data"]["song"]["list"]
    mid_list = []
    music_title_list = []
    music_album_name = []
    music_singer_name = []
    for index, for_dict in enumerate(list_all):
        # 专辑名
        album_name = for_dict["album"]["title"]
        music_album_name.append(album_name)
        # new url
        mid_list.append(for_dict["mid"])
        # 歌名
        music_title = for_dict["title"]
        music_title_list.append(music_title)
        # 歌手
        singer_name = for_dict["singer"][0]["title"]
        music_singer_name.append(singer_name)
    return mid_list, music_title_list, music_singer_name, music_album_name


def get_url(data):
    url = 'http://www.douqq.com/qqmusic/qqapi.php'  # 接口网站
    headers = {
        "Content-Type": "application/json",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.douqq.com',
        'Origin': 'http://www.douqq.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }
    from_data = {
        'mid': data
    }
    response = requests.post(url=url, data=from_data, headers=headers)
    str_data = response.content.decode('utf-8')  # 得到字符串数据
    str_data = json.loads(str_data)
    str_data = str_data.replace('\/\/', '//').replace('\/', '/')
    str_data = re.findall('"m4a":"(.*?)",', str_data, re.S)[0]
    return str_data


def save(my_str):
    url = my_str
    response = requests.get(url=url)
    result = response.content
    return result

'''
def select(result):  # 搜索按钮
    a = str(inp1.get())
    s = youdao(a)
    txt.delete(0.0, END)
    txt.insert(END, s)
'''

def show():
    name = str(e1.get())  # get是用来获取e1的内容的
    e2.delete(0.0, END)
    e2.insert(END, '   歌曲\t\t\t  歌手\t\t  专辑\n')
    global my_data
    my_data = music(name=name)
    for i in range(1, 6):
        my_music_list = '%d  ' % i + my_data[1][i] + '\t\t\t ' + my_data[2][i] + '\t\t  ' + my_data[3][i] + '\n'
        e2.insert(END, my_music_list)


def show1():
    name_num = str(e3.get())  # get是用来获取e1的内容的
    e2.delete(0.0, END)
    e2.insert(END, '   歌曲\t\t\t  歌手\t\t  专辑\n')
    my_music_list = '   ' + my_data[1][int(name_num)] + '\t\t\t ' + my_data[2][int(name_num)] + '\t\t  ' + my_data[3][
        int(name_num)] + '\n'
    e2.insert(END, my_music_list)
    data = 'https://y.qq.com/n/yqq/song/' + my_data[0][int(name_num)] + '.html'
    my_str = get_url(data)
    music = save(my_str)

    global my_music_name
    my_music_name = my_data[1][int(name_num)]
    with open('spyider_music\%s.mp3' % my_music_name, 'wb') as f:
        f.write(music)
        f.flush()
    time.sleep(5)
    mixer.init()
    mixer.music.load(r'spyider_music\\' + my_music_name + '.mp3')
    mixer.music.play()
    time.sleep(300)
    mixer.music.stop()
    e2.insert(END, '\n   歌曲缓存中，请等待...\n')
    e2.insert(END, '   缓存完毕！')


if __name__ == "__main__":
    app = Tk()
    app.geometry('540x280')
    app.title('音乐播放器')
    Label(app, text="请输入歌名或者歌手名：").grid(row=1, column=0)
    theButton1 = Button(app, text="搜索", background='#CA0316', foreground='white', activebackground='red',
                        activeforeground='white', width=10, command=show)
    theButton1.grid(row=1, column=4, sticky=W + E, padx=10, pady=5)
    v1 = StringVar()
    e1 = Entry(app, textvariable=v1)
    e2 = Text(app, font=('华文新魏', 11))
    e1.grid(row=1, column=1)
    e2.place(relx=0.03, rely=0.14, relwidth=0.938, relheight=0.5, )
    Label(app, text="   要听第几首歌（根据序号）?").grid(row=6, column=0)
    theButton2 = Button(app, text="播放", background='#CA0316', foreground='white', activebackground='red',
                        activeforeground='white', width=10, command=show1)
    theButton2.grid(row=6, column=4, sticky=W + E, padx=10, pady=145)
    v3 = StringVar()
    e3 = Entry(app, textvariable=v3)
    e3.grid(row=6, column=1)

    mainloop()
