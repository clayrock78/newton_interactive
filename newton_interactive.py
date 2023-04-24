import pygame as pg
import numpy as np
import random
from root import Root

ITERATIONS = 30
WIDTH = 1920
HEIGHT = 1080
ASPRAT = WIDTH / HEIGHT
STARTING_SCALAR = 2

STARTING_BOUNDS = (STARTING_SCALAR * -ASPRAT, STARTING_SCALAR *
                   ASPRAT, STARTING_SCALAR * -1, STARTING_SCALAR * 1)
real_width = abs(STARTING_BOUNDS[1] - STARTING_BOUNDS[0])
real_offset = STARTING_BOUNDS[0]
imag_height = abs(STARTING_BOUNDS[3] - STARTING_BOUNDS[2])
imag_offset = STARTING_BOUNDS[2]


def distance_between(pos1, pos2):
    return ((pos1.real - pos2.real)**2 + (pos1.imag - pos2.imag)**2)**.5


def distance_between_tuples(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**.5


def complex_to_pix(root: Root):
    x = (root.real - real_offset) / real_width * WIDTH
    y = (root.imag - imag_offset) / imag_height * HEIGHT
    return x, y


def pix_to_complex(pos):
    x = pos[0] / WIDTH * real_width + real_offset
    y = pos[1] / HEIGHT * imag_height + imag_offset
    return x + 1j * y


def f(x):
    current = np.full(x.shape, np.complex128(1))
    for root in roots:
        current *= (x - root.complex)
    return current


def f_prime(x):
    # returns the derivative of f(x) where x is a polynomial
    current = np.full(x.shape, np.complex128(0))
    for root in roots:
        current += f(x) / (x - root.complex)
    return current


global fractal_surface
active = False


def render():
    global fractal_surface
    # display "rendering" to the user
    text = large_font.render(
        "Rendering, please wait...", True, (255, 255, 255))
    screen.blit(text, (WIDTH/2 - text.get_width() /
                2, HEIGHT/2 - text.get_height()/2))
    pg.display.flip()

    # form 2 2D arrays to store the real and imag
    res_width = int(WIDTH / res_scale)
    res_height = int(HEIGHT / res_scale)
    x = np.linspace(real_offset, real_offset + real_width, res_width)
    y = np.linspace(imag_offset, imag_offset + imag_height, res_height)
    reals, imags = np.meshgrid(x, y)
    c = np.complex128(reals + 1j*imags)
    colors = np.zeros((res_height, res_width, 3), dtype=np.uint8)
    calculated = np.zeros((res_height, res_width), dtype=bool)

    # calculate the fractal
    for i in range(ITERATIONS):
        not_calculated = np.logical_not(calculated)
        c[not_calculated] = c[not_calculated] - \
            f(c[not_calculated]) / f_prime(c[not_calculated])
        for root in roots:
            # if the root is close enough, set the color (only for non-calculated points)
            mask = (c.real - root.real)**2 + (c.imag - root.imag)**2 < .001
            mask = np.logical_and(mask, not_calculated)
            # make the color darker based on how many iterations it took to find the root
            if simple:
                colors[mask] = np.array(root.color)
            else:
                colors[mask] = (np.array(root.color) *
                                (1-(i / ITERATIONS)**.75))
            calculated[mask] = True

        if active:
            # draw the fractal to fractal_surface as pixelarray
            # swap axes
            tcolors = np.swapaxes(colors, 0, 1)
            fractal_surface = pg.surfarray.make_surface(tcolors)
            fractal_surface = pg.transform.scale(
                fractal_surface, (WIDTH, HEIGHT))
            screen.blit(fractal_surface, (0, 0))
            pg.display.flip()

    tcolors = np.swapaxes(colors, 0, 1)
    fractal_surface = pg.surfarray.make_surface(tcolors)
    fractal_surface = pg.transform.scale(fractal_surface, (WIDTH, HEIGHT))


# define a long list of colors
COLORS = [(random.randint(50, 255), random.randint(50, 255),
           random.randint(50, 255)) for _ in range(100)]
BLACK = (0, 0, 0)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("pygame template")
clock = pg.time.Clock()

roots = []
root_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
fractal_surface = pg.Surface((WIDTH, HEIGHT))

res_scale = 2

mouse = pg.mouse
simple = False

is_dragging_root = False
current_root = None
mouse_prev = (0, 0)

cur_col = 0

font = pg.font.SysFont("Arial", 20)
large_font = pg.font.SysFont("Arial", 28)

mode = "roots"

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if mouse.get_pressed()[2]:
                if mode == "roots":
                    c = pix_to_complex(mouse.get_pos())
                    real, imag = c.real, c.imag
                    roots.append(Root(real, imag, len(roots), COLORS[cur_col]))
                    cur_col += 1
                elif mode == "zooming":
                    mode = "zoom"

            if mouse.get_pressed()[0]:
                if mode == "zoom":
                    mouse_prev = mouse.get_pos()
                    mode = "zooming"
                elif mode == "zooming":
                    print('changing zoom')
                    # change the bounds of the image (while preserving aspect ratio)
                    mouse_cur = mouse.get_pos()
                    prev = pix_to_complex(mouse_prev)
                    cur = pix_to_complex(mouse_cur)
                    # calculate the new bounds (represented by the space that zoom_rect encloses)
                    real_offset = pix_to_complex(zoom_rect.topleft).real
                    imag_offset = pix_to_complex(zoom_rect.topleft).imag
                    real_width = abs(pix_to_complex(
                        zoom_rect.bottomright).real - pix_to_complex(zoom_rect.topleft).real)
                    imag_height = abs(pix_to_complex(
                        zoom_rect.bottomright).imag - pix_to_complex(zoom_rect.topleft).imag)

                    mode = "zoom"
                    render()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                imag_offset -= imag_height * .1
                render()
            if event.key == pg.K_DOWN:
                imag_offset += imag_height * .1
                render()
            if event.key == pg.K_LEFT:
                real_offset -= real_width * .1
                render()
            if event.key == pg.K_RIGHT:
                real_offset += real_width * .1
                render()
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                render()
            if event.key == pg.K_r:
                roots = []
                cur_col = 0
                # set bounds to default
                real_offset = STARTING_BOUNDS[0]
                imag_offset = STARTING_BOUNDS[1]
                real_width = abs(STARTING_BOUNDS[2] - STARTING_BOUNDS[0])
                imag_height = abs(STARTING_BOUNDS[3] - STARTING_BOUNDS[1])
                fractal_surface.fill((0, 0, 0, 0))
                COLORS = [(random.randint(50, 255), random.randint(
                    50, 255), random.randint(50, 255)) for _ in range(100)]

            if event.key == pg.K_s:
                temp = res_scale, ITERATIONS
                # prompt user for resolution scalar
                res_scale = float(input("Resolution scalar: "))
                # prompt user for iterations
                ITERATIONS = int(input("Iterations: "))
                # prompt user for filename
                filename = input("Filename: ")
                render()
                pg.image.save(fractal_surface, filename)
                res_scale, ITERATIONS = temp
                render()
            if event.key == pg.K_u:
                ITERATIONS += 1
                print(ITERATIONS)
            if event.key == pg.K_j:
                ITERATIONS -= 1
                print(ITERATIONS)
            if event.key == pg.K_l:
                simple = not simple
                print(simple)
            if event.key == pg.K_z:
                mode = "zoom"
            if event.key == pg.K_c:
                mode = "roots"
            if event.key == pg.K_i:
                res_scale += .2
            if event.key == pg.K_k:
                res_scale -= .2
            if event.key == pg.K_LCTRL:
                if mode != "controls":
                    mode = "controls"
                else:
                    mode = "roots"

    # 3 Draw/render
    screen.fill(BLACK)
    root_surface.fill((0, 0, 0, 0))

    for root in roots:
        root_pos = complex_to_pix(root)
        pg.draw.circle(root_surface, BLACK, root_pos, root.radius)
        pg.draw.circle(root_surface, root.color, root_pos, root.radius-10)

        if mouse.get_pressed()[0]:
            if current_root == root:
                c = pix_to_complex(mouse.get_pos())
                root.complex = c
                root.real = c.real
                root.imag = c.imag
            if distance_between_tuples(mouse.get_pos(), root_pos) <= root.radius:
                is_dragging_root = True
                current_root = root
        else:
            is_dragging_root = False
            current_root = None

    screen.blit(fractal_surface, (0, 0))
    screen.blit(root_surface, (0, 0))

    # if mode is zooming, draw a square to show the user what they are zooming to
    if mode == "zooming":
        # display text to the user
        text = large_font.render(
            "Zooming - Left click to zoom | Right click to cancel", True, (255, 255, 255))
        # display text in bottom right
        screen.blit(text, (WIDTH - text.get_width(),
                    HEIGHT - text.get_height()))

        mouse_cur = mouse.get_pos()
        left = 1 if mouse_cur[0] - mouse_prev[0] > 0 else -1
        top = 1 if mouse_cur[1] - mouse_prev[1] > 0 else -1
        width = max(abs(mouse_cur[0] - mouse_prev[0]),
                    abs(mouse_cur[1] - mouse_prev[1]))
        height = width * HEIGHT / WIDTH  # preserve aspect ratio
        zoom_rect = pg.Rect(
            mouse_prev[0], mouse_prev[1], width*left, height*top)
        pg.draw.rect(screen, (255, 255, 255), zoom_rect, 2, border_radius=5)

    # write current iterations to top left of screen
    text = large_font.render(
        f"Iterations: {ITERATIONS} Simple Mode:{simple} Resolution Scale:{res_scale} {'Active Mode On' if active else ''}", True, (255, 255, 255))
    screen.blit(text, (0, 0))

    if mode == "zoom":
        text = large_font.render("Zoom Mode", True, (255, 255, 255))
        screen.blit(text, (0, HEIGHT - text.get_height()))
    elif mode == "roots":
        text = large_font.render("Root Mode", True, (255, 255, 255))
        screen.blit(text, (0, HEIGHT - text.get_height()))
    elif mode == "controls":
        screen.fill((0, 0, 0))
        "Explain all the controls to the user"
        explanation = """
        Welcome to the Newton Fractal Generator!

        Zoom Mode (z)
            Allows you to zoom in on the fractal with left click

        Root Mode (c)
            Move roots with left click
            Place roots with right click

        Panning (arrow keys)
            Move the fractal around

        Increase/Decrease Iterations (u/j)
            Increase or decrease the number of iterations
            
        Increase/Decrease Resolution (i/k)
            Increase or decrease the resolution scale
            Using this with high values will allow you to generate low resolution images quickly
            Conversely, using this with low values will allow you to generate high resolution images slowly

        Toggle Simple Mode (l)
            Makes rendering slightly faster and changes style

        Save Image (s)
            Saves the current image to a file
            It will prompt you for options in the terminal

        Reset (r)
            Resets the fractal to its default state and changes root colors

        Quit (esc)
            Quits the program
        """
        for i, line in enumerate(explanation.split("\n")):
            text = large_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (WIDTH/2, 0)
            text_rect.y += i * text.get_height()
            screen.blit(text, text_rect)

    pg.display.flip()

pg.quit()
