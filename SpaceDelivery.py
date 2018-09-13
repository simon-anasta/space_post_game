#!/usr/bin/python

#------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------

# External modules
import pygame
from pygame.locals import KMOD_ALT, K_F4, QUIT, KEYDOWN, KEYUP, Rect, K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE
from math import floor,ceil,cos,sin,atan2,pi
from random import random, randint

# Internal modules
import config
from MenuMaker import MenuInstance
from LevelsLoader import getLevel
import DataHands

#------------------------------------------------------------
# MODEL
#------------------------------------------------------------

#------------------------------------------------------------
# Map Board
class MapBoard:
    """Size = [xmin xmax, ymin, ymax]"""
    def __init__(self,xmax,ymax,text,text_loc,xmin=0.0,ymin=0.0):
        # store parameters
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.text = text
        self.text_loc = text_loc
        
    def makeDrawer(self):
        return(MapBoardDrawer(self))

#------------------------------------------------------------
# Post Ship
class PostShip:
    """Post delivery ship.
    Location is (x,y) tuple.
    Board is map board ship belongs on."""
    def __init__(self,
                 location,
                 board,
                 velocity = (0,0),
                 acceleration = (0,0),
                 size = config.postShipSize):
        # store parameters
        self.x_loc, self.y_loc = location
        self.x_vel, self.y_vel = velocity
        self.x_acc, self.y_acc = acceleration
        self.size = size
        self.board = board
        # engine indicators
        if easyControls:
            self.moveUp = False
            self.moveDown = False
            self.moveLeft = False
            self.moveRight = False
        else:
            self.move = False
            self.radians = 0.0
        # indicator for waiting for level start
        self.waiting = True
        
    def timeStep(self,dt):
        # update acceleration
        self.x_acc, self.y_acc = self.updateAcceleration()
        # update velocity
        self.x_vel += self.x_acc*dt
        self.y_vel += self.y_acc*dt
        # update location
        self.x_loc += self.x_vel*dt
        self.y_loc += self.y_vel*dt
        
    def updateAcceleration(self):
        # EASY controls
        if easyControls:
            # vertical
            if self.moveUp & (not self.moveDown):
                y_acc = -config.accChange
            elif self.moveDown & (not self.moveUp):
                y_acc = +config.accChange
            else:
                y_acc = 0.0
            # horizontal
            if self.moveLeft & (not self.moveRight):
                x_acc = -config.accChange
            elif self.moveRight & (not self.moveLeft):
                x_acc = +config.accChange
            else:
                x_acc = 0.0
        # HARD controls
        else:
            # engine on
            if self.move:
                # vertical
                y_acc = -cos(self.radians)*config.accChange
                # horizontal
                x_acc = -sin(self.radians)*config.accChange
            # engine off
            else:
                x_acc = 0.0
                y_acc = 0.0
        # indicator for waiting for level start
        if self.waiting and (x_acc != 0.0 or y_acc != 0.0):
            self.waiting = False
        # return
        return((x_acc,y_acc))
        
    def computeRadians(self, mouse_pos):
        # mouse position
        mouse_x, mouse_y = mouse_pos
        # ship location
        ship_y = self.y_loc*modelToViewRatio + verti_offset
        ship_x = self.x_loc*modelToViewRatio + horiz_offset
        # calculate radians
        change_y = ship_y - mouse_y
        change_x = ship_x - mouse_x
        self.radians = atan2(change_x,change_y)
    
    def lostInSpace(self):
        # has post ship left the board?
        if   self.x_loc > self.board.xmax + self.size/2.0:
            return(True)
        elif self.x_loc < self.board.xmin - self.size/2.0:
            return(True)
        elif self.y_loc > self.board.ymax + self.size/2.0:
            return(True)
        elif self.y_loc < self.board.ymin - self.size/2.0:
            return(True)
        else:
            return(False)
        
    def makeDrawer(self):
        if easyControls:
            return(PostShipEasyDrawer(self))
        else:
            return(PostShipHardDrawer(self))

#------------------------------------------------------------
# Post Box
class PostBox:
    """Location for post ship deliveries.
    Location is (x,y) tuple.
    Board is map board post box belongs on."""
    def __init__(self,location, board, 
                 innerSize = config.postBoxInnerSize, outerSize = config.postBoxOuterSize):
        # store parameters
        self.x_loc, self.y_loc = location
        self.board = board
        self.innerSize = innerSize
        self.outerSize = outerSize
        self.delivered = False
        
    def timeStep(self,postShip):
        # distance to postship
        dist = (postShip.x_loc - self.x_loc)**2 + (postShip.y_loc - self.y_loc)**2
        limit = (self.outerSize/2.0)**2
        # check for delivery
        if dist < limit and not self.delivered:
            self.delivered = True
        
    def collisionCheck(self,postShip):
        # distance to postship
        dist = (postShip.x_loc - self.x_loc)**2 + (postShip.y_loc - self.y_loc)**2
        limit = (self.innerSize/2.0 + postShip.size/2.0)**2
        # check for collision
        return(dist < limit and config.precisionDelivery)
        
    def makeDrawer(self):
        return(PostBoxDrawer(self))

    
