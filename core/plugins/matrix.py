import random
import time

class Matrix:
    def __init__(self, screen, width=64, height=8):
        self.screen = screen
        self.width = width
        self.height = height
        self.buffer = [(0,0,0) for _ in range(width*height)]
        self.waiting = [False for _ in range(width*height)]
        self.speeds = [1 for _ in range(width*height)]

    def stop(self):
        print("stop MATRIX")
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # create a new line at the top with random speeds
            new_line = [(0, random.randint(0, 255), 0) if random.random() < 0.1 else (0, 0, 0) for _ in range(self.width)]
            new_speeds = [random.randint(4, 20) if c == (0, 255, 0) and random.random() < 0.02 else s for c, s in zip(new_line + self.buffer[:-self.width], self.speeds + [1]*self.width)]
            # move everything down and fade the color
            self.buffer = [self.fade_color(c) if not w else c for c, w in zip(new_line + self.buffer[:-self.width], self.waiting + [False]*self.width)]
            self.waiting = [random.random() < 0.02 if c == (0, 255, 0) else w for c, w in zip(self.buffer, self.waiting + [False]*self.width)]
            self.speeds = new_speeds
            
            # convert the buffer to the NeoPixel format
            buffer2 = [self.buffer[y*self.width:(y+1)*self.width] for y in range(self.height)]
            buffer = []
            for x in range(self.width):
                for y in range(self.height):
                    if x % 2 == 0:
                        buffer.append(buffer2[y][x])
                    else:
                        buffer.append(buffer2[self.height-y-1][x])
            
            self.screen.drawBuffer(buffer)
            time.sleep(0.05 / self.speeds[random.randint(0, self.width*self.height-1)])

    # reduce the green component to create the trail effect
    def fade_color(self, color):
        r, g, b = color
        g = max(g - 5, 0)  # reduce the amount subtracted for longer trails
        # if the pixel is waiting, its color shoudl change to white or gray
        if (r, g, b) == (0, 255, 0) and random.random() < 0.02:
            return random.choice([(255, 255, 255), (192, 192, 192), (128, 128, 128), (64, 64, 64)])
        elif (r, g, b) == (0, 255, 0):
            return (255, 255, 255) if random.random() < 0.1 else (0, 255, 0)
        return r, g, b
