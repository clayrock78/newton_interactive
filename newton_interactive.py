import pygame as pg
import random
from root import Root

real_width = 2
real_offset = 0
imag_height = 2
imag_offset = 0

ITERATIONS = 5
WIDTH = 1920
HEIGHT = 1080
FPS = 60

def distance_between(pos1, pos2):
    if type(pos1) == complex: pos1 = (pos1.real, pos1.imag)
    if type(pos2) == complex: pos2 = (pos2.real, pos2.imag)
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**.5

def complex_to_pix(root:Root):
    x = root.real / real_width * WIDTH
    y = root.imag / imag_height * HEIGHT
    return x,y

def pix_to_complex(pos):
    x = pos[0] / WIDTH * real_width 
    y = pos[1] / HEIGHT * imag_height
    return x,y

def f(x):
    current = 1
    for root in roots:
        current *= (x - root.complex)
    return complex(current)

def f_prime(x):
    step = .000001
    return (f(x + step) - f(x)) / step

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [WHITE, BLACK, RED, GREEN, BLUE]

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("pygame template")
clock = pg.time.Clock()


roots = [Root(1,1,RED), Root(1,2,BLUE), Root(0,1,GREEN)]

root_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
fractal_surface = pg.Surface((WIDTH, HEIGHT))

mouse = pg.mouse

is_dragging_root = False
current_root = None
mouse_prev = (0,0)

running = True
while running:

    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                fractal_surface_pa = pg.PixelArray(fractal_surface)
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        c = complex(*pix_to_complex((x,y)))
                        for _ in range(ITERATIONS):
                            c = c - f(c)/f_prime(c)
                        color = min(roots, key=lambda x:distance_between(x.complex, c)).color
                        fractal_surface_pa[x,y] = color
                fractal_surface_pa.close()

    #3 Draw/render
    screen.fill(BLACK)
    root_surface.fill((0,0,0,0))

    for root in roots:
        root_pos = complex_to_pix(root)
        pg.draw.circle(root_surface, BLACK, root_pos, root.radius)
        pg.draw.circle(root_surface, root.color, root_pos, root.radius-10)

        if mouse.get_pressed()[0]:
            if current_root == root:
                c = complex(*pix_to_complex(mouse.get_pos()))
                root.complex = c
                root.real = c.real
                root.imag = c.imag
            if distance_between(mouse.get_pos(), root_pos) <= root.radius:                
                is_dragging_root = True
                current_root = root   
        else:
            is_dragging_root = False
            current_root = None

    mouse_prev = mouse.get_pos()

    screen.blit(fractal_surface,(0,0))
    screen.blit(root_surface,(0,0))
    pg.display.flip()       

pg.quit()