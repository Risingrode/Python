# 导入
import os
import time
import tkinter
import tkinter.filedialog
import threading
import pygame  # pip

folder = ''
res = []
num = 0
now_music = ''


def Start():
    file = r'D://音乐/不堪.mp3'
    pygame.mixer.init()
    print('正在播放', file)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    time.sleep(130)
    pygame.mixer.music.stop()


def buttonChooseClick():
    """
    添加文件夹
    :return:
    """
    global folder
    global res
    if not folder:
        folder = tkinter.filedialog.askdirectory()
        musics = [folder + '\\' + music
                  for music in os.listdir(folder) \
 \
                  if music.endswith(('.mp3', '.wav', '.ogg'))]
        ret = []
        for i in musics:
            ret.append(i.split('\\')[1:])
            res.append(i.replace('\\', '/'))

        var2 = tkinter.StringVar()
        var2.set(ret)
        lb = tkinter.Listbox(root, listvariable=var2, selectmode=tkinter.SINGLE)
        lb.place(x=50, y=100, width=300, height=400)
        # print(lb.curselection())

    if not folder:
        return

    global playing
    playing = True
    # 根据情况禁用和启用相应的按钮
    buttonPlay['state'] = 'normal'
    buttonStop['state'] = 'normal'
    # buttonPause['state'] = 'normal'
    pause_resume.set('播放')


def play():
    """
    播放音乐
    :return:
    """
    if len(res):
        pygame.mixer.init()
        global num
        while playing:
            if not pygame.mixer.music.get_busy():
                netxMusic = res[num]
                print(netxMusic)
                print(num)
                pygame.mixer.music.load(netxMusic.encode())
                # 播放
                pygame.mixer.music.play(1)
                if len(res) - 1 == num:
                    num = 0
                else:
                    num = num + 1
                netxMusic = netxMusic.split('\\')[1:]
                musicName.set('正在播放' + ''.join(netxMusic))
            else:
                time.sleep(0.1)


def buttonPlayClick():
    """
    点击播放
    :return:
    """
    buttonNext['state'] = 'normal'

    buttonPrev['state'] = 'normal'
    # 选择要播放的音乐文件夹
    if pause_resume.get() == '播放':
        pause_resume.set('暂停')
        global folder

        if not folder:
            folder = tkinter.filedialog.askdirectory()

        if not folder:
            return

        global playing

        playing = True

        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        t = threading.Thread(target=play)
        t.start()

    elif pause_resume.get() == '暂停':
        # pygame.mixer.init()
        pygame.mixer.music.pause()
        pause_resume.set('继续')

    elif pause_resume.get() == '继续':
        # pygame.mixer.init()
        pygame.mixer.music.unpause()

        pause_resume.set('暂停')


def buttonStopClick():
    """
    停止播放
    :return:
    """
    global playing
    playing = False
    pygame.mixer.music.stop()


def buttonNextClick():
    """
    下一首
    :return:
    """
    global playing
    playing = False
    pygame.mixer.music.stop()
    global num
    if len(res) == num:
        num = 0

    playing = True
    # 创建线程播放音乐,主线程用来接收用户操作
    t = threading.Thread(target=play)
    t.start()


def closeWindow():
    """
    关闭窗口
    :return:
    """
    # 修改变量，结束线程中的循环

    global playing
    playing = False
    time.sleep(0.3)
    try:
        # 停止播放，如果已停止，
        # 再次停止时会抛出异常，所以放在异常处理结构中
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass

    root.destroy()


def control_voice(value=0.5):
    """
    声音控制
    :param value: 0.0-1.0
    :return:
    """
    pygame.mixer.music.set_volume(float(value))


def buttonPrevClick():
    """
    上一首
    :return:
    """
    global playing

    playing = False

    pygame.mixer.music.stop()
    #
    # pygame.mixer.quit()
    global num
    # num += 1
    # num -= 1
    if num == 0:
        num = len(res) - 2
        # num -= 1
    elif num == len(res) - 1:
        num -= 2
    else:
        num -= 2
        # num -= 1
    print(num)

    playing = True

    # 创建一个线程来播放音乐，当前主线程用来接收用户操作

    t = threading.Thread(target=play)

    t.start()


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('迷你音乐播放器')
    root.geometry('460x600+500+100')
    root.resizable(False, False)  # 不能拉伸
    # 窗口关闭
    root.protocol('WM_DELETE_WINDOW', closeWindow)

    # 添加按钮
    buttonChoose = tkinter.Button(root, text='添加', command=buttonChooseClick)
    # 布局
    buttonChoose.place(x=50, y=10, width=50, height=20)

    # 播放按钮
    pause_resume = tkinter.StringVar(root, value='播放')
    buttonPlay = tkinter.Button(root, textvariable=pause_resume, command=buttonPlayClick)
    buttonPlay.place(x=190, y=10, width=50, height=20)
    buttonPlay['state'] = 'disabled'

    # 停止按钮
    buttonStop = tkinter.Button(root, text='停止', command=buttonStopClick)
    buttonStop.place(x=120, y=10, width=50, height=20)
    buttonStop['state'] = 'disabled'

    # 下一首
    buttonNext = tkinter.Button(root, text='下一首', command=buttonNextClick)
    buttonNext.place(x=260, y=10, width=50, height=20)
    buttonNext['state'] = 'disabled'
    # 上一首
    buttonPrev = tkinter.Button(root, text='上一首', command=buttonPrevClick)
    buttonPrev.place(x=330, y=10, width=50, height=20)
    buttonPrev['state'] = 'disabled'

    # 标签
    musicName = tkinter.StringVar(root, value='暂时没有播放音乐...')
    labelName = tkinter.Label(root, textvariable=musicName)
    labelName.place(x=10, y=30, width=260, height=20)

    # 音量控制
    # HORIZONTAL表示为水平放置，默认为竖直,竖直为vertical
    s = tkinter.Scale(root, label='音量', from_=0, to=1, orient=tkinter.HORIZONTAL,
                      length=240, showvalue=0, tickinterval=2, resolution=0.1, command=control_voice)
    s.place(x=50, y=50, width=200)
    # 显示
    root.mainloop()
