import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

#SCREEN
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FIGHT TO YOUR HEARTS CONTENT')


#load images
#background
background_img = pygame.image.load('img/Background/background.png').convert_alpha()

#panel
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()


#draw background
def draw_bg():
    screen.blit(background_img, (0,0))

def draw_panel():
    screen.blit(panel_img, (0,screen_height - bottom_panel))


run = True
while run:
    
    clock.tick(fps)
    
    #draw
    draw_bg()
    draw_panel()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            
    pygame.display.update()
            

pygame.quit()

