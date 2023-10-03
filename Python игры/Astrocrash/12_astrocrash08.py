# прерванный полёт - 8
# Кроме движушихся астероидов, на экране появляется корабль игрока, 
# корабль может перемещаться в пространстве, стрелять ракетами, 
# взаимодействовать с другими объектами
# добавление в игру эффектных взрывов, 
# исключение повторяющегося (избыточного) кода путём реорганизации - введением новых классов
# Добавление объекта игры. Ведётся счёт, вводятся уровни сложности, сообщения. 

import random, math
from livewires import games, color

games.init(screen_width=640, screen_height=480, fps=50)

class Game(object):
    """Собственно игра."""
    def __init__(self):
        """Инициализирует объекты Game."""
        # выбор начального игрового уровня
        self.level = 0
        # загрузка звука, сопровождающего переход на следующий уровень
        self.sound = games.load_sound("level.wav")
        # создание объекта, в котором будет храниться текущий счёт
        self.score = games.Text(value=0, size=30,\
             color=color.white, top=5,\
             right=games.screen.width-10, is_collideable=False)
        games.screen.add(self.score)
        # создание корабля
        self.ship = Ship(game=self, x=games.screen.width/2, y=games.screen.height/2)
        games.screen.add(self.ship)

    def play(self):
        """Начинает игру."""
        # запуск музыкальной темы
        games.music.load("theme.mid")
        games.music.play(-1)
        # загрузка и назначение фоновой картинки
        nebula_image = games.load_image("nebula.jpg")
        games.screen.background = nebula_image
        # переход к уровню 1
        self.advance()
        # начало игры
        games.screen.mainloop()

    def advance(self):
        """Переводит игру на очередной уровень."""
        self.level += 1
        # зарезервированное пространство вокруг корабля
        BUFFER = 150
        # создание новых астероидов
        for i in range(self.level):
            # вычислим x и y, чтобы от корабля они отстояли минимум на BUFFER пикселов
            # сначала выберем минимальные отступы по горизонтали и вертикали
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min
            # исходя из этих минимумов, сгенерируем расстояния от корабля
            # по горизонтали и вертикали
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)
            # исходя из этих значений, вычислим экранные координаты
            x = self.ship.x + x_distance
            y = self.ship.y + y_distance
            x %= games.screen.width
            y %= games.screen.height
            # создаём астероид
            new_asteroid = Asteroid(game=self, x=x, y=y, size=Asteroid.LARGE)
            games.screen.add(new_asteroid)
            # отображение номера уровня
            level_message = games.Message(value="Уровень " + str(self.level), size=40, color=color.yellow, x=games.screen.width/2 , y=games.screen.height/10, lifetime=3*games.screen.fps, is_collideable=False)
            games.screen.add(level_message)
            # звуковой эффект перехода (кроме 1-го уровня)
            if self.level > 1:
                self.sound.play()

    def end(self):
        """Завершает игру."""
        # 5-секундное отображение 'Game Over'
        end_message = games.Message(value="Game Over", size=90, color=color.red, x=games.screen.width/2, y=games.screen.height/2, lifetime=5*games.screen.fps, after_death=games.screen.quit, is_collideable=False)
        games.screen.add(end_message)



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
    VELOCITY_MAX = 3
    image = games.load_image("ship.bmp")
    sound = games.load_sound("thrust.wav")
    MISSILE_DELAY = 25

    def __init__(self, game, x, y):
        super(Ship, self).__init__(image = Ship.image, x=x, y=y)
        self.missile_wait = 0
        self.game = game

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
            # ограничение горизонтальной и вертикальной скоростей
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
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

    def die(self):
        """Разрушает корабль и завершает игру."""
        # попробовать поменять местами нижние строки, будет ли в этом случае завершаться игра?
        self.game.end()
        super(Ship, self).die()

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
    SPEED = 2
    SPAWN = 2
    POINTS = 30
    images = {SMALL : games.load_image("asteroid_small.bmp"),
            MEDIUM : games.load_image("asteroid_med.bmp"),
            LARGE : games.load_image("asteroid_big.bmp")}
    total = 0

    def __init__(self, game, x, y, size):
        super(Asteroid, self).__init__(image=Asteroid.images[size], x=x, y=y, \
            dx=random.choice([1, -1])*Asteroid.SPEED*random.random()/size, \
            dy=random.choice([1, -1])*Asteroid.SPEED*random.random()/size)
        self.size = size
        self.game = game
        Asteroid.total += 1

    
    def die(self):
        """Разрушает астероид."""
        # если размеры астероида крупные или средние, заменить его двумя более мелкими астероидами 
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game=self.game, x=self.x, y=self.y, size=self.size-1)
                games.screen.add(new_asteroid)
        super(Asteroid, self).die()
        Asteroid.total -= 1
        self.game.score.value += int(Asteroid.POINTS/self.size)
        self.game.score.right = games.screen.width - 10
        if Asteroid.total == 0:
            self.game.advance()


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
    astrocrash = Game()
    astrocrash.play()

# поехали!
main()