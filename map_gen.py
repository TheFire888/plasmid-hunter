import random
from pygame import Rect
from config import *

class GameMap:
    def __init__(self):
        self.grid = []
        self.rooms = []
        self.visible = set()
        self.generate()

    def is_blocking(self, x, y):
        if not (0 <= x < (WIDTH // TILE_SIZE) and 0 <= y < (HEIGHT // TILE_SIZE)):
            return True
        return self.grid[y][x] == 0

    def generate(self):
        cols = WIDTH // TILE_SIZE
        rows = HEIGHT // TILE_SIZE
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for _ in range(20):
            w, h = random.randint(5, 10), random.randint(5, 10)
            x, y = random.randint(1, cols - w - 1), random.randint(1, rows - h - 1)
            new_room = Rect(x, y, w, h)
            
            failed = any(new_room.colliderect(o.inflate(2, 2)) for o in self.rooms)
            if not failed:
                self.create_room(new_room)
                if self.rooms:
                    pc = self.rooms[-1].center
                    nc = new_room.center
                    if random.randint(0, 1):
                        self.h_tunnel(pc[0], nc[0], pc[1])
                        self.v_tunnel(pc[1], nc[1], nc[0])
                        self.create_joint(nc[0], pc[1])
                    else:
                        self.v_tunnel(pc[1], nc[1], pc[0])
                        self.h_tunnel(pc[0], nc[0], nc[1])
                        self.create_joint(pc[0], nc[1])
                self.rooms.append(new_room)

    def create_room(self, r):
        for x in range(r.x, r.x + r.w):
            for y in range(r.y, r.y + r.h):
                self.grid[y][x] = 1

    def h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.grid[int(y)][int(x)] = 1
            self.grid[int(y)+1][int(x)] = 1

    def v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.grid[int(y)][int(x)] = 1
            self.grid[int(y)][int(x)+1] = 1

    def create_joint(self, x, y):
        x, y = int(x), int(y)
        for i in range(x, x + 2):
            for j in range(y, y + 2):
                if 0 <= i < len(self.grid[0]) and 0 <= j < len(self.grid):
                    self.grid[j][i] = 1

    def is_wall(self, x, y):
        gx, gy = int(x // TILE_SIZE), int(y // TILE_SIZE)
        if 0 <= gx < (WIDTH // TILE_SIZE) and 0 <= gy < (HEIGHT // TILE_SIZE):
            return self.grid[gy][gx] == 0
        return True

    def update_fov(self, hero_x, hero_y):
        self.visible.clear()
        gx, gy = int(hero_x // TILE_SIZE), int(hero_y // TILE_SIZE)
        radius = 6 # Raio de visão

        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i == -radius or i == radius or j == -radius or j == radius:
                    self.cast_ray(gx, gy, gx + i, gy + j)

        # FIXME: Essa parte garante que será possível visualizar 
        # todas as paredes adjacentes a cada chão visível. Isso concerta 
        # um bug visual, mas parece pouco otimizado.
        extra_walls = set()
        for (x, y) in self.visible:
            if self.grid[y][x] == 1:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < (WIDTH // TILE_SIZE) and 0 <= ny < (HEIGHT // TILE_SIZE):
                            if self.grid[ny][nx] == 0:
                                extra_walls.add((nx, ny))

        self.visible.update(extra_walls)

    def cast_ray(self, x0, y0, x1, y1):
        # Algoritmo de Bresenham
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if 0 <= x0 < (WIDTH // TILE_SIZE) and 0 <= y0 < (HEIGHT // TILE_SIZE):
                self.visible.add((x0, y0))

                if self.grid[y0][x0] == 0:
                    break

            if x0 == x1 and y0 == y1: break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if (x,y) in self.visible:
                    img = "floor" if tile == 1 else "wall"
                    screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))
