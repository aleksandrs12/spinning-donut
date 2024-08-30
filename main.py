from math import sqrt, cos, sin, pi
import pygame
import numpy as np
#print('\033[H\033[J')
INNER_RADIUS = 20
OUTER_RADIUS = 40

x_rot = 0
y_rot = 0


sines_seen = {}
def calculate_sin(angle):
    if angle in sines_seen:
        return sines_seen[angle]
    sines_seen[angle] = sin(angle)
    return sines_seen[angle]

cosines_seen = {}
def calculate_cos(angle):
    if angle in cosines_seen:
        return cosines_seen[angle]
    cosines_seen[angle] = cos(angle)
    return cosines_seen[angle]

def calculate_ring(pos, r, x):
    if abs(x) > abs(r):
        return False, False
    
    y1 = round(sqrt(r**2 - x**2) + pos[1])
    y2 = round(-sqrt(r**2 - x**2) + pos[1])
    return (round(pos[0] + x), y1), (round(pos[1] + x), y2)

def calculate_ring2(pos, r, angle): # radians
    y = round(calculate_sin(angle) * r + pos[1])
    x = round(calculate_cos(angle) * r + pos[0])
    return [x, y]

def value_to_rgb(value):
    if not 0 <= value <= 1:
        raise ValueError("Input value must be between 0 and 1")
    
    # Use linear interpolation between blue, purple, and red
    if value <= 0.5:
        # Transition from blue to purple
        r = int(255 * (value * 2))  # Red increases
        g = 0  # Green stays at 0
        b = 255  # Blue stays at maximum
    else:
        # Transition from purple to red
        r = 255  # Red stays at maximum
        g = 0  # Green stays at 0
        b = int(255 * (1 - (value - 0.5) * 2))  # Blue decreases
    
    return r, g, b

def distance_to_color(d):
    max_r = (OUTER_RADIUS-INNER_RADIUS) // 2 * 3 + ((OUTER_RADIUS+INNER_RADIUS) / 2) / 3
    the_procentage = ((d / max_r) + 1) / 2 # 0 to 1 ratio of something to make a color of
    
    if the_procentage > 0.9:
        the_procentage = 0.9
    output = [round(255 * calculate_sin(the_procentage)), round(255 * calculate_cos(the_procentage)), round(255 * calculate_sin(the_procentage))]
    if output[2] < 210:
        output[2] += 40
    #output = list(value_to_rgb(the_procentage))
    return output

screen = pygame.display.set_mode((200, 200))
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
    x_rot += pi / 16
    y_rot += 0
    pixels_seen = {}
    x_rot_sin = calculate_sin(x_rot)
    x_rot_cos = calculate_cos(x_rot)
    for angle in np.arange(0, 2*pi, 2*pi / (360 / 1.5)):
        
        angle1_cos = calculate_cos(angle)
        inner_pos = calculate_ring2((100, 100), INNER_RADIUS, angle)
        outer_pos = calculate_ring2((100, 100), OUTER_RADIUS, angle)
        
        
        #x rotation logic
        inner_pos[0] = round((inner_pos[0] - 100) * x_rot_cos) + 100
        outer_pos[0] = round((outer_pos[0] - 100) * x_rot_cos) + 100
        
        #inner_pos[1] = round((inner_pos[1] - 200) * calculate_cos(y_rot)) + 200
        #outer_pos[1] = round((outer_pos[1] - 200) * calculate_cos(y_rot)) + 200
        # the code is a bit ugly but basically i had to subtract 200 to isolate the actual x
        
        for angle2 in np.arange(0, pi*2, 2*pi / (360 / 1.5)):
            ring_pos_adj = calculate_ring2((0, 0), (OUTER_RADIUS-INNER_RADIUS) // 2, angle2)
            x = (OUTER_RADIUS-INNER_RADIUS) / 2 * calculate_cos(angle2) + (inner_pos[0] + outer_pos[0]) / 2
            y = (OUTER_RADIUS-INNER_RADIUS) / 2 * calculate_sin(angle2) + (inner_pos[1] + outer_pos[1]) / 2
            distance = ring_pos_adj[1] * 4 + x_rot_sin * angle1_cos * ((OUTER_RADIUS+INNER_RADIUS) / 2) + ((OUTER_RADIUS+INNER_RADIUS) / 2)
            #print(distance, OUTER_RADIUS-INNER_RADIUS // 2)
            color = distance_to_color(distance)
            #print(color)
            
            # prevent parts of the circle that are further away from overwriting pixels that are closer
            if not (round(x), round(y)) in pixels_seen:
                pixels_seen[(round(x), round(y))] = distance
                screen.set_at((round(x), round(y)), color)
            elif pixels_seen[(round(x), round(y))] > distance:
                pixels_seen[(round(x), round(y))] = distance
                screen.set_at((round(x), round(y)), color)
                
            #screen.set_at((round(x), round(y)), color)
            
        #screen.set_at(inner_pos, (255, 100, 0))
        #screen.set_at(outer_pos, (255, 0, 0))
        
            
        
            
            
    pygame.display.update()
pygame.quit()

