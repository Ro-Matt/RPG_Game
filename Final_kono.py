from operator import truediv
import pygame
import random
import button


pygame.init()

clock = pygame.time.Clock()
fps = 60

#SCREEN
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FIGHT TO YOUR HEARTS CONTENT')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False




#define FONTS
font = pygame.font.SysFont('Times New Roman' , 26)

#define COLORS
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#background
background_img = pygame.image.load('img/Background/background.png').convert_alpha()

#panel
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

#button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()

#sword cursor
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()




#create function for TEXT
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


#draw background
def draw_bg():
    screen.blit(background_img, (0,0))

def draw_panel():
    #draw panel rectangle
    screen.blit(panel_img, (0,screen_height - bottom_panel))
    #show knight stats
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        #show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)
#fighter
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        # 0:idle, 1:attack, 2:hurt, 3:dead
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        #loading IDLE images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        #loading ATTACK images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        animation_cooldown = 100
        #handles animation
        self.image = self.animation_list[self.action][self.frame_index]
        
        #check ticks for update animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #loop animation at the end of index
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()        
    
     
    def attack(self, target):
        #deal damage
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #DEATH CHECK
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)    
        
        #attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
     
                
    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y ,hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        
    def draw(self, hp):
        #update with new hp
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
        
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        #FLOAT THE NUMBERS
        self.rect.y -= 1
        #FADE AWAY
        self.counter += 1
        if self.counter > 77:
            self.kill()
        
damage_text_group = pygame.sprite.Group()
        

        
knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

#HEALTH BARS
knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)


run = True
while run:
    
    clock.tick(fps)
    
    #draw background
    draw_bg()
    
    #draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)
    
    #draw fighters
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()
        
    #DRAW DMG TEXT
    damage_text_group.update()
    damage_text_group.draw(screen)

    #CONTROL PLAYER ACTION
    #reset action variables
    attack = False
    potion = False
    target = None
    
    #mouse visible
    pygame.mouse.set_visible(True)
    
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword instead of mouse
            screen.blit(sword_img, pos)
            if clicked == True:
                attack = True
                target = bandit_list[count]
    
    if potion_button.draw():
        potion = True
    #SHOW NUM OF POTIONS
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)
    
    
    #player action
    if knight.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                #look for player action
                #ATTACK
                if attack == True and target != None:
                    knight.attack(target)
                    current_fighter += 1
                    action_cooldown = 0
                #POTION
                if potion == True:
                    if knight.potions > 0:
                        #CHECK POTION HEAL BEYOND MAX HP
                        if knight.max_hp - knight.hp > potion_effect:
                            heal_amount = potion_effect
                        else:
                            heal_amount = knight.max_hp - knight.hp
                        knight.hp += heal_amount
                        knight.potions -= 1
                        damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                        damage_text_group.add(damage_text)
                        current_fighter += 1
                        action_cooldown = 0
                        
                
    #enemy action
    for count, bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #HEAL BANDIT
                    if(bandit.hp/bandit.max_hp) < 0.5 and bandit.potions > 0:
                        #CHECK POTION HEAL BEYOND MAX HP
                        if bandit.max_hp - bandit.hp > potion_effect:
                            heal_amount = potion_effect
                        else:
                            heal_amount = bandit.max_hp - bandit.hp
                        bandit.hp += heal_amount
                        bandit.potions -= 1
                        damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                        damage_text_group.add(damage_text)
                        current_fighter += 1
                        action_cooldown = 0
                    else:                       
                        #attack
                        bandit.attack(knight)
                        current_fighter +=1
                        action_cooldown = 0
            else:
                current_fighter += 1
                
    #if all fighters have had their turn reset
    if current_fighter > total_fighters:
        current_fighter = 1
        
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
            
            
    pygame.display.update()
            

pygame.quit()

