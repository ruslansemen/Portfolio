# прерванный полёт - 7
# Кроме движушихся астероидов, на экране появляется корабль игрока, 
# корабль может перемещаться в пространстве, стрелять ракетами, 
# взаимодействовать с другими объектами
# добавление в игру эффектных взрывов, 
# исключение повторяющегося (избыточного) кода путём реорганизации - введением новых классов

import random, math
from livewires import games

games.init(screen_width=640, screen_height=480, fps=50)

class Wrapper(games.Sprite):
    """Огибатель. Сппрайт, который, двигаясь, огибает графический экран."""
    def update(self):
        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height
        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        """Разрушает объект."""
        self.destroy()

class Collider(Wrapper):
    """Погибатель. Огибатель, который может сталкиваться с другими объектами и гибнуть."""
    def update(self):
        super(Collider, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()
    
    def die(self):
        """Разрушает объект со взрывом."""
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        self.destroy()


class Ship(Collider):
    """Корабль игрока."""
    ROTATION_STEP = 3
    VELOCITY_STEP = 0.03
    image = games.load_image("ship.bmp")
    sound = games.load_sound("thrust.wav")
    MISSILE_DELAY = 25

    def __init__(self, x, y):
        super(Ship, self).__init__(image = Ship.image, x=x, y=y)
        self.missile_wait = 0

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
        # огибание экрана кораблём, проверка на перекрытие с другими объектами
        super(Ship, self).update()
        # тормоз (доработка)
        if games.keyboard.is_pressed(games.K_DOWN):
            self.dx = 0
            self.dy = 0
        # если запуск следующей ракеты пока ещё не разрешён,
        # вычесть 1 из длины оставшегося интервала ожидания
        if self.missile_wait > 0:
            self.missile_wait -= 1

        # если нажат Пробел и интервал ожидания истёк, выпустить ракету
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY
       

class Missile(Collider):
    """Ракета, которую может выпустить космический корабль игрока."""
    image = games.load_image("missile.bmp")
    sound = games.load_sound("missile.wav")
    BUFFER = 40
    VELOCITY_FACTOR = 7
    LIFETIME = 40

    def __init__(self, ship_x, ship_y, ship_angle):
        """Инициализирует спрайт с изображением ракеты."""
        Missile.sound.play()
        # преобразование в радианы
        angle = ship_angle*math.pi/180
        # вычисление начальной позиции ракеты
        buffer_x = Missile.BUFFER*math.sin(angle)
        buffer_y = -Missile.BUFFER*math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y
        # вычисление горизонтальной и вертикальной скорости ракеты
        dx = Missile.VELOCITY_FACTOR*math.sin(angle)
        dy = -Missile.VELOCITY_FACTOR*math.cos(angle)
        # создание ракеты
        super(Missile, self).__init__(image=Missile.image, x=x, y=y, dx=dx, dy=dy)
        self.lifetime = Missile.LIFETIME

    def update(self):
        """Перемещает ракету"""
        # ограничение времени жизни ракеты
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
        
        # огибание экрана проверка на перекрытие с другими объектами
        super(Missile, self).update()
       
         
class Asteroid(Wrapper):
    """Астероид, прямолинейно движущийся по экрану."""
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL : games.load_image("asteroid_small.bmp"),
            MEDIUM : games.load_image("asteroid_med.bmp"),
            LARGE : games.load_image("asteroid_big.bmp")}
    SPEED = 2
    SPAWN = 2

    def __init__(self, x, y, size):
        super(Asteroid, self).__init__(image=Asteroid.images[size], x=x, y=y, \
            dx=random.choice([1, -1])*Asteroid.SPEED*random.random()/size, \
            dy=random.choice([1, -1])*Asteroid.SPEED*random.random()/size)
        self.size = size

    
    def die(self):
        """Разрушает астероид."""
        # если размеры астероида крупные или средние, заменить его двумя более мелкими астероидами 
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x=self.x, y=self.y, size=self.size-1)
                games.screen.add(new_asteroid)
        super(Asteroid, self).die()


class Explosion(games.Animation):
    """Анимация взрывов."""
    sound = games.load_sound("explosion.wav")
    images = ["explosion1.bmp", 
              "explosion2.bmp", 
              "explosion3.bmp", 
              "explosion4.bmp", 
              "explosion5.bmp", 
              "explosion6.bmp", 
              "explosion7.bmp", 
              "explosion8.bmp", 
              "explosion9.bmp"]
    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images, x=x, y=y, repeat_interval=4, n_repeats=1, is_collideable=False)
        Explosion.sound.play()




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
    the_ship = Ship(x=games.screen.width/2, y=games.screen.height/2)
    games.screen.add(the_ship)
    games.screen.mainloop()

# поехали!
main()