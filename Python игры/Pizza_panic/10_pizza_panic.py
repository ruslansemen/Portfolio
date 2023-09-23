# Паника в пиццерии
# Игрок должен ловить падающую пиццу, пока она не достигла земли
# HW: доработка игры так, чтобы сложность игрового процесса
# постепенно возрастала. С достижением счёта очков определённых пределов
# увеличивается скорость падения пиццы, скорость перемещения повара, 
# возникает на экране второй сумасшедший повар.
from livewires import games, color
import random
games.init(screen_width=640, screen_height=480, fps=50)

class Pan(games.Sprite):
    """Сковорода, в которую игрок может ловить падающую пиццу."""
    # введение нового атрибута класса для хранения счёта
    var_score = 0
    image = games.load_image("pan.bmp")
    def __init__(self):
        """Инициализирует объект Pan и создаёт \
            объект Text для отображения счёта."""
        super(Pan, self).__init__(image=Pan.image, \
            x=games.mouse.x, bottom=games.screen.height)
        self.score = games.Text(value=0, size=25, \
            color=color.black, top=5, right=games.screen.width-10)
        games.screen.add(self.score)

    def update(self):
        """Передвигает объект по горизонтали \
        в точку с абсциссой, как у указателя мыши."""
        self.x = games.mouse.x
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        self.check_catch()

    def check_catch(self):
        for pizza in self.overlapping_sprites:
            Pan.var_score += 10
            self.score.value = Pan.var_score
            self.score.right = games.screen.width - 10
            pizza.handle_caught()

class Pizza(games.Sprite):
    """Круг пиццы, падающий на землю."""
    image = games.load_image("pizza.bmp")
    speed = 1
    # вводятся доп. атрибуты класса
    gear_1 = False
    gear_2 = False
    
    def __init__(self, x, y=90):
        super(Pizza, self).__init__(image=Pizza.image, \
        x=x, y=y, dy=Pizza.speed)

    def update(self):
        """Проверяет, не коснулась ли нижняя \
        кромка спрайта нижней границы экрана"""
        if self.bottom > games.screen.height:
            self.end_game()
            self.destroy()

    def handle_caught(self):
        """Разрушает объект, пойманный игроком."""
        self.destroy()
        if Pan.var_score > 500 and not Pizza.gear_1:
            Pizza.speed = 1.2
            Pizza.gear_1 = True
        if Pan.var_score > 1000 and not Pizza.gear_2:
            Pizza.speed = 1.5
            Pizza.gear_2 = True
        
    def end_game(self):
        """Завершает игру."""
        end_message = games.Message(value="Game Over", \
            size=90, color=color.red, x=games.screen.width/2, \
            y=games.screen.height/2, lifetime=5*games.screen.fps, \
            after_death=games.screen.quit)
        games.screen.add(end_message)

class Chef(games.Sprite):
    """Кулинар, который двигаясь влево-вправо, разбрасывает пиццу."""
    image = games.load_image("chef.bmp")
    var_time_til_drop = 0
    var_change_speed = False
    new_chef = False

    def __init__(self, y=55, speed=2, odds_change = 200):
        """Инициирует объект Chef."""
        super(Chef, self).__init__(image=Chef.image, \
            x=games.screen.width/2, \
            y=y, dx=speed)
        self.odds_change = odds_change
        self.time_til_drop = Chef.var_time_til_drop

    def update(self):
        """Определяет, надо ли сменить направление."""
        if self.left < 0 or self.right > games.screen.width:
            self.dx = - self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = - self.dx
        self.check_drop()

    def check_drop(self):
        """Уменьшает интервал ожидания на единицу \
            или сбрасывает очередную пиццу и восстанавливает \
            исходный интервал."""
        if Chef.var_time_til_drop > 0:
            Chef.var_time_til_drop -= 1
            self.time_til_drop = Chef.var_time_til_drop
        else:
            new_pizza = Pizza(x=self.x)
            games.screen.add(new_pizza)
            # вне зависимости от скорости падения пиццы 
            # расстояние между падающими кругами принимается 
            # равным 30% каждого из них по высоте
            if (Pan.var_score > 480) and (Pan.var_score < 520):
                Chef.var_time_til_drop = int(new_pizza.height*13/Pizza.speed) + 1
                self.time_til_drop = Chef.var_time_til_drop
            elif (Pan.var_score > 980) and (Pan.var_score < 1020):
                Chef.var_time_til_drop = int(new_pizza.height*13/Pizza.speed) + 1
                self.time_til_drop = Chef.var_time_til_drop
                if not Chef.var_change_speed:
                    self.dx = 3
                    Chef.var_change_speed = True
            elif Pan.var_score == 1500 and (not Chef.new_chef):
                the_chef2 = Chef(speed=3)
                games.screen.add(the_chef2)
                Chef.new_chef = True
            else:
                Chef.var_time_til_drop = int(new_pizza.height*1.3/Pizza.speed) + 1
                self.time_til_drop = Chef.var_time_til_drop


def main():
    """Игровой процесс."""
    wall_image = games.load_image("wall.jpg", transparent=False)
    games.screen.background = wall_image
    the_chef = Chef()
    games.screen.add(the_chef)
    # другой повар
    # the_chef2 = None
    the_pan = Pan()
    games.screen.add(the_pan)
    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()

# Поехали
if __name__ == "__main__":
    main()