#------------------------------------------------------------
# Asteroid
class AsteroidHazard:
    """Asteriod hazard for postship.
    Location is (x,y) tuple.
    Board is map board asteroid belongs on."""
    def __init__(self,location, board, 
                 size = config.asteroidSize):
        # store parameters
        self.x_loc, self.y_loc = location
        self.board = board
        self.size = size
        self.delivered = True
        
    def timeStep(self,postShip):
        pass
        
    def collisionCheck(self,postShip):
        # distance to postship
        dist = (postShip.x_loc - self.x_loc)**2 + (postShip.y_loc - self.y_loc)**2
        limit = (self.size/2.0 + postShip.size/2.0)**2
        # check for collision
        if dist < limit:
            return(True)
        else:
            return(False)
        
    def makeDrawer(self):
        return(AsteroidHazardDrawer(self))
    
    
#------------------------------------------------------------
# Warp out
class WarpOut:
    """End of level warp out.
    Location is (x,y) tuple.
    Board is map board warp out belongs on."""
    def __init__(self,location, board, 
                 outerSize = config.warpOutOuterSize,
                 innerSize = config.warpOutInnerSize):
        # store parameters
        self.x_loc, self.y_loc = location
        self.board = board
        self.outerSize = outerSize
        self.innerSize = innerSize
        self.delivered = True
        
    def timeStep(self,postShip):
        pass
        
    def collisionCheck(self,postShip):
        # distance to postship
        dist = (postShip.x_loc - self.x_loc)**2 + (postShip.y_loc - self.y_loc)**2
        limit = (self.innerSize/2.0 + postShip.size/2.0)**2
        # check for collision
        if dist < limit:
            return(True)
        else:
            return(False)
        
    def makeDrawer(self):
        return(WarpOutDrawer(self))

        
#------------------------------------------------------------
# VIEW
#------------------------------------------------------------

#------------------------------------------------------------
# Master Drawer
class MasterDrawer:
    """Responsible for creating and holding all the drawing
    objects as a central place for drawing the screen."""
    def __init__(self, board, postShip, warpOut, spaceObjects):
        # create component drawers
        self.board = MapBoardDrawer(board)
        self.postShip = postShip.makeDrawer()
        self.warpOut = warpOut.makeDrawer()
        # space objects
        self.spaceObjects = [obj.makeDrawer() for obj in spaceObjects]
        
    def redraw(self,iFlip=True,waiting=False):
        # clear screen before redrawing
        screen.fill(0)
        # draw commands
        # back ground
        self.board.drawMapBoard()
        # warp out
        self.warpOut.draw()
        # space objects
        for obj in self.spaceObjects:
            obj.draw()
        # post ship
        self.postShip.drawPostShip()
        # redraw boundaries
        self.board.drawBoundaries()
        # update the screen
        if iFlip:
            # draw text on board
            self.board.drawText(waiting)
            # flip screen
            pygame.display.flip()
        
