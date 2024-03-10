import time

from core.screen import Screen
from core.slider import Slider, Slide

from core.plugins.retroclock import RetroClock
from core.plugins.randomremoteicon import RandomRemoteIcon
from core.plugins.snake import Snake
from core.plugins.matrix import Matrix
from core.plugins.rainbow import Rainbow
from core.plugins.nyancat import NyanCat

screen = Screen()
screen.clear()

screen.drawText("   hello, this is a prove of concern with text and plugins, here we go!   ", (0, 0, 0), (255, 255, 255), True)
screen.showBuffer()

time.sleep(5)

screen.addPlugin(Rainbow(screen))
screen.runPlugins()
time.sleep(10)
screen.stopPlugins()
screen.cleanPlugins()

time.sleep(1)
screen.addPlugin(Matrix(screen))
screen.runPlugins()
time.sleep(10)
screen.stopPlugins()
screen.cleanPlugins()

time.sleep(1)
screen.addPlugin(NyanCat(screen))
screen.runPlugins()
time.sleep(10)
screen.stopPlugins()
screen.cleanPlugins()

time.sleep(1)
screen.addPlugin(Snake(screen))
screen.runPlugins()
time.sleep(100000)
