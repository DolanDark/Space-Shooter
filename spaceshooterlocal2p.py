import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 1000,600
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("First Game")
white = (255,255,255)
bg_color = (126, 111, 199)
black_test  = (0,0,0)
red_color = (255,0,0)
yellow_color = (249,215,28)

partition = pygame.Rect(0,height//2 - 5, width, 10)

bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
fps = 60
velocity = 5
bullet_vel = 7
max_bull = 6

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

ship_width, ship_height = 55,40

yellow_spaceship = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellowship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship,(ship_width,ship_height)),180)

red_spaceship = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
redship = pygame.transform.scale(red_spaceship,(ship_width,ship_height))

health_font = pygame.font.SysFont('comicsans',30)
winner_font = pygame.font.SysFont('comicsans',100)

space = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(width,height))

def draw_win(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    #window.fill(bg_color)
    window.blit(space,(0,0))
    pygame.draw.rect(window, black_test, partition)
    red_health_txt = health_font.render("Health : " + str(red_health),1,white)
    yellow_health_txt = health_font.render("Health : " + str(yellow_health),1,white)
    window.blit(yellow_health_txt,(10,height - yellow_health_txt.get_height() -10))
    window.blit(red_health_txt,(width - red_health_txt.get_width() - 10, 10))

    window.blit(yellowship,(yellow.x, yellow.y))
    window.blit(redship,(red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(window, red_color, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(window, yellow_color, bullet)

    pygame.display.update()

def yellow_movemnet(key_press, yellow):
    if key_press[pygame.K_a] and yellow.x - velocity > 0 :  # LEFT
        yellow.x -= velocity
    if key_press[pygame.K_d] and yellow.x + velocity < width - ship_width:  # RIGHT
        yellow.x += velocity
    if key_press[pygame.K_w] and yellow.y - velocity > partition.y + 5:  # UP
        yellow.y -= velocity
    if key_press[pygame.K_s] and yellow.y + velocity < height - ship_height :  # Down
        yellow.y += velocity

def red_movement(key_press, red):
    if key_press[pygame.K_LEFT] and red.x - velocity > 0:  # LEFT
        red.x -= velocity
    if key_press[pygame.K_RIGHT] and red.x + velocity < width - ship_width :  # RIGHT
        red.x += velocity
    if key_press[pygame.K_UP] and red.y > 0 :  # UP
        red.y -= velocity
    if key_press[pygame.K_DOWN] and red.y < partition.y - ship_height:  # Down
        red.y += velocity

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.y -= bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.y < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y += bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.y > width:
            red_bullets.remove(bullet)

def winner_banner(text):
    win_text = winner_font.render(text, 1, white)
    window.blit(win_text,(width/2 - win_text.get_width()/2,height/2 - win_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(450, 10, ship_width, ship_height)
    yellow = pygame.Rect(450,550, ship_width, ship_height)

    red_bullets = []
    yellow_bullets = []

    clk = pygame.time.Clock()

    red_health = 10
    yellow_health = 10

    run = True
    while run :
        clk.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(yellow_bullets) < max_bull:
                    bullet = pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height, 5,10)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bull:
                    bullet = pygame.Rect(red.x + red.width//2, red.y + red.height, 5, 10)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()

            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "" :
            winner_banner(winner_text)
            break

        print(red_bullets,yellow_bullets)
        key_press = pygame.key.get_pressed()
        yellow_movemnet(key_press, yellow)
        red_movement(key_press, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()