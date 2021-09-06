#StratLytic 2020


class Point(object):
    def __init__(self, ax = 0, ay = 0):
        self.setxy(ax, ay)
        self.highlighted = False


    def copyfrom(self, pointcopyfrom):
        self.setxy(pointcopyfrom.x, pointcopyfrom.y)
        self.highlighted = pointcopyfrom.highlighted


    def setxy(self, ax: int, ay: int):
        self.x = ax
        self.y = ay
