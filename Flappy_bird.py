import pygame
import random
import math
import time

LARGEUR_ECRAN = 600
HAUTEUR_ECRAN = 600

score = 0
speed = 1
controle_jeu = 0
multiple = 1

pygame.init()
screen = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
score_font = pygame.font.SysFont("Arialbold", 53)
flappy_font = pygame.font.SysFont("Arialbold", 73)
flappy_font_2 = pygame.font.SysFont("Arialbold", 44)
exit_font = pygame.font.SysFont("Arialbold", 33)

BIRD_BITMAP = pygame.image.load("bird.png").convert()
BIRD_HIT_BITMAP = pygame.image.load("bird_hit.png").convert()
GAME_OVER_BITMAP = pygame.image.load("Game_Over.png").convert()
PIPE_UP_1_BITMAP = pygame.image.load("pipe_2_1.png").convert()
PIPE_UP_2_BITMAP = pygame.image.load("pipe_2_2.png").convert()
PIPE_DOWN_1_BITMAP = pygame.transform.rotate(PIPE_UP_1_BITMAP, 180)
PIPE_DOWN_2_BITMAP = pygame.transform.rotate(PIPE_UP_2_BITMAP, 180)

bird_x, bird_y = 10, (HAUTEUR_ECRAN/2) - (BIRD_BITMAP.get_height()/2)

pygame.display.set_caption('flappy bird Imrann')
screen.blit(BIRD_BITMAP, (bird_x, bird_y))

EMPTY_BLOCK = BIRD_BITMAP.get_height() + 30
n_pipe_block = int(math.ceil((float(LARGEUR_ECRAN)/PIPE_UP_1_BITMAP.get_width()))) + 1
n_pipe_block1 = int(math.ceil((float(LARGEUR_ECRAN)/PIPE_DOWN_1_BITMAP.get_width()))) + 1

pipe_up_array = []
pipe_down_array = []

pipe_up_array.append((0, bird_y + (BIRD_BITMAP.get_height()/2) - (EMPTY_BLOCK/2) - PIPE_UP_1_BITMAP.get_height()))
pipe_down_array.append((0, pipe_up_array[0][1] + EMPTY_BLOCK + PIPE_UP_1_BITMAP.get_height()))

for ii in range(1, n_pipe_block):
    if ii <= 4:
        x = ii * PIPE_UP_1_BITMAP.get_width()
        pipe_up_array.append((x, pipe_up_array[0][1]))
        pipe_down_array.append((x, pipe_down_array[0][1]))
        x = ii * PIPE_UP_1_BITMAP.get_width()

def draw_pipe_up(x, y):
    screen.blit(PIPE_UP_1_BITMAP, (x, y))
    h = PIPE_UP_2_BITMAP.get_height()
    x = x + 12
    y = y - h
    while y > -h:
        screen.blit(PIPE_UP_2_BITMAP, (x, y))
        y = y - h

def draw_pipe_down(x, y):
    screen.blit(PIPE_DOWN_1_BITMAP, (x, y))
    h = PIPE_DOWN_2_BITMAP.get_height()
    x = x + 12
    y = y + PIPE_DOWN_1_BITMAP.get_height()
    while y < HAUTEUR_ECRAN:
        screen.blit(PIPE_DOWN_2_BITMAP, (x, y))
        y = y + h

def print_score():
    s = str(score)
    text = score_font.render("Score: " + s, True, (255, 128, 0))
    x = LARGEUR_ECRAN - text.get_width() - 10
    screen.blit(text, (x, 10))

def print_flappy():
    text = flappy_font.render("Flappy bird", True, (255, 128, 0))
    screen.blit(text, (150, 200))
    text = flappy_font_2.render("Press Space bar to start", True, (255, 128, 0))
    screen.blit(text, (50, 300))

def check_overlap_x(x1, x2, xp1, xp2):
    if (xp1 >= x1) and (xp1 <= x2):
        return True
    if (xp2 >= x1) and (xp2 <= x2):
        return True
    if (x1 >= xp1) and (x1 <= xp2):
        return True
    if (x2 >= xp1) and (x2 <= xp2):
        return True
    return False

def check_collision(x1, y1, w, h, xp1, yp1, wp1, hp1):
    x2 = x1 + w
    xp2 = xp1 + wp1
    y2 = y1 + h
    yp2 = yp1 + hp1
    if check_overlap_x(x1, x2, xp1, xp2) == False:
        return False
    if check_overlap_x(y1, y2, yp1, yp2) == False:
        return False
    return True

def check_collision_with_pipe(x1, y1, w, h, xp1, yp1, wp1, hp1):
    bird_w = BIRD_BITMAP.get_width()
    bird_h = BIRD_BITMAP.get_height()
    if check_collision(bird_x, bird_y, bird_w, bird_h, x1, y1, w, h) == True:
        return True
    if check_collision(bird_x, bird_y, bird_w, bird_h, xp1, yp1, wp1, hp1) == True:
        return True
    return False

