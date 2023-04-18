import pygame as pg
import numpy as np
import random
from root import Root

real_width = 5
real_offset = 0
imag_height = 5
imag_offset = 0

ITERATIONS = 10
WIDTH = 300
HEIGHT = 300

def distance_between(pos1, pos2):
    return ((pos1.real - pos2.real)**2 + (pos1.imag - pos2.imag)**2)**.5

def distance_between_tuples(pos1, pos2):
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
    current = np.full(x.shape, np.complex64(1))
    for root in roots:
        current *= (x - root.complex)
    return current

def f_prime(x):
    step = .000001
    return (f(x + step) - f(x)) / step

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, PURPLE, YELLOW]

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("pygame template")
clock = pg.time.Clock()


roots = []

root_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
fractal_surface = pg.Surface((WIDTH, HEIGHT))

mouse = pg.mouse

is_dragging_root = False
current_root = None
mouse_prev = (0,0)

cur_col = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if mouse.get_pressed()[2]:
                real, imag = pix_to_complex(mouse.get_pos())
                roots.append(Root(real, imag, COLORS[cur_col] ))
                cur_col += 1
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                # form 2 2D arrays to store the real and imag
                x = np.linspace(real_offset, real_width, WIDTH)
                y = np.linspace(imag_offset, imag_height, HEIGHT)
                reals, imags = np.meshgrid(x,y)
                c = np.complex64(pix_to_complex((reals,imags)))
                #print(c.shape)
                #for _ in range(ITERATIONS):
                #    c = c - f(c) / f_prime(c)
                
                color_shape = [300,300,3]
                nearest_color = np.empty((300,300,3))
                nearest_distance = np.full((300,300), np.inf)
                print(c.shape)
                for root in roots:
                    distance = distance_between(c[0], np.full(c[0].shape,root.complex))
                    mask = np.greater(nearest_distance, distance)
                    nearest_distance = np.where(mask, distance, nearest_distance)
                    mask.shape = (300,300,1)
                    nearest_color = np.where(mask, np.full((300,300,3),np.array(root.color)), nearest_color)
                

                # for indx, x in enumerate(c):
                #     for indy, y in enumerate(x):
                #         for ind, comp in enumerate(y):
                #             color = np.array(list(min(roots, key=lambda x:distance_between(x.complex, comp)).color))
                #             colors[indy][indx] = color
                #print(colors)
                fractal_surface = pg.surfarray.make_surface(nearest_color)

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
            if distance_between_tuples(mouse.get_pos(), root_pos) <= root.radius:                
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