#------------------------------------------------------------
# Map Board Drawer
class MapBoardDrawer:
    """Responsible for drawing the board on the game screen."""
    def __init__(self,board):
        # store board
        self.board = board
        # load assets
        self.loadAssets()
        # rescale assets
        self.scaleAssets()
        self.text,self.textRect = self.scaleText()
        
    def loadAssets(self):
        self.starBackground = pygame.image.load(config.starBackground)
    
    def scaleAssets(self):
        # make key values global
        global modelToViewRatio
        global verti_offset
        global horiz_offset
        # fit board size to screen size
        # maximum ratio of model to view pixels
        modelToViewRatio = floor(min( 1.0 * screenHeight / (self.board.ymax - self.board.ymin) , 1.0 * screenWidth / (self.board.xmax - self.board.xmin) ))
        # board pixel size
        boardPixelHeight = modelToViewRatio * (self.board.ymax - self.board.ymin)
        boardPixelWidth  = modelToViewRatio * (self.board.xmax - self.board.xmin)
        # checks
        assert boardPixelHeight <= screenHeight, 'pixel height of board must be at most height of screen'
        assert boardPixelWidth  <= screenWidth , 'pixel width  of board must be at most width  of screen'
        # horizontal and vertical offsets
        verti_offset = floor((screenHeight - boardPixelHeight)/2.0)
        horiz_offset = floor((screenWidth  - boardPixelWidth )/2.0)
        
        # scale up if necessary
        rescaleRatio = max( boardPixelWidth / self.starBackground.get_width() , boardPixelHeight / self.starBackground.get_height() , 1 )
        tmpBackground = pygame.transform.scale(self.starBackground, (ceil(self.starBackground.get_width()*rescaleRatio),ceil(self.starBackground.get_height()*rescaleRatio)))
        # random start point
        tmp_width = tmpBackground.get_width()
        tmp_height = tmpBackground.get_height()
        x_start = randint(0,tmpBackground.get_width()  - boardPixelWidth)
        y_start = randint(0,tmpBackground.get_height() - boardPixelHeight)
        # clip out
        subimage = tmpBackground.subsurface(x_start,y_start,int(boardPixelWidth),int(boardPixelHeight))
        # save
        subimage = subimage.convert()
        self.starBackground = subimage
    
    def scaleText(self):
        # initial font size
        fontSize = config.messageSize
        # iterate until satisfied
        while True:
            # title text
            font = pygame.font.Font('FreeSansBold.ttf', fontSize)
            text = font.render(self.board.text, True, config.WHITE)
            # get widths
            textWidth = text.get_width()
            # check fits
            if (textWidth < screenWidth):
                break
            else:
                fontSize = int(fontSize / 1.2)
        # rectangles containing text
        textRect = text.get_rect()
        # locate rectangles horizontally
        textRect.left = self.board.text_loc[0] * modelToViewRatio + horiz_offset
        textRect.top  = self.board.text_loc[1] * modelToViewRatio + verti_offset
        # store
        return(text, textRect)
    
    def drawMapBoard(self):
        # draw background
        screen.blit(self.starBackground,(horiz_offset,verti_offset))
        
    def drawBoundaries(self):
        # top rectangle
        left_edge = 0
        top_edge = 0
        width = screenWidth
        height = verti_offset
        pygame.draw.rect(screen, config.BLACK, (left_edge,top_edge,width,height))
        # bottom rectangle
        left_edge = 0
        top_edge = verti_offset + self.starBackground.get_height()
        width = screenWidth
        height = screenHeight - top_edge
        pygame.draw.rect(screen, config.BLACK, (left_edge,top_edge,width,height))
        # left rectangle
        left_edge = 0
        top_edge = 0
        width = horiz_offset
        height = screenHeight
        pygame.draw.rect(screen, config.BLACK, (left_edge,top_edge,width,height))        
        # right rectangle
        left_edge = horiz_offset + self.starBackground.get_width()
        top_edge = 0
        width = screenWidth - left_edge
        height = screenHeight
        pygame.draw.rect(screen, config.BLACK, (left_edge,top_edge,width,height))
        
    def drawText(self,waiting=False):
        # current time
        nowTime = pygame.time.get_ticks()
        # elapsed time
        elapsedSeconds = (nowTime - startTime)/1000
        # display time
        secs = elapsedSeconds % 60
        mins = (elapsedSeconds - secs)/60
        
        # location to display
        displayAt = (10,10)
        # text to display
        text = str(int(mins))+":"+str(round(secs,1))
        # timer text
        font = pygame.font.Font('FreeSansBold.ttf', config.timerSize)
        text = font.render(text, True, config.WHITE)
        
        # draw time
        screen.blit(text, displayAt)
        # draw text
        screen.blit(self.text, self.textRect)
        
        # if waiting inform player
        if waiting:
            # message
            text = 'Ready'
            # waiting text
            font = pygame.font.Font('FreeSansBold.ttf', config.waitingSize)
            text = font.render(text, True, config.WHITE)
            # draw location
            textRect = text.get_rect()
            textRect.center = (screenWidth/2,screenHeight/2)
            # draw text
            screen.blit(text, textRect)
        
        
