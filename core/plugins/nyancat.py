import time

class NyanCat:
    def __init__(self, screen, width=64, height=8):
        self.screen = screen
        self.width = width
        self.height = height
        self.buffer = [(0,0,0) for _ in range(width*height)] 
        self.phase = 0
        self.tail_colors = [(255,0,0), (255,165,0), (255,255,0), (0,255,0)]  # stela colors
        
        self.dif2 = 0
        self.pre = False

    def stop(self):
        print("stop RAINBOW TRAIL")
        self.running = False

    # an stela is centered in the screen, and then the cat is moving the stela change position
    def generateStela(self, start = 0, nyancat = 50, startPoint = 0, endPoint = 64, nyancatSize = 10, stelaChangeWidth = 5):
        dif = 1
        margin = 2
        
        marginTop = 1 # min distance to top
        marginBottom = 3 # max distance to bottom
        
        if start % 4 != 0:
            # change it
            if self.dif2 == 1 or self.dif2 == -1:
                self.dif2 = 0
            else:
                self.dif2 = 1 if self.pre else -1
                self.pre = not self.pre 
        for x in range(startPoint, endPoint): # rows
            if (start + x) % stelaChangeWidth == 0:
                margin += dif
                if margin == 1:
                    dif = 1
                elif margin == 3:
                    dif = -1
                else:
                    dif = 0
                    margin = 3
                
            for y in range(self.height): # fields
                index = x*self.height + y if x % 2 == 0 else ((x+1)*self.height) - y - 1
                if y + dif - 3 > -2 and y + 3 + dif < self.height and x <= nyancat:
                    self.buffer[index] = self.tail_colors[(x-self.phase) % 4]
                elif x > nyancat and x <= nyancat + nyancatSize:
                    if y - self.dif2 - marginTop > 0 and y + marginBottom - self.dif2 <= self.height :
                        #print(self.dif2, x)
                        if (x - 1 == nyancat or x -1 == nyancat + nyancatSize -1): 
                            self.buffer[index] = (30,30,30)
                            pass
                        elif y - marginTop - self.dif2 == 1:
                            self.buffer[index] = (30,30,30) # grey top
                        elif y + marginBottom - self.dif2 == self.height:
                            self.buffer[index] = (30,30,30) # grey bottom
                        else:
                            self.buffer[index] = (255,100,100) # pinky cat body
                    else:
                        self.buffer[index] = (0,0,100) # around nyancat
                else: # no rainbow no nyancat
                    self.buffer[index] = (0,0,100) 
      

    def run(self):
        self.running = True
        counter = 0
        while self.running:

            self.phase = (self.phase + 1) % 4  # color phase change 
            counter = counter+1 if counter < self.width else 0 # stela movement
            
            self.generateStela(start = counter)

            # Update the neopixels
            self.screen.drawBuffer(self.buffer)
            time.sleep(0.1)
