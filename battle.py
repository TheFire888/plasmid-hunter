import random
from ui import Text
from config import *
from pygame import Rect

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
        length = 9 + difficulty * 3
        self.timer = 240 + (difficulty * 60)

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
        Text.draw(screen, f"HP: {hero_hp}", pos=(20, 20), color="white", fontsize=15)
        
        timer_seconds = int(self.timer / 60)
        timer_color = "red" if timer_seconds <= 5 else "gold"
        Text.draw(screen, f"{timer_seconds}", center=(WIDTH/2, 40), fontsize=30, color=timer_color, shadow=(1,1))
        
        Text.draw(screen, self.message, center=(WIDTH/2, 100), fontsize=15, color="yellow")

        chunk_size = 21
        chunks = [self.enemy_dna[i:i+chunk_size] for i in range(0, len(self.enemy_dna), chunk_size)]
        formatted_dna = "\n".join(chunks)
        Text.draw(screen, "VIRAL SEQUENCE:", center=(WIDTH/2, 140), fontsize=12, color="red")
        dna_rect = Rect(40, 160, WIDTH - 80, 200)
        Text.draw_textbox(screen, formatted_dna, dna_rect, color="#ff4444")

        section_width = WIDTH // 4
        y_pos = HEIGHT - 60
        
        for i, opt in enumerate(self.options):
            x_center = (i * section_width) + (section_width // 2)
            Text.draw(screen, f"[{i+1}]", center=(x_center, y_pos), fontsize=10, color="gray")
            Text.draw(screen, opt, center=(x_center, y_pos + 20), fontsize=18, color="white")