#------------------------------------------------------------
# Post Ship Drawer - Easy
class PostShipEasyDrawer:
    """Responsible for drawing the easy version post ship on the game screen."""
    def __init__(self,postShip):
        # store parameters
        self.postShip = postShip
        # load assets
        self.loadAssets()
        # rescale assets
        self.scaleAssets()
        
    def loadAssets(self):
        self.shipImage = pygame.image.load(config.easyShip)
        self.engineFire = pygame.image.load(config.engineFire)
    
    def scaleAssets(self):
        # rescale ship image
        rescaleRatio = modelToViewRatio * self.postShip.size / (self.shipImage.get_height() - 4)
        new_width  = ceil(self.shipImage.get_width()  * rescaleRatio)
        new_height = ceil(self.shipImage.get_height() * rescaleRatio)
        # save ship image
        self.shipImage = pygame.transform.smoothscale(self.shipImage, (new_width, new_height))
        # prep for blit
        self.shipImage = self.shipImage.convert_alpha()
        
        # rescale engine fire
        new_width  = ceil(self.engineFire.get_width()  * rescaleRatio)
        new_height = ceil(self.engineFire.get_height() * rescaleRatio)
        # save fire
        self.engineFireTop = pygame.transform.smoothscale(self.engineFire, (new_width, new_height))
        # prep for blit
        self.engineFireTop = self.engineFireTop.convert_alpha()
        
        # rotate engine fire
        self.engineFireLeft   = pygame.transform.rotate(self.engineFireTop, 90)
        self.engineFireBottom = pygame.transform.rotate(self.engineFireTop,180)
        self.engineFireRight  = pygame.transform.rotate(self.engineFireTop,270)
        
    def drawPostShip(self):
        # post ship position
        x_loc = int(0.5 + self.postShip.x_loc*modelToViewRatio)+horiz_offset
        y_loc = int(0.5 + self.postShip.y_loc*modelToViewRatio)+verti_offset
        # align
        tmpRect = self.shipImage.get_rect()
        tmpRect.centerx = x_loc
        tmpRect.centery = y_loc
        # blit
        screen.blit(self.shipImage, tmpRect)
        ##pygame.draw.circle(screen, config.GREEN, (x_loc,y_loc), round(self.postShip.size*modelToViewRatio/2), 0)
        # engine offset
        engOffset = self.postShip.size/2.0 + config.engineOffset
        # engines
        if self.postShip.moveUp:
            # position
            x_loc = int(0.5 +  self.postShip.x_loc             *modelToViewRatio)+horiz_offset
            y_loc = int(0.5 + (self.postShip.y_loc + engOffset)*modelToViewRatio)+verti_offset
            # align
            tmpRect = self.engineFireBottom.get_rect()
            tmpRect.centerx = x_loc
            tmpRect.centery = y_loc
            # blit
            screen.blit(self.engineFireBottom, tmpRect)
            ##pygame.draw.circle(screen, config.RED, (x_loc,y_loc), int(0.5 + self.postShip.size*modelToViewRatio/10), 0)
        if self.postShip.moveDown:
            # position
            x_loc = int(0.5 +  self.postShip.x_loc             *modelToViewRatio)+horiz_offset
            y_loc = int(0.5 + (self.postShip.y_loc - engOffset)*modelToViewRatio)+verti_offset
            # align
            tmpRect = self.engineFireTop.get_rect()
            tmpRect.centerx = x_loc
            tmpRect.centery = y_loc
            # blit
            screen.blit(self.engineFireTop, tmpRect)
            ##pygame.draw.circle(screen, config.RED, (x_loc,y_loc), int(0.5 + self.postShip.size*modelToViewRatio/10), 0)
        if self.postShip.moveLeft:
            # position
            x_loc = int(0.5 + (self.postShip.x_loc + engOffset)*modelToViewRatio)+horiz_offset
            y_loc = int(0.5 +  self.postShip.y_loc             *modelToViewRatio)+verti_offset
            # align
            tmpRect = self.engineFireRight.get_rect()
            tmpRect.centerx = x_loc
            tmpRect.centery = y_loc
            # blit
            screen.blit(self.engineFireRight, tmpRect)
            ##pygame.draw.circle(screen, config.RED, (x_loc,y_loc), int(0.5 + self.postShip.size*modelToViewRatio/10), 0)
        if self.postShip.moveRight:
            # position
            x_loc = int(0.5 + (self.postShip.x_loc - engOffset)*modelToViewRatio)+horiz_offset
            y_loc = int(0.5 +  self.postShip.y_loc             *modelToViewRatio)+verti_offset
            # align
            tmpRect = self.engineFireLeft.get_rect()
            tmpRect.centerx = x_loc
            tmpRect.centery = y_loc
            # blit
            screen.blit(self.engineFireLeft, tmpRect)
            ##pygame.draw.circle(screen, config.RED, (x_loc,y_loc), int(0.5 + self.postShip.size*modelToViewRatio/10), 0)

