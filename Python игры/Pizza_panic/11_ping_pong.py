# Игра в пинг-понг
from livewires import games
import random

games.init(screen_width=640, screen_height=480, fps=50)

# _________________________________________
# доработка игры - ввожу отдельные классы для ракетки и мяча

class Racket(games.Sprite):
    """Ракетка, которой игрок отбивает мяч."""
    image = games.load_image("racket.bmp")

    def __init__(self):
        super().__init__(image=Racket.image, x=games.mouse.x, bottom=games.screen.height - 25)

    def update(self):
        self.x = games.mouse.x
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        self.check_collide()

    def check_collide(self):
        for ball in self.overlapping_sprites:
            ball.handle_collide()


class Ball(games.Sprite):
    """Мяч, отскакивает от трёх границ поля и ракетки игрока."""
    image = games.load_image("ball.bmp")
    def __init__(self):
        super().__init__(image=Ball.image, x=games.screen.width/2, y=games.screen.height/2, dx=1, dy=1)

    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            self.dx = - self.dx
        if self.top < 0 or self.bottom > games.screen.height:
            self.dy = - self.dy

    def handle_collide(self):
        self.dy = - self.dy
        d_speed = random.randrange(-1, 2)
        self.dx += d_speed 



# _________________________________________

field_image = games.load_image("field.jpg", transparent=False)
games.screen.background = field_image
# racket_image = games.load_image("racket.bmp")
# racket = games.Sprite(image=racket_image, x=200, y=150)
the_racket = Racket()
games.screen.add(the_racket)
# ball_image = games.load_image("ball.bmp")
# ball = games.Sprite(image=ball_image, x=250, y=200)
the_ball = Ball()
games.screen.add(the_ball)
games.mouse.is_visible = False
games.screen.event_grab = True
# games.screen.add(ball)
games.screen.mainloop()