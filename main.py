from math import sqrt, cos, sin, pi
import pygame
import numpy as np
#print('\033[H\033[J')
INNER_RADIUS = 60
OUTER_RADIUS = 120

x_rot = 0
y_rot = 0
def calculate_ring(pos, r, x):
    if abs(x) > abs(r):
        return False, False
    
    y1 = round(sqrt(r**2 - x**2) + pos[1])
    y2 = round(-sqrt(r**2 - x**2) + pos[1])
    return (round(pos[0] + x), y1), (round(pos[1] + x), y2)

def calculate_ring2(pos, r, angle): # radians
    y = round(sin(angle) * r + pos[1])
    x = round(cos(angle) * r + pos[0])
    return [x, y]

def distance_to_color(d):
    max_r = (OUTER_RADIUS-INNER_RADIUS) // 2
    the_procentage = ((d / max_r) + 1) / 2 # 0 to 1 ratio of something to make a color of
    shifted_procentage = (the_procentage + 0.3) % 1 # shifts the procentage by 0.2
    shifted_procentage2 = (the_procentage + 0.6) % 1 # shifts the procentage by 0.4
    return (round(255 * the_procentage), round(255 * shifted_procentage), round(255 * shifted_procentage2))

screen = pygame.display.set_mode((400, 400))
run = True
while run:
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 400))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    '''
    for x in np.arange(-200.0, 200.0, 0.1):
        p1, p2 = calculate_ring((200, 200), INNER_RADIUS, x)
        if p1:
            screen.set_at(p1, (255, 0, 0))
            screen.set_at(p2, (255, 0, 0))
            
    for x in np.arange(-200.0, 200.0, 0.1):
        p1, p2 = calculate_ring((200, 200), OUTER_RADIUS, x)
        if p1:
            screen.set_at(p1, (255, 0, 0))
            screen.set_at(p2, (255, 0, 0))
    '''
    x_rot += pi / 8
    pixels_seen = {}
    for angle in np.arange(0, 2*pi, 2*pi / (360 * 4)):
        inner_pos = calculate_ring2((200, 200), INNER_RADIUS, angle)
        outer_pos = calculate_ring2((200, 200), OUTER_RADIUS, angle)
        
        #x rotation logic
        inner_pos[0] = round((inner_pos[0] - 200) * cos(x_rot)) + 200
        outer_pos[0] = round((outer_pos[0] - 200) * cos(x_rot)) + 200
        # the code is a bit ugly but basically i had to subtract 200 to isolate the actual x
        
        for angle2 in np.arange(0, 2*pi, 2*pi / (360 * 1)):
            ring_pos_adj = calculate_ring2((0, 0), (OUTER_RADIUS-INNER_RADIUS) // 2, angle2)
            x = ring_pos_adj[0] * cos(angle) + (inner_pos[0] + outer_pos[0]) / 2
            y = ring_pos_adj[0] * sin(angle) + (inner_pos[1] + outer_pos[1]) / 2
            distance = ring_pos_adj[1]
            #print(distance, OUTER_RADIUS-INNER_RADIUS // 2)
            color = distance_to_color(distance)
            #print(color)
            
            # prevent parts of the circle that are further away from overwriting pixels from the closer ones
            if not (round(x), round(y)) in pixels_seen:
                pixels_seen[(round(x), round(y))] = distance
                screen.set_at((round(x), round(y)), color)
            elif pixels_seen[(round(x), round(y))] > distance:
                pixels_seen[(round(x), round(y))] = distance
                screen.set_at((round(x), round(y)), color)
        
            
        #screen.set_at(inner_pos, (255, 0, 0))
        #screen.set_at(outer_pos, (255, 0, 0))
            
            
    pygame.display.update()
pygame.quit()