#------------------------------------------------------------
# Post Ship Drawer - Hard
class PostShipHardDrawer:
    """Responsible for drawing the hard version post ship on the game screen."""
    def __init__(self,postShip):
        # store parameters
        self.postShip = postShip
        # load assets
        self.loadAssets()
        # rescale assets
        self.scaleAssets()
        
    def loadAssets(self):
        self.shipImage = pygame.image.load(config.hardShip)
        self.engineFire = pygame.image.load(config.engineFire)
    
    def scaleAssets(self):
        # rescale ship image
        rescaleRatio = modelToViewRatio * self.postShip.size / (self.shipImage.get_height() - 4)
        new_width  = ceil(self.shipImage.get_width()  * rescaleRatio)
        new_height = ceil(self.shipImage.get_height() * rescaleRatio)
        # save ship image
        self.shipImage = pygame.transform.smoothscale(self.shipImage, (new_width, new_height))
        # prep for blit
        self.shipImage = self.shipImage.convert_alpha()
        
        # rescale engine fire
        new_width  = ceil(self.engineFire.get_width()  * rescaleRatio)
        new_height = ceil(self.engineFire.get_height() * rescaleRatio)
        # rotate
        self.engineFire = pygame.transform.rotate(self.engineFire,180)
        # save fire
        self.engineFire = pygame.transform.smoothscale(self.engineFire, (new_width, new_height))
        # prep for blit
        self.engineFire = self.engineFire.convert_alpha()
        
    def drawPostShip(self):
        # post ship position
        x_loc = int(0.5 + self.postShip.x_loc*modelToViewRatio)+horiz_offset
        y_loc = int(0.5 + self.postShip.y_loc*modelToViewRatio)+verti_offset
        # rotate
        degrees = self.postShip.radians/(2*pi)*360
        tmpImage = pygame.transform.rotate(self.shipImage, degrees)
        # align
        tmpRect = tmpImage.get_rect()
        tmpRect.centerx = x_loc
        tmpRect.centery = y_loc
        # blit
        screen.blit(tmpImage, tmpRect)
        ##pygame.draw.circle(screen, config.GREEN, (x_loc,y_loc), round(self.postShip.size*modelToViewRatio/2), 0)
        # engines
        if self.postShip.move:
            # position
            x_adjust = (self.postShip.size/2.0 + config.engineOffset) * sin(self.postShip.radians + pi)
            y_adjust = (self.postShip.size/2.0 + config.engineOffset) * cos(self.postShip.radians + pi)
            x_loc = int(0.5 + (self.postShip.x_loc - x_adjust) * modelToViewRatio)+horiz_offset
            y_loc = int(0.5 + (self.postShip.y_loc - y_adjust) * modelToViewRatio)+verti_offset
            # rotate
            tmpImage = pygame.transform.rotate(self.engineFire, degrees)
            # align
            tmpRect = tmpImage.get_rect()
            tmpRect.centerx = x_loc
            tmpRect.centery = y_loc
            # blit
            screen.blit(tmpImage, tmpRect)
            ##pygame.draw.circle(screen, config.RED, (x_loc,y_loc), int(0.5 + self.postShip.size*modelToViewRatio/10), 0)

#------------------------------------------------------------
# Post Box Drawer
class PostBoxDrawer:
    """Responsible for drawing post boxes on the game screen."""
    def __init__(self,postBox):
        # store parameters
        self.postBox = postBox
        # load assets
        self.loadAssets()
        # rescale assets
        self.scaleAssets()
        
    def loadAssets(self):
        pass
    
    def scaleAssets(self):
        pass
    
    def draw(self):
        # target area if awaiting delivery
        if not self.postBox.delivered:
            ## draw with only delivery areas transparent - almost as fast as no transparency
            # pizel size of post box
            size = int(0.5 + self.postBox.outerSize*modelToViewRatio)
            # transparent sub screen
            s = pygame.Surface((size,size), pygame.SRCALPHA)
            # draw circle
            pygame.draw.circle(s, config.transLIGHTGREY,  (int(0.5 + size/2.0),int(0.5 + size/2.0)), int(0.5 + size/2.0), 0)
            screen.blit(s, (int(0.5 + self.postBox.x_loc*modelToViewRatio-size/2.0)+horiz_offset,int(0.5 + self.postBox.y_loc*modelToViewRatio-size/2.0)+verti_offset))
        # draw post box itself
        x_loc = int(0.5 + self.postBox.x_loc*modelToViewRatio)+horiz_offset
        y_loc = int(0.5 + self.postBox.y_loc*modelToViewRatio)+verti_offset
        radiu = int(0.5 + self.postBox.innerSize*modelToViewRatio/2.0)
        pygame.draw.circle(screen, config.TEAL, (x_loc,y_loc), radiu, 0)

