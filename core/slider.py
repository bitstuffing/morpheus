import json

class Slider:

    slides = []

    def __init__(self):
        pass

    def __init__(self, name, slides, fields, columns):
        self.name = name
        self.slides = slides
        self.fields = fields
        self.columns = columns

    def add(self, slide):
        self.slides.append(slide)

    def toJSON(self):
        return {
            "name": self.name,
            "slides": [slide.toJson() for slide in self.slides],
            "fields": self.fields,
            "columns": self.columns
        }
        
    
    def fromJSON(self, jsonSlider):
        sliderJson = json.loads(jsonSlider)
        name = sliderJson["name"]
        slides = [Slide.fromJson(None,slide) for slide in sliderJson["slides"]]
        fields = sliderJson["fields"]
        columns = sliderJson["columns"]
        obj = Slider(name, slides, fields, columns)
        return obj

    def toJsonFile(self, fileName):
        
        #trim fileName to avoid errors
        fileName += self.name.replace(" ","_").replace("/","_") + ".json"
        print(f"saving file: {fileName}")
        # lowercase
        fileName = fileName.lower()

        with open(fileName, 'w') as f:
            json.dump(self.toJSON(), f)
        return fileName
    
    

class Slide:

    def __init__(self, buffer, delay=0):
        self.buffer = buffer
        self.delay = delay

    def toJson(self):
        return {
            "buffer": self.getBufferSerialized(),
            "delay": self.delay
        }
    
    def fromJson(self, jsonSlide):
        buffer = jsonSlide["buffer"]
        delay = jsonSlide["delay"]
        return Slide(buffer, delay)
    
    def getBufferSerialized(self):
        return [ [ int(pixel[0]),int(pixel[1]),int(pixel[2]) ] for pixel in self.buffer]
    

        
