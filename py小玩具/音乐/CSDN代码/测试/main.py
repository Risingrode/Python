from UI import ui

from requests_html import HTMLSession
import time, random, os, threading, json, hashlib, pygame
import tkinter.messagebox as msgbox
import tkinter.filedialog

USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.7 Firefox/68.0 PaleMoon/28.16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
]


def user_input_data(self):
    '''
        2、获取用户输入
    '''
    keyword = self.user_input.get()
    if keyword == '':
        self.text_box.insert("insert", '--------------------请正确输入歌手关键字-------------------' + '\n')
    else:
        self.keyword = keyword
        self.Reverse_JS()


def Reverse_JS(self):
    '''
            3、JS逆向部分, 获取signature
        '''
    # 1、获取时间戳
    timestamps = int(time.time() * 1000)
    # 2、获取加密列表
    sign_list = ['NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt', 'bitrate=0', 'callback=callback123',
                 f'clienttime={timestamps}', 'clientver=2000', 'dfid=-', 'inputtype=0', 'iscorrection=1',
                 'isfuzzy=0', f'keyword={self.keyword}', f'mid={timestamps}', 'page=1', 'pagesize=30',
                 'platform=WebFilter', 'privilege_filter=0', 'srcappid=2919', 'tag=em', 'userid=0',
                 f'uuid={timestamps}', 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt']
    # 3、MD5加密
    signature = hashlib.md5("".join(sign_list).encode()).hexdigest()  # #拿到加密字符串

    signature = signature.upper()
    self.confrim_params_index(timestamps, signature)


def confrim_params_index(self, timestamps, signature):
    '''
            4、确认歌曲列表页请求参数
        '''
    params = {
        "callback": "callback123",
        "keyword": "{}".format(self.keyword),
        "page": "1",
        "pagesize": "30",
        "bitrate": "0",
        "isfuzzy": "0",
        "tag": "em",
        "inputtype": "0",
        "platform": "WebFilter",
        "userid": "0",
        "clientver": "2000",
        "iscorrection": "1",
        "privilege_filter": "0",
        "srcappid": "2919",
        "clienttime": "{}".format(timestamps),
        "mid": "{}".format(timestamps),
        "uuid": "{}".format(timestamps),
        "dfid": "-",
        "signature": "{}".format(signature),
    }

    self.requests_start_url(params)


def requests_start_url(self, params):
    '''
            5、发送请求，获取响应数据
        '''
    headers = {'user-agent': random.choice(USER_AGENT_LIST)}
    response_first = self.session.get(self.start_url, headers=headers, params=params).content.decode()  # 解码

    # FIXME：TODO：response_first[12:-2]
    response_first = json.loads(response_first[12:-2])  # 将str类型的数据转换为dict(字典)类型

    self.parse_response_first(response_first)


def parse_response_first(self, response_first):
    '''
            6、解析获取歌曲ID，
        '''
    song_infos = response_first['data']['lists']

    for song_info in song_infos:
        song_id = song_info['AlbumID']
        song_hash = song_info['FileHash']
        self.confrim_params_info(song_id, song_hash)
    self.showMusic()


def confrim_params_info(self, song_id, song_hash):
    '''
            7、确认歌曲详情页请求参数
        '''
    params = {
        "r": "play/getdata",
        # "callback": "jQuery191045156410697659455_1633537283159",
        "hash": "{}".format(song_hash),
        "dfid": "{}".format(self.cookies_dfid),  # 初始化时自己定义的
        "mid": "{}".format(self.cookies_mid),
        "appid": "1014",
        "platid": "4",
        "album_id": "{}".format(song_id),
        "_": "{}".format(int(time.time() * 1000)),
    }
    self.requests_song_info_url(params)


def requests_song_info_url(self, params):
    '''
            8、获取歌曲详情页数据
        '''
    headers = {'user-agent': random.choice(USER_AGENT_LIST)}
    try:
        response_second = self.session.get(self.song_info_url, headers=headers, params=params).json()
        self.parse_response_second(response_second)
    except Exception as e:
        pass


def parse_response_second(self, response_second):
    """
            9、解析获取歌曲名字， 歌曲地址
        """
    song_name = response_second['data']['song_name']
    song_url = response_second['data']['play_url']
    # print(song_name, song_url, sep=' | ')
    self.List_name.append(song_name)
    self.List_url.append(song_url)
    # self.requests_song_url(song_name, song_url)


# 音乐播放
def PlayMusic(self):
    # playUrl = str(self.List_url[int(self.input_num.get()) - 1])
    self.path = tkinter.filedialog.askdirectory()
    self.music_path = [self.path + '/' + x for x in os.listdir(self.path) if x.endswith(".mp3")]
    # self.clear()
    self.showMusicList()


def showMusic(self):
    a = len(self.List_name)
    self.text_box.insert("insert", '共有{}首音乐'.format(a) + "\n")
    for i in range(a):
        self.text_box.insert("insert", '{}的第{}首音乐是：{}'.format(self.keyword, i + 1, self.List_name[i]) + "\n")


def Download(self):
    num = int(self.input_num.get())
    List_num = len(self.List_name)
    if num > List_num:
        self.PopWin('超出范围，输入错误！')
    else:
        self.requests_song_url(self.List_name[num - 1], self.List_url[num - 1])


def DownloadAll(self):
    for i in len(self.List_name):
        self.requests_song_url(self.List_name[i - 1], self.List_url[i - 1])
    self.PopWin('一键下载成功！')


# 弹窗
def PopWin(self, target):
    answer = msgbox.askokcancel('提示', target)
    '''if answer:
            self.lb.config(text='已确认')
        else:
            self.lb.config(text='已取消')
        '''


# 一键下载路径选择
def DownloadPath(self):
    self.DownPath = tkinter.filedialog.askopenfilename()

    '''
        self.music_path = tkinter.filedialog.askopenfilename()# 获取文件名
        print(self.music_path)    
        self.music_path = tkinter.filedialog.askdirectory()# 获取文件夹
        print(self.music_path)
        '''


def showMusicList(self):
    i = 0
    for x in os.listdir(self.path):
        i += 1
        self.text_box.insert("insert", '序号是:{}:音乐是：{}'.format(i, x + "\n"))
    self.choice()


# 音乐播放  TODO：未测试
def choice(self):
    num = int(self.input_num.get())
    pygame.mixer.init()
    pygame.mixer.music.load(str(self.music_path[num - 1]))
    for i in range(num + 2, len(self.music_path) + 1):  # 左闭右开
        pygame.mixer.music.queue(str(self.music_path[i - 1]))
        pygame.mixer.music.play()  # 0表示不循环，-1表示无限循环，设置1表示循环一次，即一共播放两次
        while pygame.mixer.music.get_busy():  # 在音频播放为完成之前不退出程序
            pass

    # playsound(str(self.music_path[num - 1])) # 这个不会用
    '''
        pygame.mixer.music.load() 加载音乐。参数为filename，以字符串传入音频文件地址；
        pygame.mixer.music.unload() 卸载已经加载的音乐。无参数；
        pygame.mixer.music.play() 播放加载的音乐。三个可选参数，loops循环次数（int）；start开始播放时间（float）有的文件类型可能不支持（我试验过的Ubuntu环境下wav文件不支持设置）mp3文件的时间定位可能不准确；fade_ms音量渐变的时间间隔（int）我没有听出啥区别。。。；这三个参数默认为0
        pygame.mixer.music.rewind() 重新开始音乐。
        pygame.mixer.music.stop() 停止音乐播放。
        pygame.mixer.music.pause() 暂停音乐播放。
        pygame.mixer.music.unpause() 恢复暂停的音乐。
        pygame.mixer.music.fadeout() 淡出后停止音乐播放。
        pygame.mixer.music.set_volume() 设置音量。参数0~1之间的浮点数；
        pygame.mixer.music.get_volume() 获得音量。返回一个浮点数（0~1之间）；
        pygame.mixer.music.get_busy() 音乐是否播放。返回一个bool类型的值（文档的说明）我实际测试返回的是0和1不过无所谓当需要传bool值是python会将1看成True0，看成False的（Ubuntu环境）。我的测试程序及结果如下：
        pygame.mixer.music.set_pos() 设定位置（开始播放的位置）。参数pos（float），有的文件类型可能不支持详细见文档。
        pygame.mixer.music.get_pos() 获取音乐播放时间(注意这是已经播放的时间不是音乐时间长度)。返回播放的毫秒数；
        pygame.mixer.music.queue() 将声音文件排队以跟随当前文件（意思是在当前播放的声音后面再加上声音一次只能加一个，如果当前的声音未播放完就停止则后面加的声音也将丢失）。参数filename，以字符串传入音频文件地址；
        pygame.mixer.music.set_endevent() 播放停止时让音乐发送事件
        pygame.mixer.music.get_endevent() 获取播放停止时频道发送的事件
        '''


def requests_song_url(self, song_name, song_url):
    '''
            10、请求获取歌曲二进制数据
        '''
    try:
        headers = {'user-agent': random.choice(USER_AGENT_LIST)}
        song_content = self.session.get(song_url, headers=headers).content
        self.create_dir(song_name, song_content)
    except Exception as e:
        pass


def create_dir(self, song_name, song_content):
    '''
            11、创建文件夹
        '''
    if not os.path.exists(r'./{}'.format(self.keyword)):
        os.mkdir(r'./{}'.format(self.keyword))
    self.save_data(song_name, song_content)


def save_data(self, song_name, song_content):
    '''
            12、保存数据
        '''
    try:
        if (self.DownPath):
            with open(self.path + '/{}.mp3'.format(song_name), 'wb') as f:
                f.write(song_content)
            self.text_box.insert("insert", '歌曲下载成功: {} - {}.mp3'.format(self.keyword, song_name) + "\n")
        else:
            with open(r'./{}/{}.mp3'.format(self.keyword, song_name), 'wb') as f:
                f.write(song_content)
            self.text_box.insert("insert", '歌曲下载成功: {} - {}.mp3'.format(self.keyword, song_name) + "\n")
    except Exception as e:
        self.text_box.insert("insert", '歌曲下载失败: {} - {}.mp3'.format(self.keyword, song_name) + "\n")


def clear(self):
    '''
            13、清除富文本框数据
        '''
    self.text_box.delete("1.0", "end")


def quit(self):
    '''
            14、退出程序
        '''
    self.window.quit()


def main(self):
    '''
            逻辑控制部分, 添加守护线程，防止线程停止时卡顿
        '''
    Running = threading.Thread(target=self.user_input_data)
    Running.daemon = True
    Running.start()


if __name__ == '__main__':
    kgyy = ui.MainUi()
    kgyy.window.mainloop()
