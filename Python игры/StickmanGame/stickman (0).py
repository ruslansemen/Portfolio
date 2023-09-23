# здесь только часть кода, необходимо скопировать этот код в общий файл

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates



class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x+width, y+height)

platform1 = PlatformSprite(g, PhotoImage(file='platform1.gif'), 0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file='platform1.gif'), 150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file='platform1.gif'), 300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file='platform1.gif'), 300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file='platform2.gif'), 175, 350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file='platform2.gif'), 50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file='platform2.gif'), 170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file='platform2.gif'), 45, 60, 66, 10)
platform9 = PlatformSprite(g, PhotoImage(file='platform3.gif'), 170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file='platform3.gif'), 230, 160, 100, 10)

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

# глава 17. Создаём человечка 25.05.22

class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [PhotoImage(file='figure-L1.gif'), PhotoImage(file='figure-L2.gif'), PhotoImage(file='figure-L3.gif')]
        self.images_right = [PhotoImage(file='figure-R1.gif'), PhotoImage(file='figure-R2.gif'), PhotoImage(file='figure-R3.gif')]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<spase>', self.jump)

    def turn_left(self, evt):
        if self.y == 0 :
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0 :
            self.x = 2

    def jump(self, evt):
        if self.y == 0 :
            self.y = -4
            self.jump_count = 0

    # глава 18 анимация
    def animate(self):
        if self.x != 0 and self.y == 0 :
            if time.time() - self.last_time > 0.1 :
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2 :
                    self.current_image_add = -1
                if self.current_image <= 0 :
                    self.current_image_add = 1

                    # p. 254 finish
        
        
    
