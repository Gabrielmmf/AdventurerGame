from math import floor
from math import ceil
import pygame
from sys import exit
from pygame.locals import *
from settings import *

size = scr_w, scr_h = 1280, 720


def import_and_resize(location, scale):
    surface = pygame.image.load(location).convert_alpha()
    surface = pygame.transform.scale(
        surface, (surface.get_size()[0]*scale, surface.get_size()[1]*scale))
    return surface


def import_and_extend_to_display(location):
    surface = pygame.image.load(location).convert_alpha()
    scale = ceil(scr_w/surface.get_size()[0])
    surface = pygame.transform.scale(
        surface, (surface.get_size()[0]*scale, surface.get_size()[1]*scale))
    return surface


def import_and_fill_display(location):
    surface = pygame.image.load(location).convert_alpha()
    scale = ceil(max(scr_w/surface.get_size()[0], scr_h/surface.get_size()[1]))
    surface = pygame.transform.scale(
        surface, (surface.get_size()[0]*scale, surface.get_size()[1]*scale))
    return surface


def fit_to_rectangle(bounding_rec, margins):
    return bounding_rec.left+margins[0], bounding_rec.top+margins[1]


def find_margins(bound, unbound):
    return (unbound.left-bound.left, unbound.top-bound.top, unbound.right-bound.right, unbound.bottom - bound.bottom)


def add_margins(rectangle, margins):
    left = rectangle.left+margins[0]
    top = rectangle.top+margins[1]
    width = rectangle.right + margins[2] - left
    height = rectangle.bottom+margins[3] - top
    new_rectangle = pygame.Rect(left, top, width, height)
    return new_rectangle


def invert_margins(margins):
    new_margins = (-margins[2], margins[1], -margins[0], margins[3])
    return new_margins


def import_action(action, n_sprites):

    if n_sprites == 4:
        return(import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-00.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-01.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-02.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-03.png', 4))
    if n_sprites == 5:
        return(import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-00.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-01.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-02.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-03.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-04.png', 4))
    if n_sprites == 6:
        return(import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-00.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-01.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-02.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-03.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-04.png', 4), import_and_resize(
            'graphics/Adventurer/Individual Sprites/adventurer-'+action+'-05.png', 4))


pygame.init()


# Setando a tela, fonte, nome da janela e escala de aumento de acordo com a resolução
screen = pygame.display.set_mode(size)
text_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
pygame.display.set_caption("Adventurer")
game_scale = ceil(scr_w/320)

adventurer_idle2 = import_action('idle-2', 4)
adventurer_run = import_action('run', 6)
adventurer_jump = import_action('jump', 4)
adventurer_fall = import_action('fall', 4)
adventurer_attack1 = import_action('attack1', 5)
adventurer_attack2 = import_action('attack2', 6)
adventurer_attack3 = import_action('attack3', 6)
adventurer_air_attack1 = import_action('air-attack1', 4)

print(adventurer_idle2)

# Inicia relógio para controlar framerate
clock = pygame.time.Clock()

# Preenche a tela toda com o céu e estica e posiciona o chão
sky = import_and_fill_display('graphics/Sky.png')
ground = import_and_extend_to_display('graphics/ground.png')
ground_y = ceil(55*scr_h/72)
score = 0
score_surface = text_font.render('Score:   '+str(score), False, 'Red')
score_rect = score_surface.get_rect(center=(scr_w/2, 50))

# Construindo hitboxes
adventurer = import_and_resize(
    'graphics/Adventurer/Individual Sprites/adventurer-rectangle.png', game_scale)

adventurer_x = scr_w/2
adventurer_unbound_rec = adventurer.get_rect(
    midbottom=(adventurer_x, ground_y))
adventurer_rec = adventurer.get_bounding_rect()
adventurer_rec.move_ip(adventurer_unbound_rec.topleft)
# margins left, top, rigth, bottom
margins_adventurer = find_margins(adventurer_rec, adventurer_unbound_rec)

enemy_surface = import_and_resize('graphics/Enemies/1.png', 2)
enemy_x = scr_w - enemy_surface.get_size()[0]
enemy_rec = enemy_surface.get_rect(midbottom=(enemy_x, ground_y))


adventurer_state = 0
adventurer_action = adventurer_idle2

player_speed = 0
player_gravity = 0
falling = False
last_x, last_y, last_direction = adventurer_rec.centerx, adventurer_rec.centery, 'right'
ininterrupt = False
endofininterrupt = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE and adventurer_rec.bottom >= ground_y and not (ininterrupt)):
                player_gravity = -25
                adventurer_action = adventurer_jump
                falling = True
            if (event.key == pygame.K_s and adventurer_rec.bottom < ground_y and not (ininterrupt)):
                player_gravity += 5
            if (event.key == pygame.K_d and not (ininterrupt)):
                print('RIGHT')
                player_speed += 10
                if not(ininterrupt):
                    adventurer_action = adventurer_run
            if (event.key == pygame.K_a and not (ininterrupt)):
                print('LEFT')
                player_speed -= 10
                if not(ininterrupt):
                    adventurer_action = adventurer_run
            if (event.key == pygame.K_j and not (ininterrupt)):
                print('ATTACK 1')
                adventurer_action = adventurer_attack1
                player_speed = 0
                ininterrupt = True

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_d):
                print('K UP RIGHT')
                player_speed = 0
                if(pygame.key.get_pressed()[K_a]):
                    player_speed = -10
                
            if (event.key == pygame.K_a):
                player_speed = 0
                if(pygame.key.get_pressed()[K_d]):
                    player_speed = 10
                

    if(adventurer_state < len(adventurer_action)-1):
        adventurer_state += 1/10
    else:
        ininterrupt = False
        endofininterrupt = True
        adventurer_state = 0

    adventurer = adventurer_action[floor(adventurer_state)]
    if (last_direction == 'left'):
        adventurer = pygame.transform.flip(adventurer, True, False)

    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, ground_y))
    screen.blit(enemy_surface, enemy_rec)
    screen.blit(score_surface, score_rect)

    enemy_rec.x -= 6
    if (enemy_rec.right <= 0):
        enemy_rec.left = scr_w
    adventurer_rec.x += player_speed

    attack_hitbox = add_margins(adventurer_rec, margins_adventurer)
    pygame.draw.rect(screen, (0, 0, 0, 0.3), attack_hitbox)
    pygame.draw.rect(screen, (245, 0, 0, 0.3), adventurer_rec)


    if(adventurer_rec.bottom < ground_y):
        player_gravity += 1
    adventurer_rec.centery += player_gravity

    if adventurer_rec.bottom > ground_y:
        adventurer_rec.bottom = ground_y
        falling = False

    current_x, current_y = adventurer_rec.centerx, adventurer_rec.centery

    if not(ininterrupt):
        if(current_x == last_x and current_y == last_y):
            adventurer_action = adventurer_idle2
        if(current_y > last_y):
            adventurer_action = adventurer_fall
        if(current_x == last_x):
            current_direction = last_direction
        if(current_x > last_x):
            current_direction = 'right'
            if not(falling and not(ininterrupt)):
                adventurer_action = adventurer_run
                print('right')
        if(current_x < last_x):
            current_direction = 'left'
            print('left')
            if not(falling and not(ininterrupt)):
                adventurer_action = adventurer_run

    last_x, last_y, last_direction = current_x, current_y, current_direction
    screen.blit(adventurer, fit_to_rectangle(
        adventurer_rec, margins_adventurer))

    pygame.display.update()
    clock.tick(60)
