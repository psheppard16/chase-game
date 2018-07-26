import math
from PIL import Image, ImageTk
import PIL
try:
    import pygame
except:
    pass
from tkinter import Canvas, NW
import os
import platform
from Screens.screen import Screen
class DrawingEngine(Screen):
    def __init__(self, window):
        super().__init__(window, "gameEngine")
        os.environ['SDL_WINDOWID'] = str(self.f.winfo_id())
        if platform.system() == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
            self.usePygame = True
            self.display = pygame.display.set_mode((self.window.width, self.window.height))
            self.display.fill((255,255,255))
            pygame.display.init()
            pygame.font.init()
        else:
            self.usePygame = False
            self.canvas = Canvas(self.window.root, bg="white", width=self.window.width, height = self.window.height)
            self.canvas.pack(in_=self.f)
        self.tkImageList = [] #images must maintain a reference in order to appear on the canvas



        self.scale = self.window.width / 1280

    def render(self):
        self.scale = self.window.width / 1280

        self.window.frameRate.startTimer("clear")
        if self.usePygame:
            self.display.fill((121, 202, 249))
        else:
            self.canvas.delete("all")
            self.canvas.create_rectangle(0, 0, self.window.width, self.window.height, fill = "#%02x%02x%02x" % (121, 202, 249))
            self.tkImageList.clear()
        self.window.frameRate.timeChange()

        self.showCircles()

        self.window.frameRate.startTimer("update")
        if self.usePygame:
            pygame.display.update()
            self.window.root.update() #must update while in canvas in pygame but not in tkinter
        else:
            self.canvas.update()
        self.window.frameRate.timeChange()

    def showCircles(self):
        self.showCircle(self.window.gameEngine.player.radius * self.scale, (self.getScreenX(self.window.gameEngine.player.x), self.getScreenY(self.window.gameEngine.player.y)), self.window.gameEngine.player.color)
        for circle in self.window.gameEngine.circleList:
            self.showCircle(circle.radius * self.scale, (self.getScreenX(circle.x), self.getScreenY(circle.y)), circle.color)

    def showRectangle(self, x1, y1, x2, y2, color, width=0):
        if self.usePygame:
            pygame.draw.rect(self.display, color, ((x1, y1), (x2 - x1, y2 - y1)))
            if width != 0:
                pygame.draw.rect(self.display, (0, 0, 0), ((x1, y1), (x2 - x1, y2 - y1)), width)
        else:
            tk_rgb = "#%02x%02x%02x" % color
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=tk_rgb, width=width)

    def showLine(self, position1, position2, color, width):
        if self.usePygame:
            pygame.draw.line(self.display, color, (int(position1[0]), int(position1[1])), (int(position2[0]), int(position2[1])), int(width))
        else:
            tk_rgb = "#%02x%02x%02x" % color
            self.canvas.create_line(position1[0], position1[1], position2[0], position2[1],
                                    fill=tk_rgb, width=width)

    def showText(self, text, position, color, fontName="Times", fontSize=12, bold=False, italic=False, anchorCenter=False, shadowWidth=0, secondaryColor=(0, 0, 0), outlineWidth=0):
        if self.usePygame:
            if outlineWidth!= 0:
                font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                screenText = font.render(text, 1, secondaryColor)
                if anchorCenter:
                    textW = screenText.get_width()
                    textH = screenText.get_height()
                else:
                    textW = 0
                    textH = 0

                for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                    x = outlineWidth * math.sin(angle)
                    y = outlineWidth * math.cos(angle)
                    self.display.blit(screenText, (int(position[0] - textW / 2) + x, int(position[1] - textH / 2) + y))
            elif shadowWidth != 0:
                font = pygame.font.SysFont(fontName, fontSize, bold, italic)
                screenText = font.render(text, 1, secondaryColor)
                if anchorCenter:
                    textW = screenText.get_width()
                    textH = screenText.get_height()
                else:
                    textW = 0
                    textH = 0
                for shift in range(shadowWidth):
                    self.display.blit(screenText, (int(position[0] - textW / 2) + shift, int(position[1] - textH / 2)))
            font = pygame.font.SysFont(fontName, fontSize, bold, italic)
            screenText = font.render(text, 1, color)
            if anchorCenter:
                textW = screenText.get_width()
                textH = screenText.get_height()
            else:
                textW = 0
                textH = 0
            self.display.blit(screenText, (int(position[0] - textW / 2), int(position[1] - textH / 2)))

        else:
            tk_rgb = "#%02x%02x%02x" % color
            fontString = fontName + " " + str(fontSize)
            if bold:
                fontString += " bold"
            if italic:
                fontString += " italic"
            if anchorCenter:
                if outlineWidth!= 0:
                    secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                    for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                        x = outlineWidth * math.sin(angle)
                        y = outlineWidth * math.cos(angle)
                        self.canvas.create_text(position[0] + x, position[1] + y, fill=secondary_tk_rgb, font=fontString, text=text)
                elif shadowWidth != 0:
                    secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                    for shift in range(shadowWidth):
                        self.canvas.create_text(position[0] + shift, position[1], fill=secondary_tk_rgb, font=fontString, text=text)
                self.canvas.create_text(position[0], position[1], fill=tk_rgb, font=fontString, text=text)
            else:
                if outlineWidth!= 0:
                    secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                    for angle in range(0, 361, int(8 / math.sqrt(outlineWidth)) + 1):
                        x = outlineWidth * math.sin(angle)
                        y = outlineWidth * math.cos(angle)
                        self.canvas.create_text(position[0] + x, position[1] + y, fill=secondary_tk_rgb, font=fontString, text=text, anchor=NW)
                elif shadowWidth != 0:
                    secondary_tk_rgb = "#%02x%02x%02x" % secondaryColor
                    for shift in range(shadowWidth):
                        self.canvas.create_text(position[0] + shift, position[1], fill=secondary_tk_rgb, font=fontString, text=text, anchor=NW)
                self.canvas.create_text(position[0], position[1], fill=tk_rgb, font=fontString, text=text, anchor=NW)


    def showImage(self, image, position, anchorCenter=False):
        if self.usePygame:
            if anchorCenter:
                imageW = image.get_width()
                imageH = image.get_height()
            else:
                imageW = 0
                imageH = 0
            self.display.blit(image, (int(position[0] - imageW / 2), int(position[1] - imageH / 2)))
        else:
            image = ImageTk.PhotoImage(image)
            self.tkImageList.append(image)
            if not anchorCenter:
                imageW = image.width()
                imageH = image.height()
            else:
                imageW = 0
                imageH = 0
            self.canvas.create_image((position[0] + imageW / 2, position[1] + imageH / 2), image=image)

    def showPolygon(self, pointList, color, position=(0, 0)):
        points = []
        for index in range(len(pointList)):
            points.append((pointList[index][0] + position[0], pointList[index][1] + position[1]))
        if self.usePygame:
            pygame.draw.polygon(self.display, color, points)
            pygame.draw.polygon(self.display, (0, 0, 0), points, 2)
        else:
            tk_rgb = "#%02x%02x%02x" % color
            self.canvas.create_polygon(points, outline='black', fill=tk_rgb, width=2)

    def showCircle(self, radius, position, color):
        try:
            if self.usePygame:
                pygame.draw.circle(self.display, color, (int(position[0]), int(position[1])), int(radius))
                pygame.draw.circle(self.display, (0, 0, 0), (int(position[0]), int(position[1])), int(radius), 2)
            else:
                tk_rgb = "#%02x%02x%02x" % color
                self.canvas.create_oval(position[0] - radius, position[1] - radius,
                                        position[0] + radius, position[1] + radius, fill=tk_rgb)
        except ValueError:
            pass

    def update(self):
        self.f.config(width=self.window.width, height=self.window.width)
        if self.usePygame:
            self.diplay = pygame.display.set_mode((self.window.width, self.window.height))
        else:
            self.canvas.config(width=self.window.width, height=self.window.height)

    def scaleImage(self, image, scale):
        newWidth = image.size[0] * scale
        wPercent = (newWidth/float(image.size[0]))
        hSize = int((float(image.size[1])*float(wPercent)))
        scaledImage = image.resize((int(newWidth), int(hSize)), PIL.Image.ANTIALIAS)
        return scaledImage

    def rotate(self, image, angle):
        if self.usePygame:
            return pygame.transform.rotate(image, angle)
        else:
            return self.rotatePIL(image, angle)

    def rotatePIL(self, image, angle):
        startSize = image.size
        imageString = image.convert('RGBA')
        rotatedImage = imageString.rotate(angle, expand=0).resize(startSize)
        finalImage = Image.new("RGBA", startSize, (255, 255, 255, 0))
        finalImage.paste(rotatedImage, (0, 0), rotatedImage)
        return finalImage

    def convertToDisplayFormat(self, image):
        if self.usePygame:
            imageBytes = image.convert('RGBA').tobytes("raw", 'RGBA')
            convertedImage = pygame.image.fromstring(imageBytes, image.size, 'RGBA')
        else:
            convertedImage = image
        return convertedImage

    def manipulateImage(self, image, scale, angle):
        scaledImage = self.scaleImage(image, scale)
        rotatedImage = self.rotatePIL(scaledImage, angle)
        finalImage = self.convertToDisplayFormat(rotatedImage)
        return finalImage

    def getScreenX(self, x):
        return x * self.scale

    def getScreenY(self, y):
        return (self.window.height - y) * self.scale