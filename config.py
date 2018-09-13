#!/usr/bin/python

#------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------


#------------------------------------------------------------
# Parameters

FPS = 40
dt = 0.05
windowed = False

# gameplay
##easyControls = False
precisionDelivery = False

# object sizes
postShipSize = 1.0 ## default is 1.0
postBoxInnerSize = 0.5 ## default is 0.5
postBoxOuterSize = 2.5 ## default is 2.5
asteroidSize = 3.0 ## default is 3.0
warpOutOuterSize = 2.7
warpOutInnerSize = 0.3
# ship
accChange = 1.5
engineOffset = 0.15
# board
timerSize = 24
messageSize = 36
waitingSize = 180
# menu base
shareText = 0.33
shareButtons = 0.67
menuFontSize = 80
# menu buttons
buttonWidth = 222
buttonHeight = 100
buttonFontSize = 36
# random level defaults
xmax = 18
ymax = 15
numPostBox = 3
numAsteroid = 3
# number of levels made
numLevelsMade = 30

#------------------------------------------------------------
# Colours

RED       = (255,  0,  0)
BLACK     = (  0,  0,  0)
BLUE      = (  0,  0,255)
GREEN     = (  0,255,  0)
WHITE     = (255,255,255)
LIGHTGREY = (200,200,200)
TEAL      = (  0,250,100)
BROWN     = (139, 69, 19)
# transparent
transLIGHTGREY = (200,200,200,110)
transDARKGREY  = (100,100,100, 90)
transGREEN     = ( 90,255, 90, 90)
transRED       = (155,  0,  0, 90)

#------------------------------------------------------------
# Files

# data file for saving setting and scores
dataLocation    = "Resources/data.json"
# back ground
starBackground  = "Resources/Images/StarsBackground.png"
tmpMenuBackgrd  = "Resources/Images/tmpMenuBackground.png"
welcomeMenuBack = "Resources/Images/welcomeMenuBackground.png"
tmpWelcomeMBack = "Resources/Images/tmpWelcomeMenuBackground.png"
# ships
easyShip        = "Resources/Images/ShipEasy_alpha.png"
hardShip        = "Resources/Images/ShipHard_alpha.png"
engineFire      = "Resources/Images/engineFire_alpha.png"
# asteroid
asteroidTexture = "Resources/Images/asteroid texture.png"
asteroid01      = "Resources/Images/asteroid01_alpha.png"
asteroid02      = "Resources/Images/asteroid02_alpha.png"
asteroid03      = "Resources/Images/asteroid03_alpha.png"
asteroid04      = "Resources/Images/asteroid04_alpha.png"
asteroid05      = "Resources/Images/asteroid05_alpha.png"
asteroid06      = "Resources/Images/asteroid06_alpha.png"
asteroid07      = "Resources/Images/asteroid07_alpha.png"
asteroid08      = "Resources/Images/asteroid08_alpha.png"
asteroid09      = "Resources/Images/asteroid09_alpha.png"
asteroid10      = "Resources/Images/asteroid10_alpha.png"
asteroid11      = "Resources/Images/asteroid11_alpha.png"
asteroid12      = "Resources/Images/asteroid12_alpha.png"
asteroid13      = "Resources/Images/asteroid13_alpha.png"
asteroid14      = "Resources/Images/asteroid14_alpha.png"
asteroid15      = "Resources/Images/asteroid15_alpha.png"
asteroid16      = "Resources/Images/asteroid16_alpha.png"
asteroid17      = "Resources/Images/asteroid17_alpha.png"
asteroid18      = "Resources/Images/asteroid18_alpha.png"
# warp out
warpOut         = "Resources/Images/wormHole_trial2.png"