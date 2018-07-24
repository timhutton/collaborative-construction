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

class WallBuilder:
    def __init__(self):
        self.area_x = 16
        self.area_y = 16
        self.wallV = 6
        self.scale = 20
        self.num_players = 3 # wasdq, ijklu, <l><r><u><d>'/'
        self.screen_x = self.area_x*self.scale
        self.screen_y = self.area_y*self.scale
        # area and wall starts out empty
        self.area = [[0 for y in range(self.area_x)] for x in range(self.area_y)]
        # add some 'source' squares at the bottom
        self.area[5][self.area_y-1] = 1
        self.area[9][self.area_y-1] = 2
        self.area[13][self.area_y-1] = 3
        self.area[7][self.area_y-1] = 4
        # initialize the players
        self.players = [ [[4+i*3,self.wallV*2],(255,255,255),1] for i in range(self.num_players)]

        self.brick_colors = [ (0,0,0), (0,0,200), (200,200,200), (128,255,255), (255,128,0) ]
        self.background_color = (0,0,0)

    def placeInWall(self,x,b):
        for y in range(self.wallV-1,-1,-1):
            if self.area[x][y]==0:
                self.area[x][y]=b
                break

    def playerMove(self,i,dxdy):
        dx,dy = dxdy
        newx = max( min( self.players[i][0][0]+dx, self.area_x-1 ), 0 )
        newy = max( min( self.players[i][0][1]+dy, self.area_y-2 ), self.wallV )
        if all( not self.players[j][0][0] == newx or not self.players[j][0][1] == newy for j in range(self.num_players)):
            self.players[i][0][0] = newx
            self.players[i][0][1] = newy

    def playerUse(self,i):
        if self.players[i][2]==0:
            # player not holding anything - can they pick up a block?
            if self.area[self.players[i][0][0]][self.players[i][0][1]] > 0: # they are standing on a block
                self.players[i][2] = self.area[self.players[i][0][0]][self.players[i][0][1]] # pick up the block
                self.area[self.players[i][0][0]][self.players[i][0][1]] = 0 # ground is now empty
            elif self.players[i][0][1]==self.area_y-2 and self.area[self.players[i][0][0]][self.area_y-1] > 0: # they are next to a source
                self.players[i][2] = self.area[self.players[i][0][0]][self.area_y-1] # pick up a block from the source
        else:
            # player holding a block - can they place it?
            if self.players[i][0][1]==self.wallV: # standing at wall
                if self.area[self.players[i][0][0]][0]==0: # wall has an empty slot here
                    self.placeInWall( self.players[i][0][0], self.players[i][2] ) # place the brick in the wall
                    self.players[i][2] = 0 # player is now holding nothing
            elif self.area[self.players[i][0][0]][self.players[i][0][1]]==0: # standing somewhere else on empty ground
                self.area[self.players[i][0][0]][self.players[i][0][1]] = self.players[i][2] # place the block on the ground
                self.players[i][2] = 0 # player is now holding nothing
                
    def render(self, DISPLAYSURF):
        # update the display
        pygame.draw.rect(DISPLAYSURF, self.background_color, (0,0,self.screen_x,self.screen_y))
        # draw the wall
        for x in range(self.area_x):
            for y in range(self.area_y):
                pygame.draw.rect(DISPLAYSURF, self.brick_colors[self.area[x][y]], (x*self.scale,y*self.scale,self.scale,self.scale))
                if y < self.wallV:
                    pygame.draw.rect(DISPLAYSURF, (255,255,255), (x*self.scale,y*self.scale,self.scale,self.scale), 1)
        # draw the players
        for i in range(self.num_players):
            x,y = self.players[i][0]
            color = self.players[i][1]
            holding = self.players[i][2]
            pygame.draw.circle(DISPLAYSURF, color, (x*self.scale+self.scale//2,y*self.scale+self.scale//2), self.scale//2)
            pygame.draw.circle(DISPLAYSURF, self.brick_colors[holding], (x*self.scale+self.scale//2,y*self.scale+self.scale//2), self.scale//4)

env = WallBuilder()
DISPLAYSURF = pygame.display.set_mode((env.screen_x,env.screen_y))
pygame.display.set_caption('WallBuilder')

while True:

    # get all the user events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key==K_d:
                env.playerMove(0,(1,0))
            elif event.key==K_a:
                env.playerMove(0,(-1,0))
            elif event.key==K_s:
                env.playerMove(0,(0,1))
            elif event.key==K_w:
                env.playerMove(0,(0,-1))
            elif event.key==K_q:
                env.playerUse(0)
            elif event.key==K_l:
                env.playerMove(1,(1,0))
            elif event.key==K_j:
                env.playerMove(1,(-1,0))
            elif event.key==K_k:
                env.playerMove(1,(0,1))
            elif event.key==K_i:
                env.playerMove(1,(0,-1))
            elif event.key==K_u:
                env.playerUse(1)
            elif event.key==K_RIGHT:
                env.playerMove(2,(1,0))
            elif event.key==K_LEFT:
                env.playerMove(2,(-1,0))
            elif event.key==K_DOWN:
                env.playerMove(2,(0,1))
            elif event.key==K_UP:
                env.playerMove(2,(0,-1))
            elif event.key==K_SLASH:
                env.playerUse(2)
    
    # check for new combos
    
    pygame.display.update()
    env.render(DISPLAYSURF)
