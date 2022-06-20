from multiprocessing.context import os
from turtle import width
import pygame
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1000,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Spaceship game")

WHITE = (255,255,255)
BLACK= (0,0,0)
RED = (255,0,0)
YELLOW = (255,255.0)

BORDER = pygame.Rect(0,250,1000,5)

BULLET_HIT_SOUND= pygame.mixer.Sound('pygam/Assets_Grenade+1.mp3')
BULLET_FIRE_SOUND= pygame.mixer.Sound('pygam/Assets_Gun_Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 40)

FPS= 60
VEL = 5
BULLET_VEL = 7 
MAX_BULLETS = 100
SPACESHIP_WIDTH, SAPCESHIP_HEIGHT = 70,90

ONE_HIT= pygame.USEREVENT + 1
TWO_HIT= pygame.USEREVENT + 2

Spaceship_image_one = pygame.transform.rotate(pygame.image.load(os.path.join('pygam','spaceshipone.png')),0)
Spaceship_one= pygame.transform.scale(Spaceship_image_one,(10,105))
Spaceship_image_two = pygame.transform.rotate(pygame.image.load(os.path.join('pygam','spaceshiptwo.png')),180)
Spaceship_two = pygame.transform.scale(Spaceship_image_two,(125,100))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('pygam','space.png')), (WIDTH,HEIGHT))

def draw_window( one, two, one_bullets, two_bullets, one_health, two_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,WHITE, BORDER)
   
    one_health_text = HEALTH_FONT.render("HEALTH: " + str(one_health),1,WHITE)
    two_health_text = HEALTH_FONT.render("HEALTH: " +str(two_health),1,WHITE)
    WIN.blit(one_health_text,(WIDTH - one_health_text.get_width() -770, 450))
    WIN.blit(two_health_text,(10,10))

    WIN.blit(Spaceship_one,( one.x, one.y ))
    WIN.blit(Spaceship_two,( two.x, two.y ))
    
    for bullet in one_bullets:
        pygame.draw.rect(WIN,RED, bullet)
    
    for bullet in two_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    
    pygame.display.update()

def handle_bullet(one_bullets, two_bullets, one, two):
    for bullet in two_bullets:
        bullet.y += BULLET_VEL
        if one.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ONE_HIT))
            two_bullets.remove(bullet)
        elif bullet.x < 0:
            two_bullets.remove(bullet)
    
    for bullet in one_bullets:
        bullet.y -= BULLET_VEL
        if two.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TWO_HIT))
            one_bullets.remove(bullet)
        elif bullet.x < 0:
            one_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    WIN.blit(draw_text,(WIDTH/2 - draw_text. get_width()/2, HEIGHT/2 - draw_text.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(5000)


    

def main():
    one = pygame.Rect(430, 350, SPACESHIP_WIDTH + 40, SAPCESHIP_HEIGHT)
    two = pygame.Rect(430, 20, SPACESHIP_WIDTH + 55, SAPCESHIP_HEIGHT)
    one_bullets = []
    two_bullets = []

    one_health = 20
    two_health = 20


    
    clock = pygame.time.Clock()
    run = True
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type  ==pygame. QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and len(two_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(two.x + two.width, two.y + two.height// 2 - 2,10,5)
                    two_bullets.append(bullet)
                    #bullet_fire_sound_play
                
                if event.key == pygame.K_s and len(one_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(one.x + one.width, one.y + one.height// 2 - 2,10,5)
                    one_bullets.append(bullet)
                    #bullet_fire_sound_play
            
            if event.type == ONE_HIT:
                one_health -= 1
            
            if event.type == TWO_HIT:
                two_health -= 1
            
        winner_text = ""
        if one_health == 0:
            winner_text = "SPACESHIP TWO WINS!"
        
        if two_health == 0:
            winner_text = "SPACESHIP ONE WINS"

        if winner_text != "":
            draw_winner(winner_text)
            break 

        keys_pressed = pygame.key.get_pressed()
        
        #spaceship one
        if keys_pressed[pygame.K_a]: #spaceone Left
            one.x -= VEL
        if keys_pressed[pygame.K_d]:# spaceone right
            one.x +=VEL
        # spaceship two
        if keys_pressed[pygame.K_LEFT]:# spacetwo Left
            two.x -= VEL
        if keys_pressed[pygame.K_RIGHT]:# spacetwo right
            two.x +=VEL
        
        
        draw_window(one, two, one_bullets, two_bullets, one_health, two_health)
        handle_bullet(one_bullets, two_bullets, one, two)
    
    pygame.quit()

if __name__ == "__main__":
    main()