#!/usr/bin/python

#------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------

# External modules
import pygame
from pygame.locals import KMOD_ALT, K_F4, QUIT, KEYDOWN, KEYUP, Rect
from random import randint
import config

#------------------------------------------------------------
# VIEW
#------------------------------------------------------------

#------------------------------------------------------------
# Menu drawer
class MenuDrawer:
    """Draws the menu"""
    def __init__(self,messageText1,messageText2,backgroundFilename,buttons):
        # store parameters
        self.buttons = [button.makeDrawer() for button in buttons]
        # prepare images
        self.displayBackground = self.prepareBackground(backgroundFilename)
        # prepare text
        self.text1, self.text1Rect, self.text2, self.text2Rect = self.scaleText(messageText1,messageText2)
        
    def redraw(self,win=False):
        # draw yourself
        self.draw()
        # draw your buttons
        for button in self.buttons:
            button.draw(win)
        # update the screen
        pygame.display.flip()
        
    def prepareBackground(self,backgroundFilename):
        # load background
        background = pygame.image.load(backgroundFilename)
        # size of background
        backgroundWidth  = background.get_width()
        backgroundHeight = background.get_height()
        # scale up if necessary
        rescaleRatio = max( screenWidth / backgroundWidth, screenHeight / backgroundHeight, 1)
        tmpBackground = pygame.transform.scale(background, (int(0.4+backgroundWidth*rescaleRatio),int(0.4+backgroundHeight*rescaleRatio)))
        # random start point
        tmp_width = tmpBackground.get_width()
        tmp_height = tmpBackground.get_height()
        x_start = randint(0,tmp_width  - screenWidth)
        y_start = randint(0,tmp_height - screenHeight)
        # clip out
        subimage = tmpBackground.subsurface(x_start,y_start,screenWidth,screenHeight)
        # save
        return(subimage)
    
    def scaleText(self,messageText1,messageText2):
        # initial font size
        fontSize = config.menuFontSize
        # iterate until satisfied
        while True:
            # title text
            font = pygame.font.Font('FreeSansBold.ttf', fontSize)
            text1 = font.render(messageText1, True, config.WHITE)
            text2 = font.render(messageText2, True, config.WHITE)
            # get widths
            text1Width = text1.get_width()
            text2Width = text2.get_width()
            # check fits
            if (text1Width < screenWidth) and (text2Width < screenWidth):
                break
            else:
                fontSize = int(fontSize / 1.2)
        # rectangles containing text
        text1Rect = text1.get_rect()
        text2Rect = text2.get_rect()
        # locate rectangles horizontally
        text1Rect.centerx = screenRect.centerx
        text2Rect.centerx = screenRect.centerx
        # locate rectangles vertically
        text1Rect.centery = int(config.shareText*screenHeight - text1Rect.height * 1.2)
        text2Rect.centery = int(config.shareText*screenHeight - text2Rect.height * 0.2)
        # store
        return(text1, text1Rect, text2, text2Rect)
        
    def draw(self):
        # draw background
        screen.blit(self.displayBackground,(0,0))
        # draw text
        screen.blit(self.text1, self.text1Rect)
        screen.blit(self.text2, self.text2Rect)

#------------------------------------------------------------
# Menu button drawer
class MenuButtonDrawer:
    """Draws menu buttons"""
    def __init__(self,text,rectangle):
        # store parameters
        self.buttonRect = rectangle
        # rescale assets
        self.text, self.textRect = self.scaleText(text)
        
    def scaleText(self,text):
        # button text
        font = pygame.font.Font('FreeSansBold.ttf', config.buttonFontSize)
        text = font.render(text, True, config.WHITE)
        textRect = text.get_rect()
        textRect.center = self.buttonRect.center
        # store
        return(text, textRect)
        
    def draw(self,win=False):
        # button color
        if win:
            buttonCol = config.GREEN
        else:
            buttonCol = config.RED
        # bounding rectangle + 4 size
        buttonBacking = self.buttonRect.inflate(4,4)
        pygame.draw.rect(screen, buttonCol, buttonBacking)
        # button proper
        pygame.draw.rect(screen, config.BLACK, self.buttonRect)
        # draw text
        screen.blit(self.text, self.textRect)


