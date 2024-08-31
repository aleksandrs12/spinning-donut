from math import sqrt, cos, sin, pi, floor
import pygame
import numpy as np
#print('\033[H\033[J')
INNER_RADIUS = 10
OUTER_RADIUS = 30

x_rot = 0
y_rot = 0

donut_centre = [30, 30]

buffer = []
for n in range(OUTER_RADIUS*2+1):
    buffer.append([' '] * (OUTER_RADIUS*2+1))

def printout(buffer):
    print('\033[H\033[J')
    for line in buffer:
        for char in line:
            print(char, end='')
        print()

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

def calculate_ring2(pos, r, angle): # radians
    y = round(calculate_sin(angle) * r + pos[1])
    x = round(calculate_cos(angle) * r + pos[0])
    return [x, y]


def distance_to_char(d):
    max_r = (OUTER_RADIUS-INNER_RADIUS) // 2 * 3 + ((OUTER_RADIUS+INNER_RADIUS) / 2) * 3
    the_procentage = ((d / max_r) + 1) / 2 # 0 to 1 ratio of something to make a char of
    rank = ['$', '$', '$', '$', '$', 'E', 'F', 'L', 'l', 'v', '!', ';', ',', '.', '.', '.']
    the_procentage *= len(rank) - 1
    return rank[floor(the_procentage)]

run = True
while run:
    buffer = []
    for n in range(OUTER_RADIUS*2+1):
        buffer.append([' '] * (OUTER_RADIUS*2+1))
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
        inner_pos = calculate_ring2(donut_centre, INNER_RADIUS, angle)
        outer_pos = calculate_ring2(donut_centre, OUTER_RADIUS, angle)
        
        
        #x rotation logic
        inner_pos[0] = round((inner_pos[0] - donut_centre[0]) * x_rot_cos) + donut_centre[0]
        outer_pos[0] = round((outer_pos[0] - donut_centre[0]) * x_rot_cos) + donut_centre[0]
        
        #inner_pos[1] = round((inner_pos[1] - 200) * calculate_cos(y_rot)) + 200
        #outer_pos[1] = round((outer_pos[1] - 200) * calculate_cos(y_rot)) + 200
        # the code is a bit ugly but basically i had to subtract 200 to isolate the actual x
        
        for angle2 in np.arange(0, pi*2, 2*pi / (360 / 1.5)):
            ring_pos_adj = calculate_ring2((0, 0), (OUTER_RADIUS-INNER_RADIUS) // 2, angle2)
            x = (OUTER_RADIUS-INNER_RADIUS) / 2 * calculate_cos(angle2) + (inner_pos[0] + outer_pos[0]) / 2
            y = (OUTER_RADIUS-INNER_RADIUS) / 2 * calculate_sin(angle2) + (inner_pos[1] + outer_pos[1]) / 2
            distance = ring_pos_adj[1] * 4 + x_rot_sin * angle1_cos * ((OUTER_RADIUS+INNER_RADIUS) / 2) + ((OUTER_RADIUS+INNER_RADIUS) / 2)
            #print(distance, OUTER_RADIUS-INNER_RADIUS // 2)
            #print(color)
            
            # prevent parts of the circle that are further away from overwriting pixels that are closer
            if not (round(x), round(y)) in pixels_seen:
                pixels_seen[(round(x), round(y))] = distance
                buffer[round(y)][round(x)] = distance_to_char(distance)
            elif pixels_seen[(round(x), round(y))] > distance:
                pixels_seen[(round(x), round(y))] = distance
                buffer[round(y)][round(x)] = distance_to_char(distance)
                
            #screen.set_at((round(x), round(y)), color)
            
        #screen.set_at(inner_pos, (255, 100, 0))
        #screen.set_at(outer_pos, (255, 0, 0))
        
            
        
    #print(buffer)
    printout(buffer)