#  Copyright (c) 2020.
#  By Jorn Schampheleer
import random

from DinoAI.DinoAI.GameObjects.obstacle import Obstacle

MIN_TIME_BETWEEN_SPAWN = 1
SPAWN_RATE = 0.1


class ObstacleSpawner(object):
    def __init__(self, surfacewidth, surfaceheight):
        self.speed = 100
        self.time_since_last_spawn = 0
        self.obstacles = []
        self.surfacewidth = surfacewidth
        self.surfaceheight = surfaceheight

    def update(self, deltatime):
        self.time_since_last_spawn += deltatime
        if self.time_since_last_spawn > (MIN_TIME_BETWEEN_SPAWN/(self.speed/100)) and random.random() < SPAWN_RATE:
            self.obstacles.append(Obstacle(self.surfacewidth, self.surfaceheight))
            self.obstacles[-1].increase_speed(self.speed)
            self.time_since_last_spawn = 0
        if len(self.obstacles) > 0 and self.obstacles[0].is_offscreen():
            self.obstacles.pop(0)

    def is_colliding(self, dinosaur):
        for obstacle in self.obstacles:
            if obstacle.is_colliding(dinosaur):
                return True
        return False

    def get_next_obstacle_xy(self, dinosaur):
        for obstacle in self.obstacles:
            if obstacle.x + obstacle.texture.get_size()[0] > dinosaur.x:
                return obstacle.x, obstacle.relative_y
        return None

    def increase_speed(self, newspeed):
        self.speed = newspeed
        for obstacle in self.obstacles:
            obstacle.increase_speed(newspeed)