#------------------------------------------------------------
# Asteroid Hazard Drawer
class AsteroidHazardDrawer:
    """Responsible for drawing asteroids on the game screen."""
    def __init__(self,asteroidHazard):
        # store parameters
        self.asteroid = asteroidHazard
        # load assets
        self.loadAssets()
        # rescale assets
        self.scaleAssets()
        
    def loadAssets(self):
        num = randint(1,18)
        if num == 1:
            filename = config.asteroid01
        elif num == 2:
            filename = config.asteroid02
        elif num == 3:
            filename = config.asteroid03
        elif num == 4:
            filename = config.asteroid04
        elif num == 5:
            filename = config.asteroid05
        elif num == 6:
            filename = config.asteroid06
        elif num == 7:
            filename = config.asteroid07
        elif num == 8:
            filename = config.asteroid08
        elif num == 9:
            filename = config.asteroid09
        elif num == 10:
            filename = config.asteroid10
        elif num == 11:
            filename = config.asteroid11
        elif num == 12:
            filename = config.asteroid12
        elif num == 13:
            filename = config.asteroid13
        elif num == 14:
            filename = config.asteroid14
        elif num == 15:
            filename = config.asteroid15
        elif num == 16:
            filename = config.asteroid16
        elif num == 17:
            filename = config.asteroid17
        elif num == 18:
            filename = config.asteroid18
        # load file
        self.asteroidTexture = pygame.image.load(filename)
    
    def scaleAssets(self):
        # rescale image
        rescaleRatio = modelToViewRatio * self.asteroid.size / (self.asteroidTexture.get_width() - 4)
        new_width  = ceil(self.asteroidTexture.get_width() * rescaleRatio)
        new_height = ceil(self.asteroidTexture.get_height()* rescaleRatio)
        tmpImage = pygame.transform.scale(self.asteroidTexture, (new_width,new_height))
        # rotate
        degrees = randint(0,360)
        tmpImage = pygame.transform.rotate(tmpImage, degrees)
        # set transparency
        tmpImage = tmpImage.convert_alpha()
        ##tmpImage.set_colorkey(config.WHITE)
        # save
        self.asteroidTexture = tmpImage
        
    def draw(self):
        # location
        x_loc = int(0.5 + self.asteroid.x_loc*modelToViewRatio)+horiz_offset
        y_loc = int(0.5 + self.asteroid.y_loc*modelToViewRatio)+verti_offset
        ##radiu = int(0.5 + self.asteroid.size*modelToViewRatio/2.0)
        # set location
        asteroidRect = self.asteroidTexture.get_rect()
        asteroidRect.centerx = x_loc
        asteroidRect.centery = y_loc
        ##pygame.draw.circle(screen, config.BROWN, (x_loc,y_loc), radiu, 0)
        # draw texture
        screen.blit(self.asteroidTexture, asteroidRect)

#------------------------------------------------------------
# Warp Out Drawer
class WarpOutDrawer:
    """Responsible for drawing warp out on the game screen."""
    def __init__(self,warpOut):
        # store parameters
        self.warpOut = warpOut
        # load assets
        self.loadAssets()
        # rescale assets
        self.scaleAssets()
        
    def loadAssets(self):
        # load file
        self.warpOutTexture = pygame.image.load(config.warpOut)
    
    def scaleAssets(self):
        # rescale image
        rescaleRatio = modelToViewRatio * self.warpOut.outerSize / (self.warpOutTexture.get_width() - 4)
        new_width  = ceil(self.warpOutTexture.get_width() * rescaleRatio)
        new_height = ceil(self.warpOutTexture.get_height()* rescaleRatio)
        tmpImage = pygame.transform.scale(self.warpOutTexture, (new_width,new_height))
        # set transparency
        tmpImage = tmpImage.convert_alpha()
        ##tmpImage.set_colorkey(config.WHITE)
        # save
        self.warpOutTexture = tmpImage
        
    def draw(self):
        # location
        x_loc = int(0.5 + self.warpOut.x_loc*modelToViewRatio)+horiz_offset
        y_loc = int(0.5 + self.warpOut.y_loc*modelToViewRatio)+verti_offset
        ##radiu = int(0.5 + self.asteroid.size*modelToViewRatio/2.0)
        # set location
        warpOutRect = self.warpOutTexture.get_rect()
        warpOutRect.centerx = x_loc
        warpOutRect.centery = y_loc
        ##pygame.draw.circle(screen, config.BROWN, (x_loc,y_loc), radiu, 0)
        # draw texture
        screen.blit(self.warpOutTexture, warpOutRect)

#------------------------------------------------------------
# CONTROLLER
#------------------------------------------------------------

