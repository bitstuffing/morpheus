import colorsys
import time

class Rainbow:
    def __init__(self, screen, width=64, height=8):
        self.screen = screen
        self.width = width
        self.height = height
        self.buffer = [(0,0,0) for _ in range(width*height)]
        self.phase = 0

    def stop(self):
        print("stop RAINBOW")
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.phase = (self.phase + 13) % 360
            for i in range(self.width*self.height):
                hue = (i + self.phase) % 360 / 360.0
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
                self.buffer[i] = (r, g, b)
            
            # convert the buffer to the NeoPixel format
            buffer2 = [self.buffer[y*self.width:(y+1)*self.width] for y in range(self.height)]
            buffer = []
            for x in range(self.width):
                for y in range(self.height):
                    if x % 2 == 0:
                        buffer.append(buffer2[y][x])
                    else:
                        buffer.append(buffer2[self.height-y-1][x])
            
            # update the neopixels
            self.screen.drawBuffer(buffer)
            time.sleep(0.05)
