import os
import time
import random

class Snake:
    def __init__(self, screen, width=64, height=8, firstColumn=0):
        self.screen = screen
        self.width = width
        self.height = height
        self.snake = [(0, 0)]
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.direction = self.directions[0]
        self.food = None
        self.firstColumn = firstColumn
        self.buffer =  [(0,0,0) for _ in range(width*height)]

    def move(self):
        head = self.snake[0]
        new_head = ((head[0] + self.direction[0]) % self.width, (head[1] + self.direction[1]) % self.height)
        if new_head in self.snake:
            return False  # game over
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = None  # eat the food
        else:
            self.snake.pop()  # move the tail
        if self.food is None:
            while True:
                self.food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
                if self.food not in self.snake:
                    break
        return True

    def change_direction(self):
        # calculate the direction to the food
        head = self.snake[0]
        dx = self.food[0] - head[0]
        dy = self.food[1] - head[1]
        if abs(dx) > abs(dy):  # move in x direction
            self.direction = self.directions[0] if dx > 0 else self.directions[2]
        else:  # move in y direction
            self.direction = self.directions[1] if dy > 0 else self.directions[3]

        # check if the next move will cause a collision with the snake itself
        new_head = ((head[0] + self.direction[0]) % self.width, (head[1] + self.direction[1]) % self.height)
        if new_head in self.snake:
            # ff a collision is predicted, change direction
            safe_directions = [d for d in self.directions if d != self.direction]
            random.shuffle(safe_directions)  # shuffle the safe directions
            for d in safe_directions:
                new_head = ((head[0] + d[0]) % self.width, (head[1] + d[1]) % self.height)
                if new_head not in self.snake:
                    self.direction = d
                    break

    def get_frame(self):
        frame = [[(0,0,0) for _ in range(self.width)] for _ in range(self.height)]
        for x, y in self.snake:
            frame[y][x] = (0,255,0)
        if self.food is not None:
            frame[self.food[1]][self.food[0]] = (255,0,0)
        return frame
    
    def stop(self):
        print("stop SNAKE")
        self.running = False

    def run(self):
        screens = 8
        rows = self.height
        columns = self.width
        dimensions = 8
        self.running = True
        emptyBuffer = [(0, 0, 0) for _ in range(rows*columns)]
        while self.move() and self.running:
            self.change_direction()

            buffer2 = self.get_frame()
            
            # now we have a buffer2 with x,y coordinators, and now we have to convert to a vector
            buffer = []
            for x in range(columns):
                for y in range(rows):
                    if x % 2 == 0:
                        buffer.append(buffer2[y][x])
                    else:
                        buffer.append(buffer2[rows-y-1][x])

            
            self.buffer = buffer
            # Update the neopixels
            self.screen.drawBuffer(buffer)

            time.sleep(0.02)
            
        self.running = False
