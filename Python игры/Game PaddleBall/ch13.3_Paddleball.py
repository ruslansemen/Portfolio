from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle, textend, color):  # 2 добавим новую переменную textend
        self.canvas = canvas
        self.paddle = paddle
        self.textend = textend  # 2
        self.textend.hidden()  # 2
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = True            # 1
        self.canvas.bind_all('<Button-1>', self.start)  # 1

    def start(self, evt):
        self.hit_bottom = False           # 1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            # self.y = -3
            self.hit_bottom = True
            time.sleep(1.2)                 # 2
            self.textend.normal()           # 2
        if self.hit_paddle(pos) == True:    # проверка на столкновение с ракеткой
            self.y = -3
            if paddle.x > 0 and self.x > 0:                           # 3
                self.x = self.x + 2                                   # 3
            elif paddle.x < 0 and self.x < 0:                         # 3
                self.x = self.x - 2                                   # 3
            elif paddle.x < 0 and self.x > 0:                         # 3
                self.x = self.x - 2                                   # 3
            elif paddle.x > 0 and self.x < 0:                         # 3
                self.x = self.x + 2                                   # 3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.speed = 4

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed


# 2             Создаём новый класс для отображения текста "Конец игры"
class Game_end:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_text(
            250, 150, text='Конец игры', font=('Helvetica', 20))

    def hidden(self):
        self.canvas.itemconfig(self.id, state='hidden')

    def normal(self):
        self.canvas.itemconfig(self.id, state='normal')


tk = Tk()
tk.title("Игра")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, heigh=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

textend = Game_end(canvas)                      # 2
paddle = Paddle(canvas, 'blue')
# 2 добавим новую переменную textend
ball = Ball(canvas, paddle, textend, 'red')


while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
