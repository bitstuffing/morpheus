
import requests
from core.slider import Slider, Slide
import json
import time
import random

class RandomRemoteIcon():

    def __init__(self, screen, firstColumn=0,lastColumn=56):
        self.screen = screen
        self.firstColumn = firstColumn
        self.lastColumn = lastColumn
        self.running = True
        self.store = False
        self.buffer = []

    def stop(self):
        print("stop RANDOM")
        self.running = False

    def run(self, category="popular"):
        if category is not None:
            response = requests.get(f'https://developer.lametric.com/api/v1/dev/preloadicons?page=1&category={category}&search=&count=1000&guest_icons=')
            res = response.json()
            i = None
            max = len(res["icons"])
            while i is None:
                x = random.randint(0,max)
                icon = res["icons"][x]
                if icon["thumbnail"] != "":
                    i = icon["id"]
        else:
            # get a random number from 1 to 59107
            i = random.randint(1, 59107)
        print("exploring: ", i)
        slider2 = self.drawRemoteBuffer(i)
        if slider2 is not None:
            mirrorSlides = []
            counter=0
            for slide in slider2.slides:
                
                buffer = self.screen.mirrorWithoutPillow(slide.buffer,int(slider2.fields),int(slider2.columns))
                if not self.running:
                    mirrorSlides = []
                    self.buffer = []
                    break
                slide = Slide(buffer, slide.delay)
                mirrorSlides.append(slide)
                counter+=1
            
            if self.running:

                slider = Slider("mirror",mirrorSlides, slider2.fields, slider2.columns)
                print("running...",str(self))

                self.screen.drawSliders(sliders=[slider2,slider],firstColumns=[self.firstColumn,self.lastColumn], forceShow=True)

                if self.store and slider2 is not None:
                    slider2.toJsonFile("slides3/")
        self.running = False


    def drawRemoteBuffer(self, id=661, show=True):
        jsonResponse = requests.get(f'https://developer.lametric.com/api/v1/dev/preloadicons?icon_id={id}').json()
        iconsJ = None
        try:
            iconsJ=json.loads(jsonResponse["body"])
        except:
            pass
        if self.running and iconsJ is not None and "icons" in iconsJ and len(iconsJ["icons"])>0:
            name = jsonResponse["name"]
            icons = iconsJ["icons"]
            delay = json.loads(jsonResponse["body"])["delays"]
            fields = self.screen.DIMENSION
            columns = len(icons[0][0])
            #columns = self.screen.DIMENSION
            slider = Slider(name, [], fields, columns)
            for x in range(len(icons)):
                # before instance buffer, check the number of fields and columns
                i=0
                icon = icons[x]
                buffer = [(0, 0, 0) for _ in range(fields*columns)]
                # should be one but...
                for iconData in icon:
                    # iconData is each column, and array of 8 columns with r,g,b,active
                    for index in range(len(iconData)):
                        field = iconData[index]
                        active = field[3]
                        #print(str(field))
                        if active:
                            # now get the iconData value = [0,0,0,0]
                            red = int(field[0] * 255)
                            green = int(field[1] * 255)
                            blue = int(field[2] * 255)
                            # parse "blue" to int
                            buffer[i] = (red, green, blue)
                            #print(str(buffer[i]))
                        else: 
                            buffer[i] = (0, 0, 0) # or background, now it's off
                        i+=1

                # now the buffer is turned 90 degrees and mirrored, so change matrix
                if columns == fields:
                    buffer = self.screen.rotate(buffer)
                    buffer = self.screen.mirror(buffer)
                
                # now copy the buffer to the screen
                
                delayMS = 0
                if len(delay)>0:
                    delayMS = delay[x] if delay[x] < 1000 else 1000
                if show and self.running:
                    #self.screen.drawBuffer(buffer)
                    self.buffer = buffer
                    time.sleep(delayMS*0.001)

                slide = Slide(buffer, delayMS)
                slider.add(slide)
                
            return slider
        else:
            print(f"none for index: {id}")