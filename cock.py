import numpy as np
import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()

z = np.array([
    [(255, 170, 0), (255, 170, 0)],
    [(255, 170, 0), (0, 127, 255)],
    [(255, 170, 0), (255, 170, 0)],
    [(255, 170, 0), (255, 170, 0)],
    ])
print(z.shape)
print(type(z))
print(z[0][0])
# Either use `make_surface` to create a new surface ...
surface = pg.surfarray.make_surface(z)
# or create the surface first and then use `blit_array` to fill it.
surface2 = pg.Surface(z.shape[:2])
pg.surfarray.blit_array(surface2, z)
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    screen.fill((30, 30, 30))
    screen.blit(surface, (50, 50))
    screen.blit(surface2, (50, 100))

    pg.display.flip()
    clock.tick(30)