from GameObjects.circle import Circle
import random
import math
class GameEngine:
    def __init__(self, window):
        self.window = window
        self.circleList = []
        self.arenaSize = 1000
        self.player = Circle(self.window, 1280 / 2, 720 / 2, 10, self.circleList)
        self.spawnCircles()

    def run(self):
        self.runCircles()
        mouseX = self.window.root.winfo_pointerx() - self.window.root.winfo_rootx()
        mouseY = self.window.root.winfo_pointery() - self.window.root.winfo_rooty()
        xC = mouseX - self.player.x * 1280 / self.window.width
        yC = self.player.y * 1280 / self.window.width - mouseY
        angle = math.atan2(yC, xC)
        self.player.shiftPosition(25 * -math.cos(angle), 25 * -math.sin(angle))

    def runCircles(self):
        for circle in self.circleList:
            circle.run()

    def spawnCircles(self):
        numberOfBlobs = 15
        lowestRadius = 1
        maxRadius = 5
        for i in range(numberOfBlobs):
            x = random.randint(0, 1280)
            y = random.randint(0, 720)
            radius = random.randint(lowestRadius, maxRadius)
            self.circleList.append(Circle(self.window, x, y, radius, self.circleList))
        for circle in self.circleList:
            if self.circleList.index(circle) != 0:
                target = self.circleList[self.circleList.index(circle) - 1]#random.choice(self.circleList)
                circle.target = target
            else:
                circle.target = self.player
            #while target == circle:
            #    target = random.choice(self.circleList)

    def kp(self, event):
        pass

    def kr(self, event):
        pass

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)





