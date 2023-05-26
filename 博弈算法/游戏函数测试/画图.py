import sys, pygame

pygame.init()  # 初始化pygame类
screen = pygame.display.set_mode((600, 300))  # 设置窗口大小
pygame.display.set_caption('动画测试')  # 设置窗口标题
image = pygame.image.load('1.png')  # 加载图片，这里一定要正确填写图片路径，如果和py文件在同目录下则直接写文件名（带上文件类型）
tick = pygame.time.Clock()
frameNumber = 6  # 设置帧数，示例图片有6帧
frameRect = image.get_rect()  # 获取全图的框体数据，以此计算单帧框体
frameRect.width //= frameNumber  # 获取每一帧的边框数据，实例图片之只有一行，所以单帧高度和整体图片高度相等
fps = 10  # 设置刷新率，数字越大刷新率越高，但因为示例图片只有6帧所以建议设低一点 否则闪的太凶。
fcclock = pygame.time.Clock()
n = 0  # 这算是一个magic number吧，是为了计算框体位置所引用的一个计算变量，实在懒得想名字了。

while True:

    for event in pygame.event.get():  # 事件检测，如果点击右上角X，则程序退出，没有这个循环的话，窗口可能会在打开时闪退。
        if event.type == pygame.QUIT:
            sys.exit()
    if n < frameNumber:
        frameRect.x = frameRect.width * n  # 这里通过移动单帧矿体的x轴坐标实现单帧框体位移
        n += 1
    else:
        n = 0

    screen.fill((255, 255, 255))  # 设置背景为白色
    screen.blit(image, (0, 0), frameRect)  # 这里给了3个实参，分别是图像，绘制的位置，绘制的截面框
    fcclock.tick(fps)  # 设置图像刷新率，如果刷新率太高，图像闪的太厉害
    pygame.display.flip()  # 刷新窗口