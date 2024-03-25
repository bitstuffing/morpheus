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

screen.drawText(" starting... ", (0, 0, 0), (255, 255, 255), True)
screen.showBuffer()
time.sleep(3)
screen.clear()

import random

while True:

    screen.addPlugin(RandomRemoteIcon(screen=screen, firstColumn=0))
    screen.addPlugin(RetroClock(screen=screen, firstColumn=16))
    screen.runPlugins()
    running = True
    while running:
        for plugin in screen.plugin_threads:
            if isinstance(plugin, RandomRemoteIcon):
                if plugin.running:
                    time.sleep(1)
                    running = True
                else:
                    running = False
    screen.stopPlugins()
    screen.cleanPlugins()
    time.sleep(1)

    # now get a random int to select one plugin
    element = random.randint(0, 3)
    if element == 0:
        screen.addPlugin(Rainbow(screen))
        screen.runPlugins()
        time.sleep(10)
        screen.stopPlugins()
        screen.cleanPlugins()

        time.sleep(1)
    elif element == 1:
        screen.addPlugin(Matrix(screen))
        screen.runPlugins()
        time.sleep(10)
        screen.stopPlugins()
        screen.cleanPlugins()

        time.sleep(1)
    elif element == 2:
        screen.addPlugin(NyanCat(screen))
        screen.runPlugins()
        time.sleep(10)
        screen.stopPlugins()
        screen.cleanPlugins()

        time.sleep(1)
    elif element == 3:
        screen.addPlugin(Snake(screen))
        screen.runPlugins()
        time.sleep(1) #running
        running = True
        while running:
            for plugin in screen.plugin_threads:
                if plugin.running:
                    time.sleep(1)
                    running = True
                else:
                    running = False
        screen.stopPlugins()
        screen.cleanPlugins()
        screen.clear()

