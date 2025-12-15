import random
import math
from entity import Entity
from config import *

class Phage(Entity):
    def __init__(self):
        super().__init__(0, 0, "phage")
        self.vx = 0
        self.vy = 0
        self.speed = 1.0

        
    def update(self, target, game_map):
        dx = target.x - self.x
        dy = target.y - self.y
        dist = math.hypot(dx, dy)

        move_x, move_y = 0, 0

        if dist < 80:
            if dist > 0:
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed
        else:
            if random.randint(0, 50) == 0:
                self.vx = random.choice([-1, 1]) * 0.5
                self.vy = random.choice([-1, 1]) * 0.5
            move_x = self.vx
            move_y = self.vy

        self.move(move_x, move_y, game_map)
        self.animate()
