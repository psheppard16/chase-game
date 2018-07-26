__author__ = 'psheppard16'
import random
import math
from GameObjects.mobile import Mobile
class Circle(Mobile):
    def __init__(self, window, x, y, radius, circleList, color=None):
        super().__init__(window, x, y, 0, 0)
        self.window = window
        self.radius = radius
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 128, 0), (255, 255, 0), (0, 255, 255), (128, 0, 255), (255, 0, 255)]
        if color == None:
            self.color = random.choice(self.colors)
        else:
            self.color = color
        self.circleList = circleList
        self.alive = True
        self.target = None
        self.moveStrength = 10
        self.accStrength = 10

    def run(self):
        self.move()
        try:
            xC = self.x - self.target.x
            yC = self.y - self.target.y
            angle = math.atan2(yC, xC)
            self.accelerate(self.accStrength * -math.cos(angle), self.accStrength * -math.sin(angle))
            self.shiftPosition(self.moveStrength * -math.cos(angle), self.moveStrength * -math.sin(angle))
        except:
            print("target")

    def isTouching(self, x, y, radius):
        if self.distanceToSelf(x, y) < self.radius + radius:
            return True
        else:
            return False