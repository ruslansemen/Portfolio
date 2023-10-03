# прерванный полёт - 3
# Кроме движушихся астероидов, на экране появляется корабль игрока, корабль может перемещаться в пространстве


import random, math
from livewires import games

games.init(screen_width=640, screen_height=480, fps=50)

class Ship(games.Sprite):
    """Корабль игрока."""
    ROTATION_STEP = 3
    VELOCITY_STEP = 0.03
    image = games.load_image("ship.bmp")
    sound = games.load_sound("thrust.wav")

    def update(self):
        """Вращает, ускоряет корабль при нажатии клавиш со стрелками"""
        # вращение корабля
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP
        # ускорение корабля
        if games.keyboard.is_pressed(games.K_UP):
            Ship.sound.play()
            # преобразование меры угла из градусов в радианы
            angle = self.angle*math.pi/180
            self.dx += Ship.VELOCITY_STEP*math.sin(angle)
            self.dy += -Ship.VELOCITY_STEP*math.cos(angle)
        # огибание экрана кораблём
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width
        # тормоз (доработка)
        if games.keyboard.is_pressed(games.K_DOWN):
            self.dx = 0
            self.dy = 0


class Asteroid(games.Sprite):
    """Астероид, прямолинейно движущийся по экрану."""
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL : games.load_image("asteroid_small.bmp"),
            MEDIUM : games.load_image("asteroid_med.bmp"),
            LARGE : games.load_image("asteroid_big.bmp")}
    SPEED = 2

    def __init__(self, x, y, size):
        super(Asteroid, self).__init__(image=Asteroid.images[size], x=x, y=y, \
            dx=random.choice([1, -1])*Asteroid.SPEED*random.random()/size, \
            dy=random.choice([1, -1])*Asteroid.SPEED*random.random()/size)
        self.size = size

    def update(self):
        """Заставляет астероид обогнуть экран."""
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width

def main():
    # назначаем фоновую картинку
    nebula_image = games.load_image("nebula.jpg")
    games.screen.background = nebula_image
    # создаём 8 астероидов
    for i in range(8):
        x = random.randrange(0, games.screen.width)
        y = random.randrange(0, games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x=x, y=y, size=size)
        games.screen.add(new_asteroid)
    the_ship = Ship(image=Ship.image, x=games.screen.width/2, y=games.screen.height/2)
    games.screen.add(the_ship)
    games.screen.mainloop()

# поехали!
main()