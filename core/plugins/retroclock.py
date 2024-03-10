from datetime import datetime
import time
import threading

REFRESH_TIME = 0.1

class RetroClock(threading.Thread):
    
    def __init__(self, firstColumn = 0, backgroundColor = (0, 0, 0), pixelColor = (255, 255, 255)):
        # 24:24 time is composed of 5 elements of 8x4 pixels
        elements = 8 # TODO, if you want more elements, you need to change the buffer size
        self.buffer =  [backgroundColor for _ in range((elements) * 8*4)]
        self.background = backgroundColor
        self.pixelColor = pixelColor
        self.running = True
        self.firstColumn = firstColumn

    def stop(self):
        print("stop RETRO")
        self.running = False

    # run in a new thread            
    def run(self):
        #print("run - clock")
        self.drawCurrentTime()
        time.sleep(REFRESH_TIME)

    def drawCurrentTime(self):
        # get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        #print("Current Time =", current_time)
        
        # draw the characters in the self.buffer, one by one
        for i in range(len(current_time)):
            self.drawChar(current_time[i], i )

    def drawChar(self, char, index):
        # get the char buffer
        charBuffer = self.getCharBuffer(char)
        # copy the char buffer to the self.buffer
        for i in range(len(charBuffer)):
            self.buffer[index*8*4 + i] = charBuffer[i]


    def getCharBuffer(self, char):
        # get the char buffer
        if char == "0":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.background, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "1":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.background, self.background, self.background, self.background, self.background, self.background, 
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "2":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "3":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.background, self.background, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "4":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.background,
                self.background, self.background, self.background, self.pixelColor, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "5":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background, self.pixelColor, self.background
            ]
        elif char == "6":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background,
                self.background, self.background, self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background, self.background, self.background 
            ]
        elif char == "7":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "8":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.background,
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == "9":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.background,
                self.background, self.pixelColor, self.background, self.pixelColor, self.background, self.background, self.background, self.background, 
                self.background, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.pixelColor, self.background
            ]
        elif char == ":":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.pixelColor, self.background, self.background, self.pixelColor, self.background, self.background,
            ]
        elif char == ".":
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.pixelColor, self.background,
            ]
        else: # TODO, blank or white-space
            return [
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
                self.background, self.background, self.background, self.background, self.background, self.background, self.background, self.background,
            ]
    
