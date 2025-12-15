from entity import Entity
from config import *

class Bacterium(Entity):
    def __init__(self):
        super().__init__(0, 0, "bac")
        self.hp = 100
        self.plasmids = []
        self.speed = 3

    def update(self, keyboard, game_map):
        dx, dy = 0, 0
        if keyboard.A: dx = -self.speed
        if keyboard.D: dx = self.speed
        if keyboard.W: dy = -self.speed
        if keyboard.S: dy = self.speed

        self.move(dx, dy, game_map)
        self.animate()
