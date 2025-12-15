import random
from ui import Text
from config import *

class BattleSystem:
    def __init__(self):
        self.active = False
        self.enemy_dna = ""
        self.options = []
        self.correct_index = -1
        self.message = ""
        self.cooldown = 0
        self.timer = 0

    def start_battle(self, difficulty):
        self.active = True
        self.message = "MATCH ENZYME!"
        length = 10 + difficulty * 2
        self.timer = max(100, 600 - (difficulty * 50))

        bases = ["A", "T", "C", "G"]
        self.enemy_dna = "".join(random.choice(bases) for _ in range(length))
        
        start = random.randint(0, length - 4)
        correct = self.enemy_dna[start : start + 3]
        
        self.options = []
        while len(self.options) < 3:
            p = "".join(random.choice(bases) for _ in range(3))
            if p not in self.enemy_dna: self.options.append(p)
            
        self.correct_index = random.randint(0, 3)
        self.options.insert(self.correct_index, correct)

    def update(self, hero, sounds):
        if self.cooldown == 0:
            self.timer -= 1
            if self.timer <= 0:
                self.timer = 0
                hero.hp -= 5
                self.message = "TIME OUT! DAMAGE!"
                sounds.damage.play()
                self.timer = 180

    def check_answer(self, index, hero, sounds):
        if self.cooldown > 0: return
        if index == self.correct_index:
            self.message = "ELIMINATED!"
            self.cooldown = 60
            sounds.correct.play()
        else:
            hero.hp -= 10
            self.cooldown = 60
            self.message = "DAMAGE TAKEN!"
            sounds.damage.play()

    def draw(self, screen, hero_hp):
        screen.fill((30, 0, 0))
        Text.draw(screen, f"HP: {hero_hp}s", pos=(10, 10), color="white")
        Text.draw(screen, f"TIMER: {int(self.timer/60)}s", pos=(WIDTH-100, 10), color="orange")
        Text.draw(screen, f"VIRAL DNA:\n{self.enemy_dna}", pos=(50, 80), fontsize=20, color="red")
        Text.draw(screen, self.message, center=(WIDTH/2, 40), fontsize=15, color="yellow")
        
        for i, opt in enumerate(self.options):
            Text.draw(screen, f"{i+1}: {opt}", pos=(100, 200 + i * 40), fontsize=12)