def check_collision_with_all_pipes():
    for i in range(2):
        x1, y1 = pipe_up_array[i]
        w = PIPE_UP_1_BITMAP.get_width()
        h = PIPE_UP_1_BITMAP.get_height()
        xp1 = x1 + 12
        yp1 = 0
        wp1 = PIPE_UP_2_BITMAP.get_width()
        hp1 = y1 - yp1
        if check_collision_with_pipe(x1, y1, w, h, xp1, yp1, wp1, hp1) == True:
            return True
    for i in range(2):
        x1, y1 = pipe_down_array[i]
        w = PIPE_DOWN_1_BITMAP.get_width()
        h = PIPE_DOWN_1_BITMAP.get_height()
        xp1 = x1 + 12
        yp1 = y1 + PIPE_DOWN_1_BITMAP.get_height()
        wp1 = PIPE_DOWN_2_BITMAP.get_width()
        hp1 = HAUTEUR_ECRAN - yp1
        if check_collision_with_pipe(x1, y1, w, h, xp1, yp1, wp1, hp1) == True:
            return True
    return False

def game_over():
    screen.blit(GAME_OVER_BITMAP, (100, 200))
    s = str(score)
    text = score_font.render("Ton score: " + s, True, (255, 128, 0))
    screen.blit(text, (200, 400))
    text = exit_font.render("Press Space bar to restart", True, (255, 128, 0))
    screen.blit(text, (145, 450))

def new_empty_block(i):
    (x_up, y_up) = pipe_up_array[i-1]
    y_up = y_up + PIPE_UP_1_BITMAP.get_height()
    (x_down, y_down) = pipe_down_array[i-1]
    x = PIPE_UP_1_BITMAP.get_width() * i
    chemin = random.randint(0, 3)
    if chemin == 0:
        y = y_up + ((y_down - y_up)/2) - (EMPTY_BLOCK/2)
        pipe_up_array[i] = (x, y - PIPE_UP_1_BITMAP.get_height())
        pipe_down_array[i] = (x, y + EMPTY_BLOCK)
    elif chemin == 1:
        y = y_up - EMPTY_BLOCK
        if y < 0:
            y = 0
        pipe_up_array[i] = (x, y - PIPE_UP_1_BITMAP.get_height())
        pipe_down_array[i] = (x, y + (EMPTY_BLOCK*2))
    else:
        y = y_down + EMPTY_BLOCK
        if y > (HAUTEUR_ECRAN - EMPTY_BLOCK):
            y = HAUTEUR_ECRAN - EMPTY_BLOCK
        pipe_up_array[i] = (x, y - (EMPTY_BLOCK*2) - PIPE_UP_1_BITMAP.get_height())
        pipe_down_array[i] = (x, y)

def game():
    global score
    global speed
    global controle_jeu
    global multiple
    screen.fill((0, 168, 243))
    for i in range(len(pipe_up_array)):
        x, y = pipe_up_array[i]
        draw_pipe_up(x, y)
        x = x - speed
        pipe_up_array[i] = (x, y)
        x, y = pipe_down_array[i]
        draw_pipe_down(x, y)
        x = x - speed
        pipe_down_array[i] = (x, y)
    x, y = pipe_up_array[0]
    if x <= (-PIPE_UP_1_BITMAP.get_width()):
        for i in range(1, len(pipe_up_array)):
            pipe_up_array[i-1] = pipe_up_array[i]
        for i in range(1, len(pipe_down_array)):
            pipe_down_array[i-1] = pipe_down_array[i]
        new_empty_block(i)
        score = score + 1
        if speed <= 25:
            if score == multiple * 25:
                speed = speed * 2
                multiple = multiple + 1
    if check_collision_with_all_pipes() == True:
        pygame.mixer.music.load("mixkit-bomb-explosion-in-battle-2800.wav")
        pygame.mixer.music.play(0)
        controle_jeu = controle_jeu + 1
        screen.blit(BIRD_HIT_BITMAP, (bird_x, bird_y))
    else:
        screen.blit(BIRD_BITMAP, (bird_x, bird_y))
    print_score()

pygame.mixer.music.load("Flappy Bird Theme Song.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if controle_jeu == 0:
                if event.key == pygame.K_SPACE:
                    controle_jeu = controle_jeu + 1
            if event.key == pygame.K_SPACE:
                if controle_jeu == 2:
                    controle_jeu = controle_jeu - 1
                    bird_x = 10
                    bird_y = (HAUTEUR_ECRAN/2) - (BIRD_BITMAP.get_height()/2)
                    ii = 1
                    score = 0
                    speed = 1
                    pygame.mixer.music.load("Flappy Bird Theme Song.mp3")
                    pygame.mixer.music.play(-1)
            if event.key == pygame.K_UP:
                bird_y = bird_y - 15
            elif event.key == pygame.K_DOWN:
                bird_y = bird_y + 15
        if event.type == pygame.QUIT:
            loop = False
        if controle_jeu == 0:
            screen.fill((0, 168, 243))
            print_flappy()
        if controle_jeu == 2:
            game_over()
    clock.tick(60)
    if controle_jeu == 1:
        game()
    pygame.display.flip()

pygame.quit()

