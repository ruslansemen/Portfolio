class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def within_x(co1, co2):
    if co1.x1 > co2.x1 and co1.x1 < co2.x2:
        return True
    elif co1.x2 > co2.x1 and co1.x2 < co2.x2:
        return True
    elif co2.x1 > co1.x1 and co2.x1 < co1.x2:
        return True
    elif co2.x2 > co1.x1 and co2.x2 < co1.x2:
        return True
    else:
        return False


c1 = Coords(40, 40, 100, 100)
c2 = Coords(50, 50, 150, 150)
# within_x(c1, c2)
print(within_x(c1, c2))