#------------------------------------------------------------
# CONTROL
#------------------------------------------------------------

#------------------------------------------------------------
# Welcome menu instance
class MenuInstance:
    """General function for making menu instances.
    Required input:
    - screen for display
    - message text 1
    - message text 2
    - button list
    - background image"""
    def __init__(self,screen,messageText1,messageText2,buttonList,backgroundImage):
        # globalize screen
        self.globalize(screen)
        # make buttons
        self.buttons = self.makeButtons(buttonList)
        # make drawer
        self.view = MenuDrawer(messageText1,messageText2,backgroundImage,self.buttons)
        
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
        
    def makeButtons(self,buttonList):
        # number of buttons
        numButtons = len(buttonList)
        # vertical distance buttons start from top of screen
        verticalOffset = int(config.shareText*screenHeight + config.shareButtons*screenHeight/2.0/numButtons)
        # vertical gap between buttons
        ##verticalGap = int(config.shareButtons*screenHeight/1.0/numButtons)
        verticalGap = int(config.buttonHeight * 1.2)
        # horizontal location of middle of button
        xCenter = int(screenWidth/2.0)
        
        # create empty list for button objects
        buttonObjs = []
        # iterate through buttons
        for i in range(len(buttonList)):
            # Text for button
            text = buttonList[i]
            # vertical location of middle of button
            yCenter = int(verticalOffset + verticalGap*i)
            # make button
            newButton = MenuButton(text,xCenter,yCenter)
            # append
            buttonObjs.append(newButton)
        # return list of button objects
        return(buttonObjs)
        
    def run(self,win=False):
        # preparation
        fpsClock = pygame.time.Clock()
        mouse_dwn_xy = (0,0)
        # keep looping through
        status = 'running'
        while status == 'running':
            # redraw screen
            self.view.redraw(win)
            # loop through user events
            for event in pygame.event.get():
                # check if the event is the X button
                if event.type == pygame.QUIT:
                    # quit the game
                    status = 'quit'
                # check if the event is Alt+F4
                if event.type == KEYDOWN and (event.key == K_F4 and bool(event.mod & KMOD_ALT)):
                    # quit the game
                    status = 'quit'
                # check if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # store coordinates
                    mouse_dwn_xy = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    # store coordinates
                    mouse_up_xy = pygame.mouse.get_pos()
                    # run clicked button
                    for button in self.buttons:
                        # if button clicked
                        if button.clickCheck(mouse_dwn_xy,mouse_up_xy):
                            status = button.text            
            # Lock FPS (upper bound)
            fpsClock.tick(config.FPS)
            ## find FPS (requires break post to read)
            #fpsClock.tick()
            #this_FPS = fpsClock.get_fps()
        # no longer running
        return(status)

#------------------------------------------------------------
# Menu button
class MenuButton:
    """Buttons for the menu"""
    def __init__(self,text,xCenter,yCenter):
        # store parameters
        self.text = text
        # make rectangle
        self.rectangle = self.makeRectangle(xCenter,yCenter)
        
    def makeRectangle(self,xCenter,yCenter):
        # rectangle
        rectangle = Rect(0,0,config.buttonWidth,config.buttonHeight)
        # align
        rectangle.centerx = xCenter
        rectangle.centery = yCenter
        # store
        return(rectangle)
        
    def clickCheck(self,mouse_dwn_xy,mouse_up_xy):
        # return if mouse down and up on button
        return(self.rectangle.collidepoint(mouse_dwn_xy) and self.rectangle.collidepoint(mouse_up_xy))
    
    def makeDrawer(self):
        return(MenuButtonDrawer(self.text,self.rectangle))

#------------------------------------------------------------
# run
if __name__ == '__main__':
    # initialize
    pygame.init()
    # create screen
    ##screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1000,900))
    # create
    trial = MenuInstance(screen, 'super lots of text all written here trial text 1', 'trial text 2',['B1','B2','B3'],'Images\StarsBackground.png')
    # run
    status = trial.run()
    # print status
    print(status)
    # quit
    pygame.quit()
#------------------------------------------------------------
