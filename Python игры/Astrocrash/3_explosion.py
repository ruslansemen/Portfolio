# Взрыв
# Демонстрирует создание анимации
from livewires import games
games.init(screen_width=640, screen_height=480, fps=50)
nebula_image = games.load_image("nebula.jpg", transparent=False)
games.screen.background = nebula_image
# exp1 = games.load_image("explosion1.bmp")
# exp2 = games.load_image("explosion2.bmp")
# exp3 = games.load_image("explosion3.bmp")
# exp4 = games.load_image("explosion4.bmp")
# exp5 = games.load_image("explosion5.bmp")
# exp6 = games.load_image("explosion6.bmp")
# exp7 = games.load_image("explosion7.bmp")
# exp8 = games.load_image("explosion8.bmp")
# exp9 = games.load_image("explosion9.bmp")
# explosion_files = [exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8, exp9]

explosion_files = ["explosion1.bmp", 
                    "explosion2.bmp", 
                    "explosion3.bmp", 
                    "explosion4.bmp", 
                    "explosion5.bmp", 
                    "explosion6.bmp", 
                    "explosion7.bmp", 
                    "explosion8.bmp", 
                    "explosion9.bmp"]
explosion = games.Animation(images=explosion_files, \
    x=games.screen.width/2, \
    y=games.screen.height/2, \
    n_repeats=0, repeat_interval=10)

games.screen.add(explosion)
games.screen.mainloop()