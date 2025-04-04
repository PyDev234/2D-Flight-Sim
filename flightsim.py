# 2D Flight Simulator
import numpy
import pygame
import time

# Window Attribute
size = WIDTH, HEIGHT = 780, 690

# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Initial Settings
plane_height = 96
plane_width = 196
bg = BLACK                              # Background color
fuel = 10_000                           # fuel capacity
x = 0                                   # At the left
y = 0                                   # At the bottom of screen / plane standing on ground
max_x = (WIDTH-plane_width - 20)        # max. movement on right side
max_y = (HEIGHT - plane_height)         # max. val of y after that the plane will just be at the top of window 
min_x = min_y = 0
thrust = 0.0
dmov = lambda y: y - ((1.991662e14) / ((y+6378137)**2))     # distance covered downwards due to gravity
umov = lambda y: y + 10
takeoff = False

# Constants for Calculating Force and Distance
G = 6.67e-11                        # Newton metre sq. per kg sq.
Me = 5.972e24                       # Mass of earth in kg
Re = 6.378137e6                     # Radius of Earth in metre
Gm = 3.983324e14                    # G * Me
Gmd2 = 1.991662e14                  # (G * Me) / 2 

# Initializing the pygame and setting drawing window
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg)

# Loading image assets
plane_gear_down = pygame.image.load(".\\2D_Flight_Simulator\\assets\\plane_gear_down.png")
plane_gear_up = pygame.image.load(".\\2D_Flight_Simulator\\assets\\plane_gear_up.png")
plane_crash = pygame.image.load(".\\2D_Flight_Simulator\\assets\\crash.png")
forest_img = pygame.image.load(".\\2D_Flight_Simulator\\assets\\pixel_parallax_0.png")
plane_gear_down = pygame.transform.scale(plane_gear_down, size=(plane_width, plane_height))
plane_gear_up = pygame.transform.scale(plane_gear_up, size=(plane_width, plane_height))
plane_crash = pygame.transform.scale(plane_crash, size=(plane_width, plane_height))
forest_img = pygame.transform.scale(forest_img, size = (WIDTH, 200))
# rect = plane_gear_down.get_rect()

# Loading music assets
plane_acceleration_sound = pygame.mixer.Sound("C:\\Users\\tfs\\VSCode Projects\\2D_Flight_Simulator\\assets\\plane-sound-from-distance-hq-247602.wav")
plane_deaccelaration_sound = pygame.mixer.Sound("C:\\Users\\tfs\\VSCode Projects\\2D_Flight_Simulator\\assets\\airplane-landing-6732.mp3")
myfont = pygame.font.SysFont('Comic Sans MS', 20)

# init Music
pygame.mixer.Channel(0).play(plane_acceleration_sound, -1)
pygame.mixer.Channel(0).pause()
pygame.mixer.Channel(1).play(plane_deaccelaration_sound, -1)
pygame.mixer.Channel(1).pause()

# Drawing initial situation
screen.blit(plane_gear_down, (x, y))
pygame.display.update()

running = True
while running:
    for event in pygame.event.get(): running = (event.type != pygame.QUIT)
    keys = pygame.key.get_pressed()
    prev = y
    if keys[pygame.K_UP]:                               # check if Arrow Up Key is pressed or not
        cur = y = umov(y)                               # move upward
        x += 1
        takeoff = True
        pygame.mixer.Channel(1).pause()
        pygame.mixer.Channel(0).unpause()
    else:
        pygame.mixer.Channel(0).pause()
        pygame.mixer.Channel(1).unpause()
    cur = y = dmov(y)                                   # Downward force due to gravity
    if y<plane_height and (not takeoff):                      # if at the ground then no need to apply anything
        cur = y = plane_height                          # reset its cordinates to the bottom of screen
        plane = plane_gear_down
        pygame.mixer.Channel(0).pause()
    elif y<plane_height and takeoff:
        cur = y = plane_height
        plane = plane_crash
    else: plane = plane_gear_up
    v = (0 if y>HEIGHT else (HEIGHT - y))
    k = x
    if k>max_x: k = max_x
    elif k<min_x: k = min_x
    x += 1.5*(keys[pygame.K_RIGHT]) - 0.2*(y != plane_height and x>0)
    cord_y = myfont.render(f'Y = {y: .4f} m', False, (0, 0, 255))
    cord_x = myfont.render(f'X = {x: .4f} Km', False, (0, 0, 255))
    screen.fill(BLACK)
    if prev>cur:
        wfall = myfont.render(f"Warning! Altitude Decreasing Rapidly", False, (255, 0, 0))
        screen.blit(wfall, (420, 60))
    
    # pygame.draw.rect(screen, GRAY, rect, 1)
    # screen.blit(rect, (x, v))
    screen.blit(forest_img, (0, HEIGHT - 200))
    screen.blit(plane, (k, v))
    screen.blit(cord_y, (580, 20))
    screen.blit(cord_x, (580, 40))
    pygame.display.update()
    time.sleep(0.05)
pygame.quit()