import board
import neopixel
from core.pillow import chatToMatrix
from core.slider import Slider, Slide
from core.buffer import Buffer
import time
import requests
import json
import numpy as np
import threading

class Screen(Buffer):

    def __init__(self) -> None:

        self.lock = threading.Lock()
        
        self.run_plugins = False
        self.alignToBottom = True
        self.GRADUAL_COLOR_FACTOR = 1
        self.DIMENSION = 8
        self.SCREENS = 8 # 4 panels of 8x8 pixels
        self.num_pixels = self.SCREENS*self.DIMENSION*self.DIMENSION # one panel of four 64 pixels matrix
        pixel_pin = board.D18
        ORDER = neopixel.GRB
        self.BRIGHTNESS = 0.1
        self.REFRESH_TIME = 0.1

        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, brightness=self.BRIGHTNESS, auto_write=False, pixel_order=ORDER
        )

        self.plugins = [] # TODO think about it

    def clear(self):
        self.buffer = [(0, 0, 0) for _ in range(self.num_pixels)]
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def addPlugin(self, plugin):
        self.plugins.append(plugin)

    def cleanPlugins(self):
        self.plugins = []
        if len(self.plugin_threads) > 0:
            self.run_plugins = False
            for thread in self.plugin_threads:
                # force kill the thread
                thread.stop()
            
            self.plugin_thread = []

        #self.clear()


    def runPlugins(self):
        self.run_plugins = True
        threading.Thread(target=self.runPluginsBackground).start()

    def runPluginsBackground(self):
        self.plugin_threads = {plugin: None for plugin in self.plugins}

        while self.run_plugins:
            for plugin in self.plugins:
                
                if self.run_plugins and ( plugin in self.plugin_threads and (self.plugin_threads[plugin] is None or not self.plugin_threads[plugin].is_alive())):
                    thread = threading.Thread(target=self.run, args=(plugin,))
                    thread.daemon = True
                    thread.start()
                    self.plugin_threads[plugin] = thread 
                
                time.sleep(self.REFRESH_TIME)

        self.clear()
        

    def run(self, plugin):
        plugin.run()
        if self.run_plugins:
            #print(f"buffer size: {len(plugin.buffer)}")
            self.drawBuffer(plugin.buffer, firstColumn=plugin.firstColumn, show=True)
        else:
            self.clear()


    def stopPlugins(self):
        self.run_plugins = False
        print("done!")

    def drawBuffer(self, buffer, firstColumn=0, columnSize=8, show=True):
        
        with self.lock:
            firstIndex = firstColumn * columnSize
            self.pixels[firstIndex:firstIndex+len(buffer)] = buffer
            if show:
                self.pixels.show()


    def drawBuffer2(self, buffer, firstColumn=0, columnSize=8, show=True):
        #print("drawBuffer2")
        num_pixels = len(buffer)
        firstIndex = firstColumn*columnSize
        for i in range(num_pixels):
            self.pixels[firstIndex+i] = buffer[i]
        if show:
            self.pixels.show()

    def drawText(self, targetText = "14:23:58", backgroundColor = (0, 0, 0), textColor = (255, 255, 255), changeColors = True):
        letter = []

        for i in range(len(targetText)):
            letter.append(chatToMatrix(targetText[i], 'types/Consolas.ttf', 10))
        
        self.drawBuffers(letter, backgroundColor, textColor, changeColors)


    def drawSliders(self, sliders=[], firstColumns=[], forceShow=True):
        #self.clear()
        print("drawSliders")
        if sliders is not None and sliders[0] is not None:
            for j in range(len(sliders[0].slides)): #first must be the master
                for i in range(len(sliders)):
                    if not self.run_plugins:
                        break
                    #print("call to drawBuffer from drawSliders")
                    self.drawBuffer(sliders[i].slides[j].buffer, firstColumn=firstColumns[i], show=forceShow)
                if forceShow:
                    self.pixels.show()
                time.sleep(int(sliders[0].slides[j].delay)*0.001) #first must be the master


    def drawSlider(self, slider, firstColumn=0, draw=True):
        print("drawSlider")
        rows = int(slider.fields) # could be self.DIMENSION but... I have written it in the .json to use it
        columns = int(slider.columns)
        screens = int(columns/rows)
        for slide in slider.slides:
            if columns != 8: # or True: because not it's working with "this part"
                # this fix correct the slides from de json file to the neopixel (in a matrix the pixels are soldered in a different order, for example 
                # the first column is soldered in the second column at the end, and the second column is soldered in the third column at the beginning
                # the .json file is ordered in fields, and the fields are ordered in a natural order, first row, second row, etc)
                # print(f"fix slides for columns {columns}: ")
                buffer2 = [(0, 0, 0) for _ in range(rows*columns)]
                for matriz in range(0,screens): # panels
                    counter=0
                    for column in range(0,self.DIMENSION):# panel-columns
                        for row in range(0,rows): #fields
                            if column % 2 == 1:
                                index2 = ((column+1) * rows) - row - 1  + (matriz*self.DIMENSION*self.DIMENSION)
                                targetIndex = columns*(column+1) - (int(columns/rows)*row) - (1) - matriz
                                buffer2[index2] = slide.buffer[targetIndex]
                            else:
                                index2 = counter + (matriz*self.DIMENSION*self.DIMENSION)
                                factor = (columns-(int(columns/rows)*row))
                                targetIndex = columns*(column+1) - factor + (matriz)
                                buffer2[index2] = slide.buffer[targetIndex]
                            counter+=1

                slide.buffer = buffer2
            if draw:
                self.drawBuffer(slide.buffer, firstColumn=firstColumn)
                time.sleep(int(slide.delay)*0.001)

        return slider


    def drawBuffers(self, letter, backgroundColor = (0, 0, 0), textColor = (255, 255, 255), changeColors = True):

        targetLetter = 0
        width = len(letter[targetLetter][0])
        height = len(letter[targetLetter])
        currentLetterStart = 0
        firstLetter = True

        # count the numer of columns to calculate the total buffer size
        self.totalColumns = 0
        for i in range(0, len(letter)):
            #print("adding size: ", len(letter[i][0]))
            self.totalColumns += len(letter[i][0]) 

        self.buffer = [(0, 0, 0) for _ in range(self.totalColumns*self.DIMENSION)]

        #buffer = [(0, 0, 0) for _ in range(num_pixels)]
        red = green = blue = 255
        changeRed = changeGreen = changeBlue = True
        #for i in range(DIMENSION*SCREENS):
        for i in range(self.DIMENSION*self.totalColumns):
            for j in range(height):
                if j < height and i < width:
                    targetPixel = i*self.DIMENSION + (self.DIMENSION-1-j) if i % 2 == 1 else i*self.DIMENSION + j

                    if self.alignToBottom:
                        difference = self.DIMENSION - height
                        targetPixel += difference if i % 2 == 0 else -difference

                    if letter[targetLetter][j][i-currentLetterStart] == 1:

                        if changeColors:
                            if red > self.GRADUAL_COLOR_FACTOR and changeRed:
                                red-=self.GRADUAL_COLOR_FACTOR
                            else:
                                changeRed = False
                                if red+self.GRADUAL_COLOR_FACTOR < 256:
                                    red += self.GRADUAL_COLOR_FACTOR
                                if green > self.GRADUAL_COLOR_FACTOR and changeGreen:
                                    green-=self.GRADUAL_COLOR_FACTOR
                                else:
                                    changeGreen = False
                                    if green+self.GRADUAL_COLOR_FACTOR < 256:
                                        green += self.GRADUAL_COLOR_FACTOR
                                    if blue > self.GRADUAL_COLOR_FACTOR and changeBlue:
                                        blue-=self.GRADUAL_COLOR_FACTOR
                                    else:
                                        if blue+self.GRADUAL_COLOR_FACTOR < 256:
                                            blue += self.GRADUAL_COLOR_FACTOR
                                        else:
                                            changeRed = changeGreen = changeBlue = True
                                        
                            textColor = (red, green, blue)
                        

                        self.buffer[targetPixel] = textColor
                    else:
                        self.buffer[targetPixel] = backgroundColor
                    if firstLetter:
                        print(f'FIRST char({i},{j}) -> {targetPixel} = {letter[targetLetter][j][i-currentLetterStart]}')
                    firstLetter = False
                    print(f'({i},{j}) -> {targetPixel} = {letter[targetLetter][j][i-currentLetterStart]}')
                else:
                    print(f'({i},{j}) -> is discarted width width and height: {width} and {height}')
                if width == i:
                    print(f"breaking in i = {i}")
                    break

            if i == width-1 and len(letter) > targetLetter+1:
                print("changing letter +1 ")
                firstLetter = True
                targetLetter += 1
                currentLetterStart = i+1
                width += len(letter[targetLetter][0])
                height = len(letter[targetLetter])
                print(f'new letter: {targetLetter} with width: {width} and height: {height}')


    def showBuffer(self):
        #for i in range(num_pixels):
        #    pixels[i] = buffer[i]
        #pixels.show()

        #for j in range(totalColumns-DIMENSION*SCREENS):
        # increase for by 2
        print(self.totalColumns*self.DIMENSION)
        additionalColumns = self.totalColumns-self.DIMENSION*self.SCREENS 
        if additionalColumns > 0:
            #print("additional columns: ", additionalColumns)
            for j in range(0, additionalColumns, 2):
                for i in range(self.num_pixels):
                    if j%2 ==0: 
                        self.pixels[i] = self.buffer[i+(j*self.DIMENSION)]
                    

                self.pixels.show()
                time.sleep(0.05)
        else:
            for i in range(len(self.buffer)):
                self.pixels[i] = self.buffer[i]
            self.pixels.show()

    def lightUp(self, color = (255, 255, 255)):
        self.pixels.brightness = 0.01 # be sure that you have enough power to do that
        for i in range(self.num_pixels):
            self.pixels[i] = color
        self.pixels.show()


