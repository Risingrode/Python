from tkinter import *
from gomoku import Gomoku
from keras.models import load_model
import numpy as np


model = load_model('./best_model.h5')
gsize = 15
line = 5
game = Gomoku(gsize, line)


grid_width = 40
r = 10
piece_color = ['black', 'white']
person_flag = 0
gamedone = False
PVP = False

window = Tk()
window.title("Gomoku")
canvas = Canvas(window, bg="SandyBrown", width=grid_width * (gsize + 1), height=grid_width * (gsize + 1))
canvas.grid(row=0, column=0, rowspan=10)
var = StringVar()
for i in range(gsize):
    canvas.create_line(grid_width, (grid_width * i + grid_width), grid_width * gsize, (grid_width * i + grid_width))
    canvas.create_line((grid_width * i + grid_width), grid_width, (grid_width * i + grid_width), grid_width * gsize)


def mouseBack(event):
    global person_flag, piece_color, gamedone, var, PVP
    if gamedone:
        return
    i = round(event.x / grid_width)
    j = round(event.y / grid_width)
    if not game.act_legal([i - 1, j - 1]):
        return
    state, _, done = game.step((i - 1) * gsize + j - 1)
    canvas.create_oval(i * grid_width - r, j * grid_width - r,
                       i * grid_width + r, j * grid_width + r,
                       fill=piece_color[person_flag], tags=("piece"))
    canvas.update()
    person_flag = 1 - person_flag
    if done:
        gamedone = True
        var.set('Win!')
        return

    if not PVP:
        arr = np.zeros((gsize, gsize))
        arr[game.grid[person_flag] == 1] = 1
        arr[game.grid[1 - person_flag] == 1] = -1
        arr = np.expand_dims(arr, axis=(0, -1)).astype(np.float32)
        output = model.predict(arr).squeeze()
        output = output.reshape((gsize, gsize))
        output_x, output_y = np.unravel_index(np.argmax(output), output.shape)
        action = output_x * gsize + output_y
        state, _, done = game.step(action)
        i, j = action // gsize + 1, action % gsize + 1
        canvas.create_oval(i * grid_width - r, j * grid_width - r,
                           i * grid_width + r, j * grid_width + r,
                           fill=piece_color[person_flag], tags=("piece"))
        # print('AI place on [{},{}]'.format(i - 1, j - 1))
        person_flag = 1 - person_flag
        if done:
            var.set('Lose!')
            # print(game.grid[1] - game.grid[0])
            gamedone = True
    else:
        piece_canvas = Canvas(window, width=200, height=200)
        piece_canvas.grid(row=0, column=1)
        piece_canvas.create_oval(100 - r, 100 - r, 100 + r, 100 + r, fill=piece_color[person_flag])


canvas.bind("<Button-1>", mouseBack)


def click_resetPVP():
    global person_flag, gamedone, var, PVP
    PVP = True
    gamedone = False
    person_flag = 0
    canvas.delete("piece")
    game.reset()
    var.set("Playing")
    piece_canvas = Canvas(window, width=200, height=200)
    piece_canvas.grid(row=0, column=1)
    piece_canvas.create_oval(100 - r, 100 - r, 100 + r, 100 + r, fill='black')


def click_resetB():
    global person_flag, gamedone, var, PVP
    PVP = False
    gamedone = False
    person_flag = 0
    canvas.delete("piece")
    game.reset()
    var.set("Playing")
    piece_canvas = Canvas(window, width=200, height=200)
    piece_canvas.grid(row=0, column=1)
    piece_canvas.create_oval(100 - r, 100 - r, 100 + r, 100 + r, fill='black')


def click_resetW():
    global person_flag, gamedone, var, PVP
    PVP = False
    gamedone = False
    canvas.delete("piece")
    game.reset()
    arr = np.zeros((gsize, gsize))
    arr = np.expand_dims(arr, axis=(0, -1)).astype(np.float32)
    output = model.predict(arr).squeeze()
    output = output.reshape((gsize, gsize))
    output_x, output_y = np.unravel_index(np.argmax(output), output.shape)
    action = output_x * gsize + output_y
    game.step(action)
    i, j = action // gsize + 1, action % gsize + 1
    canvas.create_oval(i * grid_width - r, j * grid_width - r,
                       i * grid_width + r, j * grid_width + r,
                       fill='black', tags=("piece"))
    person_flag = 1
    var.set("Playing")
    piece_canvas = Canvas(window, width=200, height=200)
    piece_canvas.grid(row=0, column=1)
    piece_canvas.create_oval(100 - r, 100 - r, 100 + r, 100 + r, fill='white')


button1 = Button(window, text="先手", font=('黑体', 10), fg='blue', width=10, height=2, command=click_resetB)
button1.grid(row=4, column=1)
button3 = Button(window, text="后手", font=('黑体', 10), fg='blue', width=10, height=2, command=click_resetW)
button3.grid(row=5, column=1)
button2 = Button(window, text="双人对战", font=('黑体', 10), fg='blue', width=10, height=2, command=click_resetPVP)
button2.grid(row=6, column=1)

piece_canvas = Canvas(window, width=200, height=200)
piece_canvas.grid(row=0, column=1)
piece_canvas.create_oval(100 - r, 100 - r, 100 + r, 100 + r, fill='black')

var.set("Playing")
label = Label(window, textvariable=var, font=("宋体", 16))
label.grid(row=1, column=1)
window.mainloop()
