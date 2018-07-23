try:
    import pygame
    from pygame.locals import *
except ImportError:
    print("\nThis script uses pygame, which you don't seem to have installed. Try running this first:\n")
    print("python -m pip install -U pygame --user\n")
    exit(1)

import random,sys

#initialise the pygame module
pygame.init()

print(' -------------- WallBuilder -------------')
print(' Player 1: w-a-s-d to move, q to pick up / place')
print(' Player 2: i-j-k-l to move, u to pick up / place')
print(' Player 3: Left-Right-Up-Down to move, "/" to pick up / place')
print(' Esc to quit')
print(' ----------------------------------------')

area_x = 16
area_y = 16
wallV = 6
scale = 20
num_players = 3 # wasdq, ijklu, <l><r><u><d>'/'

screen_x = area_x*scale
screen_y = area_y*scale
DISPLAYSURF = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption('WallBuilder')

# area and wall starts out empty
area = [[0 for y in range(area_x)] for x in range(area_y)]
# add some 'source' squares at the bottom
area[5][area_y-1] = 1
area[9][area_y-1] = 2
area[13][area_y-1] = 3
# initialize the players
players = [ [[4+i*3,wallV*2],(255,255,255),1] for i in range(num_players)]

brick_colors = [ (0,0,0),(0,255,0), (255,0,0), (128,0,128), (255,128,0) ]
background_color = (0,0,0)

def placeInWall(x,b):
    for y in range(wallV-1,-1,-1):
        if area[x][y]==0:
            area[x][y]=b
            break

def playerMove(i,dxdy):
    dx,dy = dxdy
    newx = max( min( players[i][0][0]+dx, area_x-1 ), 0 )
    newy = max( min( players[i][0][1]+dy, area_y-2 ), wallV )
    if all( not players[j][0][0] == newx or not players[j][0][1] == newy for j in range(num_players)):
        players[i][0][0] = newx
        players[i][0][1] = newy

def playerUse(i):
    if players[i][2]==0:
        # player not holding anything - can they pick up a block?
        if area[players[i][0][0]][players[i][0][1]] > 0: # they are standing on a block
            players[i][2] = area[players[i][0][0]][players[i][0][1]] # pick up the block
            area[players[i][0][0]][players[i][0][1]] = 0 # ground is now empty
        elif players[i][0][1]==area_y-2 and area[players[i][0][0]][area_y-1] > 0: # they are next to a source
            players[i][2] = area[players[i][0][0]][area_y-1] # pick up a block from the source
    else:
        # player holding a block - can they place it?
        if players[i][0][1]==wallV: # standing at wall
            if area[players[i][0][0]][0]==0: # wall has an empty slot here
                placeInWall( players[i][0][0], players[i][2] ) # place the brick in the wall
                players[i][2] = 0 # player is now holding nothing
        elif area[players[i][0][0]][players[i][0][1]]==0: # standing somewhere else on empty ground
            area[players[i][0][0]][players[i][0][1]] = players[i][2] # place the block on the ground
            players[i][2] = 0 # player is now holding nothing

while True:

    # get all the user events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key==K_d:
                playerMove(0,(1,0))
            elif event.key==K_a:
                playerMove(0,(-1,0))
            elif event.key==K_s:
                playerMove(0,(0,1))
            elif event.key==K_w:
                playerMove(0,(0,-1))
            elif event.key==K_q:
                playerUse(0)
            elif event.key==K_l:
                playerMove(1,(1,0))
            elif event.key==K_j:
                playerMove(1,(-1,0))
            elif event.key==K_k:
                playerMove(1,(0,1))
            elif event.key==K_i:
                playerMove(1,(0,-1))
            elif event.key==K_u:
                playerUse(1)
            elif event.key==K_RIGHT:
                playerMove(2,(1,0))
            elif event.key==K_LEFT:
                playerMove(2,(-1,0))
            elif event.key==K_DOWN:
                playerMove(2,(0,1))
            elif event.key==K_UP:
                playerMove(2,(0,-1))
            elif event.key==K_SLASH:
                playerUse(2)
                    
    # update the display
    pygame.display.update()
    pygame.draw.rect(DISPLAYSURF, background_color, (0,0,screen_x,screen_y))
    # draw the wall
    for x in range(area_x):
        for y in range(area_y):
            pygame.draw.rect(DISPLAYSURF, brick_colors[area[x][y]], (x*scale,y*scale,scale,scale))
            if y < wallV:
                pygame.draw.rect(DISPLAYSURF, (255,255,255), (x*scale,y*scale,scale,scale), 1)
    # draw the players
    for i in range(num_players):
        x,y = players[i][0]
        color = players[i][1]
        holding = players[i][2]
        pygame.draw.circle(DISPLAYSURF, color, (x*scale+scale//2,y*scale+scale//2), scale//2)
        pygame.draw.circle(DISPLAYSURF, brick_colors[holding], (x*scale+scale//2,y*scale+scale//2), scale//4)