#------------------------------------------------------------
# Game instance
class GameInstance:
    """General stuff for creating and being a game"""
    def __init__(self,screen,gameType,numLevel):
        # data storage object
        self.data = DataHands.loadJson()
        # globalize screen
        self.globalize(screen)
        screen.fill(0)
        # store type and level
        self.gameType = gameType
        self.numLevel = numLevel
        # game model and view
        self.createPoints()
        self.createModel()
        self.createView()
        
        # run game
        ##self.runGame()
    
    def globalize(self,screenToGlobal):
        # make screen global
        global screen
        global screenWidth
        global screenHeight
        global screenRect
        screen = screenToGlobal
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        screenRect = screen.get_rect()
        # additional globalize
        global startTime
        global easyControls
        startTime = pygame.time.get_ticks()
        easyControls = self.data['easyControls']
    
    def createPoints(self):
        # get level
        xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc = getLevel(self.gameType,self.numLevel)
        # store
        self.xmax = xmax
        self.ymax = ymax
        self.postShip_loc  = postShip_loc
        self.warpOut_loc   = warpOut_loc
        self.postBox_locs  = postBox_locs
        self.asteroid_locs = asteroid_locs
        self.text = text
        self.text_loc = text_loc
        
    def createModel(self):
        # new map board
        self.board = MapBoard(self.xmax,self.ymax,self.text,self.text_loc)
        # new post ship
        self.postShip = PostShip(self.postShip_loc,self.board)
        # new warp out
        self.warpOut = WarpOut(self.warpOut_loc,self.board)
        # other space objects
        self.spaceObjects = []
        # add 3 post boxes
        for loc in self.postBox_locs:
            # new post box
            self.spaceObjects.append(PostBox(loc,self.board))
        # add remaining asteroid hazard
        for loc in self.asteroid_locs:
            # new asteroid
            self.spaceObjects.append(AsteroidHazard(loc,self.board))        
        
    def createView(self):
        # new master drawer
        self.view = MasterDrawer(self.board,self.postShip,self.warpOut,self.spaceObjects)
    
    def runGame(self):
        # clock
        fpsClock = pygame.time.Clock()
        global startTime
        startTime = pygame.time.get_ticks()
        # preparation
        running = 1
        status = "continue"
        self.data['numAttempts'] += 1
        # keep looping through
        while running:
            # reset clock
            if self.postShip.waiting:
                startTime = pygame.time.get_ticks()
            # redraw screen
            self.view.redraw(waiting = self.postShip.waiting)
            # resolve events
            running, status = self.resolveEvents(pygame.event.get(),running,status)
            # increment model time
            # for post ship
            self.postShip.timeStep(config.dt)
            # for space objects
            for obj in self.spaceObjects:
                obj.timeStep(self.postShip)
            # check for game over conditions
            running, status = self.checkEndGameConditions(running,status)
            # Act on game not being in continue status
            running, status = self.handleStatus(running,status)
            # Handle FPS
            ## lock FPS
            fpsClock.tick(config.FPS)
            ## find FPS (requires break post to read)
            #fpsClock.tick()
            #this_FPS = fpsClock.get_fps()
        
        # game has ended
        DataHands.saveJson(self.data)
        return(status)
            
    def resolveKeyDown(self,keyPressed):
        # track keys if using easy controls
        if easyControls:
            if (keyPressed == K_UP) | (keyPressed == K_w):
                self.postShip.moveUp = True
            elif (keyPressed == K_LEFT) | (keyPressed == K_a):
                self.postShip.moveLeft = True
            elif (keyPressed==K_DOWN) | (keyPressed == K_s):
                self.postShip.moveDown = True
            elif (keyPressed==K_RIGHT) | (keyPressed == K_d):
                self.postShip.moveRight = True
        # don't track keys otherwise
        else:
            pass
            
    def resolveKeyUp(self,keyPressed):
        # track keys if using easy controls
        if easyControls:
            if (keyPressed == K_UP) | (keyPressed == K_w):
                self.postShip.moveUp = False
            elif (keyPressed == K_LEFT) | (keyPressed == K_a):
                self.postShip.moveLeft = False
            elif (keyPressed==K_DOWN) | (keyPressed == K_s):
                self.postShip.moveDown = False
            elif (keyPressed==K_RIGHT) | (keyPressed == K_d):
                self.postShip.moveRight = False
        # don't track keys otherwise
        else:
            pass

    def resolveEvents(self,eventList,running,status):
        # default = no change
        # loop through events
        for event in eventList:
            # EXIT COMMANDS
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # quit the game
                running = 0
                status = 'quit'
            # check if the event is Alt+F4
            if (event.type == KEYDOWN) and (event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                # quit the game
                running = 0
                status = 'quit'
            # check if event is abort
            if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
                # stop game
                running = 0
                status = 'abort'
            
            # EASY SHIP CONTROLS
            # key down
            if event.type == pygame.KEYDOWN:
                # resolve key
                self.resolveKeyDown(event.key)
            # key up
            if event.type == pygame.KEYUP:
                # resolve key
                self.resolveKeyUp(event.key)
            
            # HARD SHIP CONTROLS
            # mouse down
            if not easyControls and event.type == pygame.MOUSEBUTTONDOWN:
                # left mouse button only
                if event.button == 1:
                    self.postShip.move = True
            # mouse up
            if not easyControls and event.type == pygame.MOUSEBUTTONUP:
                # left mouse button only
                if event.button == 1:
                    self.postShip.move = False
        
        # track mouse
        if not easyControls:
            self.postShip.computeRadians(pygame.mouse.get_pos())        
        # all events resolved
        return((running,status))
    
    def checkEndGameConditions(self,running,status):
        # default = no change
        # lost in space
        if self.postShip.lostInSpace():
            # we are lost
            running = 0
            status = 'lost'
            self.data['numLost'] += 1
        # collision
        collision = [obj.collisionCheck(self.postShip) for obj in self.spaceObjects]
        if any(collision):
            # we have crashed
            running = 0
            status = 'crashed'
            self.data['numCrashes'] += 1
        # all mail delivered
        delivered = [obj.delivered for obj in self.spaceObjects]
        atWormHole = self.warpOut.collisionCheck(self.postShip)
        if atWormHole and not all(delivered):
            # we have warped out early
            running = 0
            status = 'early'
            self.data['numEarly'] += 1
        elif atWormHole and all(delivered):
            # we have completed mail run
            running = 0
            status = 'complete'
            self.data['numComplete'] += 1
        
        # all conditions checked
        return((running,status))
    
    def handleStatus(self,running,status):
        # current time
        nowTime = pygame.time.get_ticks()
        # start time is global
        global startTime
        # default = no change
        if status == 'continue':
            return((running,status))
        # GAME END STATUS
        if status in ['lost','crashed','early','complete']:
            # select transparency color
            if status in ['lost','crashed','early']:
                transCol = config.transRED
            elif status == 'complete':
                transCol = config.transGREEN
            # transparent cover on game screen
            self.view.redraw(False)
            s = pygame.Surface((screenWidth,screenHeight), pygame.SRCALPHA)
            s.fill(transCol)
            screen.blit(s, (0,0))
            pygame.display.flip()
            # save image
            pygame.image.save(screen,config.tmpMenuBackgrd)
            # text
            if status == 'lost':
                text1 = "Deliveries Failed"
                text2 = "Lost in Space"
            elif status == 'crashed':
                text1 = "Deliveries Failed"
                text2 = "Crashed post ship"
            elif status == 'early':
                text1 = "Deliveries Failed"
                text2 = "Warped out without delivering mail"
            else:
                secondsElapsed = round((nowTime - startTime)/1000,1)
                self.storeSeconds(secondsElapsed)
                timeText = str(secondsElapsed)+"sec"
                text1 = "Good work!"
                text2 = "All mail delivered in "+timeText
            # call menu
            MI = MenuInstance(screen, text1, text2,['Menu','New','Replay'],config.tmpMenuBackgrd)
            status = MI.run(status=="complete")
        
        # STATUS FROM MENU INSTANCE
        # return to main menu
        if status == 'Menu':
            # equivalent to abort
            status = 'abort'
            running = 0
        # replay
        if status == 'Replay':
            # remake level
            self.createModel()
            self.createView()
            startTime = pygame.time.get_ticks()
            # new status
            status = "continue"
            running = 1
            self.data['numAttempts'] += 1
        # new level
        if status == 'New':
            # increment level
            self.numLevel += 1
            if self.numLevel == 31:
                self.numLevel = 1
            # make new level
            self.createPoints()
            self.createModel()
            self.createView()
            startTime = pygame.time.get_ticks()
            # new status
            status = "continue"
            running = 1
            self.data['numAttempts'] += 1
        # return
        return((running,status))

    def storeSeconds(self,secondsElapsed):
        if easyControls and self.gameType == 'training':
            self.data['easyLevelRecords'][self.numLevel-1].append(secondsElapsed)
        elif not easyControls and self.gameType == 'training':
            self.data['hardLevelRecords'][self.numLevel-1].append(secondsElapsed)
        else:
            pass

#------------------------------------------------------------
# run
if __name__ == '__main__':
    width = 1240
    height = 880
    # initialize
    pygame.init()
    # window
    screen = pygame.display.set_mode((width, height))
    ##screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # make game instance
    trial = GameInstance(screen,'training',3)
    # run game
    status = trial.runGame()
    # quit
    pygame.quit()
#------------------------------------------------------------


# To do
# - main menu
# - display recommended level times

