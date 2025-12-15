from pgzero.actor import Actor
from pygame import Rect
from config import *

class Entity:
    def __init__(self, x, y, name_prefix):
        self.x = x
        self.y = y
        self.name_prefix = name_prefix
        self.frame = 0
        self.anim_timer = 0
        self.moving = False
        self.actor = Actor(f"{name_prefix}_idle_0", (x, y))

    def animate(self):
        self.anim_timer += 1
        speed = 10 if self.moving else 20
        if self.anim_timer % speed == 0:
            self.frame = (self.frame + 1) % 2
            mode = "move" if self.moving else "idle"
            self.actor.image = f"{self.name_prefix}_{mode}_{self.frame}"

    def move(self, dx, dy, game_map):
        self.moving = (dx != 0 or dy != 0)

        if dx != 0:
            old_x = self.x
            self.x += dx
            self.actor.x = self.x
            if self.check_collision(game_map):
                self.x = old_x
                self.actor.x = self.x

        if dy != 0:
            old_y = self.y
            self.y += dy
            self.actor.y = self.y
            if self.check_collision(game_map):
                self.y = old_y
                self.actor.y = self.y

    def check_collision(self, game_map):
        hitbox = Rect(self.actor.topleft, (self.actor.width, self.actor.height)).inflate(-2,-2)
        points = [hitbox.topleft, hitbox.topright, hitbox.bottomleft, hitbox.bottomright]

        for px, py in points:
            if game_map.is_wall(px, py):
                return True
        return False

    def draw(self):
        self.actor.draw()
