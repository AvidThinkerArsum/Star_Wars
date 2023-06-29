import pygame
import os
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game Again")

BORDER = pygame.Rect(WIDTH//2 - 5, 0 ,10 ,HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'spaceship_red.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90 )
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'spaceship_yellow.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))     #setting screen background
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))    #setting red
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  #setting yellow
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()
    
def draw_winner(winner_text):
    draw_text = WINNER_FONT.render('Winner: ' + str(winner_text), 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > WIDTH//2 + BORDER.width//2:   #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIDTH:   #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:    #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT:    #down
        red.y += VEL
        
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:   #moving left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x +yellow.width + VEL < WIDTH//2 - BORDER.width//2: #moving right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT:  #down
        yellow.y += VEL
        
def handle_bullets(red, yellow, red_bullets, yellow_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 5//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RETURN and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -5//2 - 5//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        if red_health <= 0:
            winner_text = "Yellow wins"
            draw_winner(winner_text)
            break
        if yellow_health <= 0:
            winner_text = "Red wins"
            draw_winner(winner_text)
            break
                             
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow)
        handle_bullets(red, yellow, red_bullets, yellow_bullets)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    pygame.quit()
    
if __name__ == "__main__":
    main()
