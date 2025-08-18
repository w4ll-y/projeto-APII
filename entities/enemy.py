import pygame
from random import randint 
from settings import *
from entities.player import Player
from entities.entity import Entity
from utils.suport import resize_image, import_folder_resize_image, read_settings
from utils.enums import DropType
from levels.tiles.drop import Drop
from core.config import Config


class Enemy(Entity):
    def __init__(self, id, pos, groups, obstacle_sprites,damage_player, drop_groups, settings: Config, create_gun_enemy_attack):
        self.settings = settings
        self.difficult = settings.difficult

        #geral
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #grafico
        self.import_graphics(id)
        self.move_status = 'down_idle'
        self.image = self.animations[self.move_status][self.frame_index]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.id = id
        self.enemy_info = ENEMY_DATA[self.id]
        self.health = self.enemy_info['health'] * (self.difficult - self.difficult / 2)
        self.speed = self.enemy_info['speed'] * (self.difficult - self.difficult / 2)
        self.attack_damage = self.enemy_info['damage'] * (self.difficult - self.difficult / 2)
        self.resistance = self.enemy_info['resistance'] * (self.difficult - self.difficult / 2)
        self.attack_radius = self.enemy_info['attack_radius']
        self.notice_radius = self.enemy_info['notice_radius']
        self.attack_type = self.enemy_info['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1000
        self.damage_player = damage_player
        self.gun = GUNS_DATA[1]
        self.create_gun_enemy_attack = create_gun_enemy_attack

        self.vulnerable = True
        self.hit_time = None
        self.invencibilyty_duration = 300

        self.drop_groups = drop_groups

    def ajust_difficult(self):
        if self.settings.difficult != self.difficult:
            self.difficult = self.settings.difficult

            self.health = self.enemy_info['health'] * (self.difficult - self.difficult / 2)
            self.speed = self.enemy_info['speed'] * (self.difficult - self.difficult / 2)
            self.attack_damage = self.enemy_info['damage'] * (self.difficult - self.difficult / 2)
            self.resistance = self.enemy_info['resistance'] * (self.difficult - self.difficult / 2)

    def import_graphics(self, id):
        self.animations = {
        'up': [], 'down': [], 'left': [], 'right': [],
        'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
        'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}

        main_path = f'assets/sprites/enemies/{id}/'
        for animaton in self.animations.keys():
            self.animations[animaton] = import_folder_resize_image(main_path + animaton)


    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)
    
    def get_status(self,player):
        distance, direction = self.get_player_distance_direction(player)

        # decide direção principal (parecido com o player.input())
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                base_status = "right"
            else:
                base_status = "left"
        else:
            if direction.y > 0:
                base_status = "down"
            else:
                base_status = "up"

        if distance <= self.attack_radius and self.can_attack:
            if "attack" not in self.move_status:
                self.frame_index = 0
            self.move_status = base_status + "_attack"
            
        elif distance <= self.notice_radius:
                self.move_status = base_status
        else:
            self.move_status = base_status + "_idle"

    def actions(self,player):
        distance, direction = self.get_player_distance_direction(player)
        if 'attack' in self.move_status:
            if self.id == 2:
                self.attack_time = pygame.time.get_ticks()
                self.damage_player(self.attack_damage,self.attack_type)
                self.direction = pygame.math.Vector2()
            elif self.id == 0:
                self.attack_time = pygame.time.get_ticks()
                self.create_gun_enemy_attack(150, self.move_status, self.rect)
                self.direction = pygame.math.Vector2()


        elif 'idle' not in self.move_status:
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.move_status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
           
            if 'attack' in self.move_status:
                self.can_attack = False
            self.frame_index = 0


        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invencibilyty_duration:
                self.vulnerable = True
            
    def get_damaged(self,player, attack_type):
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage(attack_type)
            elif(attack_type == 'gun'):
                self.health -= player.get_full_weapon_damage(attack_type)
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if 'attack' in self.move_status: #gambiarra pros inimigos não ficarem muito tempo atirando
                self.can_attack = False
                self.frame_index = 0
        if self.health <= 0:
            self.drop()
            self.kill()

    def drop(self):
        n = randint(1, 100)
        
        pos = {'center': (self.rect.center[0] + 20, self.rect.center[1] + 20)}
        
        if n <= 20:
            Drop(self.drop_groups, DropType.HEALTH, pos)
        if 20 < n <= 40:
            Drop(self.drop_groups, DropType.BULLET, pos)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def enemy_update(self, player: Player):
        if player.getting_item is not None or player.paused_game:
            return
        
        self.ajust_difficult()
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
        self.get_status(player)
        self.actions(player)
