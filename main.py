import pgzrun
import random
from pgzero.actor import Actor
from config import *
from map_gen import GameMap
from player import Bacterium
from enemies import Phage
from battle import BattleSystem
from ui import Text

current_state = STATE_MENU
level = 1
active_enemy = None
current_track = None
input_lock = 0

game_map = None
hero = Bacterium()
battle_sys = BattleSystem()
enemies = []
items = []

def play_music(track_name):
    global current_track
    if current_track != track_name:
        music.play(track_name)
        current_track = track_name
        music.set_volume(0.5)

def start_level():
    global game_map, enemies, items, level
    game_map = GameMap()
    
    start_room = game_map.rooms[0]
    hero.x, hero.y = start_room.centerx * TILE_SIZE, start_room.centery * TILE_SIZE
    hero.actor.pos = (hero.x, hero.y)
    
    enemies = []
    num_enemies = 2 + level
    for _ in range(num_enemies):
        if len(game_map.rooms) > 1:
            room = random.choice(game_map.rooms[1:])
            p = Phage()
            p.x, p.y = room.centerx * TILE_SIZE, room.centery * TILE_SIZE
            p.actor.pos = (p.x, p.y)
            enemies.append(p)
    
    items = []
    if len(game_map.rooms) > 1:
         room = random.choice(game_map.rooms[1:])
         items.append(Actor("plasmid", (room.centerx * TILE_SIZE, room.centery * TILE_SIZE)))


def update():
    global current_state, active_enemy, level, current_track, input_lock

    if input_lock > 0:
        input_lock -= 1
    
    if current_state == STATE_MENU:
        play_music("menu")
        if keyboard.space and input_lock == 0:
            level = 1
            hero.plasmids = []
            hero.hp = 100
            start_level()
            current_state = STATE_MAP
            play_music("exploration")
            input_lock = 30
            
    elif current_state == STATE_PAUSE:
        if keyboard.r:
            current_state = STATE_MAP

    elif current_state == STATE_MAP:
        if keyboard.p:
            current_state = STATE_PAUSE
            
        hero.update(keyboard, game_map)
        game_map.update_fov(hero.x, hero.y)

        for phage in enemies:
            phage.update(hero, game_map)
            phage_grid = (int(phage.x // TILE_SIZE), int(phage.y // TILE_SIZE))
            if phage_grid in game_map.visible:
                if hero.actor.colliderect(phage.actor.inflate(-2, -2)):
                    current_state = STATE_BATTLE
                    active_enemy = phage
                    sounds.encounter.play()
                    play_music("battle")
                    battle_sys.start_battle(difficulty=level)
        
        for item in items[:]:
            if hero.actor.colliderect(item):
                hero.plasmids.append("buff")
                items.remove(item)
                sounds.collect.play()

                if len(hero.plasmids) == 100:
                    current_state = STATE_WIN
                    play_music("menu")
                    input_lock = 60
                else:
                    level += 1
                    start_level()
        
    elif current_state == STATE_BATTLE:
        battle_sys.update(hero, sounds) 
        
        if hero.hp <= 0:
            current_state = STATE_GAME_OVER
            play_music("menu")
            input_lock = 60

        if battle_sys.cooldown > 0:
            battle_sys.cooldown -= 1
            if battle_sys.cooldown == 0 and "ELIMINATED" in battle_sys.message:
                current_state = STATE_MAP
                if active_enemy in enemies: enemies.remove(active_enemy)
                play_music("exploration")

        else:
            if keyboard.K_1: battle_sys.check_answer(0, hero, sounds)
            elif keyboard.K_2: battle_sys.check_answer(1, hero, sounds)
            elif keyboard.K_3: battle_sys.check_answer(2, hero, sounds)
            elif keyboard.K_4: battle_sys.check_answer(3, hero, sounds)

    elif current_state == STATE_WIN:
        if keyboard.space and input_lock == 0:
            current_state = STATE_MENU
            input_lock = 30

    elif current_state == STATE_GAME_OVER:
        if keyboard.space and input_lock == 0:
            input_lock = 30
            current_state = STATE_MENU

def draw():
    screen.clear()
    
    if current_state == STATE_MENU:
        screen.fill((10, 10, 20))
        Text.draw(screen, TITLE, center=(WIDTH/2, HEIGHT/3), fontsize=30, color="green")
        Text.draw(screen, "PRESS SPACE TO START", center=(WIDTH/2, HEIGHT/2))
        
    elif current_state == STATE_PAUSE:
        game_map.draw(screen)
        hero.draw()
        screen.draw.text("PAUSED", center=(WIDTH/2, HEIGHT/2), fontsize=40, color="white")
        screen.draw.text("Press R to Resume", center=(WIDTH/2, HEIGHT/2 + 40), fontsize=20)

    elif current_state == STATE_MAP:
        game_map.draw(screen)
        
        for item in items:
            gx, gy = int(item.x // TILE_SIZE), int(item.y // TILE_SIZE)
            if (gx, gy) in game_map.visible: item.draw()
                
        for p in enemies:
            gx, gy = int(p.x // TILE_SIZE), int(p.y // TILE_SIZE)
            if (gx, gy) in game_map.visible: p.draw()
                
        hero.draw()
        
        Text.draw(screen, f"HP: {hero.hp}", pos=(10, 10))
        Text.draw(screen, f"LVL: {level}", pos=(WIDTH-60, 10), color="yellow")
        Text.draw(screen, f"Plasmids: {len(hero.plasmids)}", pos=(10, 25), color="cyan")
    
    elif current_state == STATE_BATTLE:
        battle_sys.draw(screen, hero.hp)
        
    elif current_state == STATE_GAME_OVER:
        screen.fill((50, 0, 0))
        Text.draw(screen, "GAME OVER", center=(WIDTH/2, HEIGHT/2), fontsize=40)
        Text.draw(screen, "Press SPACE", center=(WIDTH/2, HEIGHT/2 + 50))
        Text.draw(screen, f"You collected {len(hero.plasmids)} Plasmids.", center=(WIDTH/2, HEIGHT/2 + 90), fontsize=15)

    elif current_state == STATE_WIN:
        screen.fill((0, 50, 0))
        Text.draw(screen, "YOU WIN!", center=(WIDTH/2, HEIGHT/2 - 20), fontsize=30, color="yellow")
        Text.draw(screen, f"You collected all {len(hero.plasmids)} Plasmids.", center=(WIDTH/2, HEIGHT/2 + 40), fontsize=15)
        Text.draw(screen, "Press SPACE to Menu", center=(WIDTH/2, HEIGHT/2 + 80), fontsize=12)

pgzrun.go()
