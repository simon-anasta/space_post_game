#!/usr/bin/python

#------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------

# External modules
import pygame

# Internal modules
import config
from SpaceDelivery import GameInstance
from MenuMaker import MenuInstance
import DataHands

#------------------------------------------------------------
# Load welcome screen

def setup(screen):
    welcomeMenuBackground = loadAssets()
    welcomeMenuBackground = scaleAssets(welcomeMenuBackground,screen)
    pygame.image.save(welcomeMenuBackground,config.tmpWelcomeMBack)

def loadAssets():
    welcomeBackground = pygame.image.load(config.welcomeMenuBack)
    return(welcomeBackground)

def scaleAssets(background,screen):
    # heights
    backgroundHeight = background.get_height()
    screenHeight = screen.get_height()
    # scale ratio
    rescaleRatio = screenHeight / backgroundHeight
    # rescale to match height
    newHeight = int(0.5 + backgroundHeight*rescaleRatio)
    newWidth  = int(0.5 + background.get_width()*rescaleRatio)
    background = pygame.transform.smoothscale(background, (newWidth, newHeight))
    
    # widths
    backgroundWidth = background.get_width()
    screenWidth = screen.get_width()
    assert backgroundWidth >= screenWidth, 'screen too large for background'
    # starting points
    x_start = int(0.5 + 0.5*(backgroundWidth-screenWidth))
    # clip out image for welcome menu
    background = background.subsurface(x_start,0,screenWidth,screenHeight)
    return(background)
    
#------------------------------------------------------------
# Menu maker

def makeMenuButtons():
    # menu buttons
    menuButtons = ['Campeign','Random','Mode = Hard','Exit']
    # load data
    data = DataHands.loadJson()
    # easy mode
    if data['easyControls']:
        menuButtons[2] = 'Mode = Easy'
    # return
    return(menuButtons)

def makeMenu(screen):
    # menu buttons
    menuButtons = makeMenuButtons()
    # call menu
    MI = MenuInstance(screen, '', '',menuButtons,config.tmpWelcomeMBack)
    # return
    return(MI)

#------------------------------------------------------------
# Status handler

def handleStatus(running,status):
    if status == 'Campeign':
        # make game instance
        GI = GameInstance(screen,'training',1)
        status = GI.runGame()
    elif status == 'Random':
        # make game instance
        GI = GameInstance(screen,'random',1)
        status = GI.runGame()
    elif status == 'Mode = Easy':
        # change to hard mode
        data = DataHands.loadJson()
        data['easyControls'] = False
        DataHands.saveJson(data)
        # return status to continue
        status = 'continue'
    elif status == 'Mode = Hard':
        # change to easy mode
        data = DataHands.loadJson()
        data['easyControls'] = True
        DataHands.saveJson(data)        
        # return status to continue
        status = 'continue'
    elif status == 'Exit' or status == 'quit':
        # stop running
        running = 0
    else:
        assert False, status
    # retru
    return((running,status))

#------------------------------------------------------------
# Run

if __name__ == '__main__':
    # initialize
    pygame.init()
    # create screen
    if config.windowed:
        width = 1240
        height = 880
        screen = pygame.display.set_mode((width, height))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # setup
    setup(screen)
    running = 1
    status = 'continue'
    
    # keep looping through
    while running == 1:
        # make menu
        MI = makeMenu(screen)
        status = MI.run(True)
        # resolve status
        running,status = handleStatus(running,status)
        
    # quit
    pygame.quit()
