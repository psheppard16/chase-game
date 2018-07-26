__author__ = 'psheppard16'
import tkinter
import pickle
from Screens.instructions import Instructions
from Screens.startScreen import StartScreen
from Window.frameRate import FrameRate
from Game.gameEngine import GameEngine
from SaveFiles.saveFile import SaveFile
from Screens.options import Options
from Screens.mainMenu import MainMenu
from Display.drawingEngine import DrawingEngine
class Window:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.cMenu = "null"
        self.rMenu = "startScreen"

        self.saveNumber = 0
        self.saveSelected = False
        self.save = SaveFile()
        self.saveCharacter(1) # resets the saves
        self.saveCharacter(2)
        self.saveCharacter(3)

        self.root = tkinter.Tk()
        self.root.title("Red Shooter")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.bind_all('<KeyPress>', self.kp)
        self.root.bind_all('<KeyRelease>', self.kr)

        self.screenList = [] #when an object that extends Screen is created it automatically adds itself to screenList
        self.frameRate = FrameRate(self)
        self.startScreen = StartScreen(self)
        self.instructions = Instructions(self)
        self.drawingEngine = DrawingEngine(self)
        self.options = Options(self)
        self.mainMenu = MainMenu(self)
        self.gameEngine = GameEngine(self)

        self.root.after(1, self.loop)
        self.root.mainloop()

    def loop(self):
        while True:
            if self.frameRate.getTime() > self.frameRate.nextTick:
                self.frameRate.tickStartTime = self.frameRate.getTime()

                self.updateFrameSizes()
                self.switchScreen()

                if self.cMenu == "gameEngine":
                    self.root.focus_force()
                    self.gameEngine.run()
                    self.drawingEngine.render()
                self.frameRate.update()
                self.root.update()

    def switchScreen(self):
        if self.cMenu != self.rMenu:
            self.clearWindow()
            for screen in self.screenList:
                if self.rMenu == screen.name:
                    screen.setUp()
            if self.rMenu == "gameEngine":
                self.gameEngine = GameEngine(self)
            self.cMenu = self.rMenu

    def clearWindow(self):
        for screen in self.screenList:
            screen.hide()

    def updateFrameSizes(self):
        if str(self.width) + 'x' + str(self.height) != self.save.resolution:
            self.root.geometry(self.save.resolution)
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
            for screen in self.screenList:
                screen.update()

    def loadChar(self, number):
        try:
            if number == 1:
                with open('SaveFiles/saveFile1', 'rb') as input:
                    self.save = pickle.load(input)
            elif number == 2:
                with open('SaveFiles/saveFile2', 'rb') as input:
                    self.save = pickle.load(input)
            elif number == 3:
                with open('SaveFiles/saveFile3', 'rb') as input:
                    self.save = pickle.load(input)
        except EOFError:
            return {}

    def saveCharacter(self, number):
        if number == 1:
            with open('SaveFiles/saveFile1', 'wb') as output:
                pickle.dump(self.save, output, pickle.HIGHEST_PROTOCOL)
        elif number == 2:
            with open('SaveFiles/saveFile2', 'wb') as output:
                pickle.dump(self.save, output, pickle.HIGHEST_PROTOCOL)
        elif number == 3:
            with open('SaveFiles/saveFile3', 'wb') as output:
                pickle.dump(self.save, output, pickle.HIGHEST_PROTOCOL)

    def kp(self, event):
        if self.cMenu == "gameEngine":
            if self.hosting:
                self.serverEngine.kp(event)
            else:
                self.connectionEngine.connection.kp(event)

    def kr(self, event):
        if self.cMenu == "gameEngine":
            if self.hosting:
                self.serverEngine.kr(event)
            else:
                self.connectionEngine.connection.kr(event)