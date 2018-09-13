#!/usr/bin/python

#------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------

# External modules
from random import random

# Internal modules
import config
import DataHands

#------------------------------------------------------------
# CONTROL
#------------------------------------------------------------

def getLevel(levelType,levelNumber=0,xmax=config.xmax,ymax=config.ymax,numPostBox=config.numPostBox,numAsteroid=config.numAsteroid):
    '''Each level needs: board size,
    locations for ship, warp out, post boxes and asteroid location.
    An optional input of text and text location for instructions would be good.'''    
    # return random level
    if levelType == 'random':
        # get random level
        xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc = randomLevel(xmax=xmax,ymax=ymax,numPostBox=numPostBox,numAsteroid=numAsteroid)
    # training level
    elif levelType == 'training':
        # get numbered training level
        xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc = trainingLevel(levelNumber)
    # regular level
    elif levelType == 'standard':
        # get numbered standard level
        xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc = standardLevel(levelNumber)
    elif levelType == 'race':
        # get numbered race level
        xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc = raceLevel(levelNumber)
    else:
        # error
        assert False, 'level type not recognized'
    # return level
    return((xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc))

#------------------------------------------------------------
# RANDOM LEVEL
#------------------------------------------------------------

def randomLevel(xmax, ymax, numPostBox, numAsteroid, xmin = 0, ymin = 0):
    # creates locations for objects
    min_dist = 0
    # object counts
    numPostShip = 1
    numWarpOut = 1
    ## 8 objects = 25% change of an iteration working
    ## 4 objects = 75% chance of an iteration working
    # number of objects
    numObjects = numPostShip + numWarpOut + numPostBox + numAsteroid
    while min_dist < 2:
        # random points
        pointsx = [0.5+(xmax-1)*random() for i in range(numObjects)]
        pointsy = [0.5+(ymax-1)*random() for i in range(numObjects)]
        # check for closeness
        min_dist = xmax
        # loop through
        for i in range(numObjects):
            for j in range(i+1,numObjects):
                # calculate distance
                dist = (pointsx[i] - pointsx[j])**2 + (pointsy[i] - pointsy[j])**2
                dist = dist**0.5
                min_dist = min(min_dist,dist)
    # store points
    postShip_loc  = (pointsx[0],pointsy[0])
    warpOut_loc   = (pointsx[1],pointsy[1])
    postBox_locs  = [(pointsx[i],pointsy[i]) for i in range(2,2+numPostBox)]
    asteroid_locs = [(pointsx[i],pointsy[i]) for i in range(2+numPostBox,2+numPostBox+numAsteroid)]
    # blank text
    text = ''
    text_loc = (0,0)
    # return output
    return((xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc))

#------------------------------------------------------------
# TRAINING LEVELS
#------------------------------------------------------------

def trainingLevel(levelNumber):
    # number of levels
    numLevelsMade = config.numLevelsMade
    # check valid level
    assert 1 <= levelNumber and levelNumber <= numLevelsMade, 'requested training level does not exist'
    # default values
    text = ''
    text_loc = (0.5,0.5)
    # LEVEL LIST
    if levelNumber   ==  1:
        # trial level
        xmax = 10
        ymax = 8
        postShip_loc = (1,4)
        warpOut_loc =  (9,4)
        postBox_locs = []
        asteroid_locs = []
        # load data
        data = DataHands.loadJson()
        if data['easyControls']:
            text = 'use arrow keys or WASD to fly to worm hole'
        else:
            text = 'fly to worm hole by clicking mouse to fire engines'
    elif levelNumber ==  2:
        # learn to deliver
        xmax = 10
        ymax = 8
        postShip_loc = (1,4)
        warpOut_loc =  (9,4)
        postBox_locs = [(4,3.1)]
        asteroid_locs = []
        text = 'fly past mailbox to deliver parcel'
    elif levelNumber ==  3:
        # avoid crashing into asteroids
        xmax = 10
        ymax = 8
        postShip_loc = (6,4)
        warpOut_loc =  (9,4)
        postBox_locs = [(3,4)]
        asteroid_locs = [(1,4)]
        text = 'it takes time to slow down, avoid crashing into the asteroid'
    elif levelNumber ==  4:
        # don't leave screen
        xmax = 10
        ymax = 8
        postShip_loc = (2,4)
        warpOut_loc =  (9.5,7.5)
        postBox_locs = [(0.5,0.5),(0.5,7.5),(9.5,0.5)]
        asteroid_locs = [(7,4)]
        text = 'remain within the delivery area'
    elif levelNumber ==  5:
        # don't warp early
        xmax = 10
        ymax = 8
        postShip_loc = (1,4)
        warpOut_loc =  (5,4)
        postBox_locs = [(3,4),(7,4)]
        asteroid_locs = [(5,1)]
        text = 'deliver all parcels before warping out'
    elif levelNumber ==  6:
        # doubles
        xmax = 14
        ymax = 12
        postShip_loc = (1,6)
        warpOut_loc =  (13,6)
        postBox_locs = [(5,5),(5,7),(9,5),(9,7)]
        asteroid_locs = [(12,3),(12,9)]
    elif levelNumber ==  7:
        # centered doubles
        xmax = 14
        ymax = 12
        postShip_loc = (1,4)
        warpOut_loc =  (7,6)
        postBox_locs = [(5,4),(5,8),(9,4),(9,8)]
        asteroid_locs = [(11,11)]
    elif levelNumber ==  8:
        # orbit 1
        xmax = 14
        ymax = 12
        postShip_loc = (12,4)
        warpOut_loc =  (9,9)
        postBox_locs = [(7,4),(7,8),(2,6)]
        asteroid_locs = [(7,6)]
    elif levelNumber ==  9:
        # orbit 2
        xmax = 14
        ymax = 12
        postShip_loc = (12,4)
        warpOut_loc =  (9,9)
        postBox_locs = [(7,4),(7,8),(5,6)]
        asteroid_locs = [(7,6)]
    elif levelNumber == 10:
        # slalem
        xmax = 14
        ymax = 12
        postShip_loc = (1,0.85)
        warpOut_loc =  (13,11.11)
        postBox_locs = [(5,4.27),(9,7.69)]
        asteroid_locs = [(3,2.56),(7,5.98),(11,9.4)]
    elif levelNumber == 11:
        # box 1
        xmax = 14
        ymax = 12
        postShip_loc = (7,6)
        warpOut_loc =  (7,1)
        postBox_locs = [(7,11),(1,6),(13,6)]
        asteroid_locs = [(4,3),(4,9),(10,3),(10,9)]
    elif levelNumber == 12:
        # box 2
        xmax = 14
        ymax = 12
        postShip_loc = (1,6)
        warpOut_loc =  (11,6)
        postBox_locs = [(3,6),(7,2),(7,10)]
        asteroid_locs = [(4,3),(4,9),(10,3),(10,9)]
    elif levelNumber == 13:
        # skimmer
        xmax = 14
        ymax = 12
        postShip_loc = (12,5)
        warpOut_loc =  (2,5)
        postBox_locs = [(5,8.4),(7,8.4),(9,8.4)]
        asteroid_locs = [(4,10),(6,10),(8,10),(10,10)]
    elif levelNumber == 14:
        # scatter 1
        xmax = 16
        ymax = 12
        postShip_loc = (9,9)
        warpOut_loc  = (15,4)
        postBox_locs = [(8,1),(12,9),(2.5,10.2)]
        asteroid_locs = [(12,4),(5,9.5),(3,8)]
    elif levelNumber == 15:
        # scatter 2
        xmax = 16
        ymax = 12
        postShip_loc = (14,7)
        warpOut_loc  = (8,6)
        postBox_locs = [(8.5,11),(13,2),(2,1)]
        asteroid_locs = [(7,9),(9,9),(6,4)]
    elif levelNumber == 16:
        # scatter 3
        xmax = 16
        ymax = 12
        postShip_loc = (3,2)
        warpOut_loc  = (2,11)
        postBox_locs = [(15,11.5),(12,2.7),(4,8)]
        asteroid_locs = [(8.5,1),(9.3,5.4),(13.3,9.3)]
    elif levelNumber == 17:
        # scatter 4
        xmax = 16
        ymax = 12
        postShip_loc = (9,2)
        warpOut_loc  = (15,5)
        postBox_locs = [(3,11),(6.2,6),(10.5,7.4)]
        asteroid_locs = [(3.8,2),(4.5,4.2),(8.5,7.5),(10,5.7)]
    elif levelNumber == 18:
        # scatter 5
        xmax = 16
        ymax = 12
        postShip_loc = (2,2)
        warpOut_loc  = (15,1)
        postBox_locs = [(6.5,5),(6,7),(12,10.5)]
        asteroid_locs = [(5,2),(4,7),(10,6)]
    elif levelNumber == 19:
        # scatter 6
        xmax = 16
        ymax = 12
        postShip_loc = (8,6)
        warpOut_loc  = (8,11)
        postBox_locs = [(8,1),(3,4),(13,8)]
        asteroid_locs = [(1,4),(3,6),(13,6),(15,8)]
    elif levelNumber == 20:
        # gaps 1
        xmax = 16
        ymax = 12
        postShip_loc = (15,1)
        warpOut_loc  = (4,9)
        postBox_locs = [(3,4),(7,6.5),(12,10)]
        asteroid_locs = [(15.5,6),(10,0.5),(11,5)]
    elif levelNumber == 21:
        # gaps 2
        xmax = 16
        ymax = 12
        postShip_loc = (12,3.5)
        warpOut_loc  = (13,8.5)
        postBox_locs = [(6,3.5),(6,8.5),(3.5,6)]
        asteroid_locs = [(6,6),(2.5,2.5),(2.5,9.5)]
    elif levelNumber == 22:
        # gaps 3
        xmax = 16
        ymax = 12
        postShip_loc = (15,6)
        warpOut_loc  = (1,6)
        postBox_locs = [(4,6),(11,4),(11,9)]
        asteroid_locs = [(8,1.1),(8,3.6),(8,10.9),(8,8.4)]
    elif levelNumber == 23:
        # zoom 1
        xmax = 24
        ymax = 18
        postShip_loc = (22,16)
        warpOut_loc  = (2,2)
        postBox_locs = [(2.4,16),(7.2,16),(12,16),(16.8,16),(7.2,2),(12,2),(16.8,2),(21.6,2),(7.2,12.6),(12,9),(16.8,5.4)]
        asteroid_locs = []
    elif levelNumber == 24:
        # zoom 2
        xmax = 24
        ymax = 18
        postShip_loc = (2,16)
        warpOut_loc  = (22,2)
        postBox_locs = [(2,2),(22,16),(12,9)]
        asteroid_locs = [(12,12),(9,9.75),(12,6),(15,8.25)]
    elif levelNumber == 25:
        # gaps 2b
        xmax = 16
        ymax = 12
        postShip_loc = (3,3.5)
        warpOut_loc  = (13,3.5)
        postBox_locs = [(10.5,6),(8,8.5),(5.5,6)]
        asteroid_locs = [(8,6),(10.5,8.5),(5.5,8.5)]
    elif levelNumber == 26:
        # layers 1
        xmax = 16
        ymax = 12
        postShip_loc = (13,1)
        warpOut_loc  = (2,6)
        postBox_locs = [(8,6),(6,6),(10,6)]
        asteroid_locs = [(8,2.7),(6,2.7),(10,2.7),(8,9.3),(6,9.3),(10,9.3)]
    elif levelNumber == 27:
        # layers 2
        xmax = 16
        ymax = 12
        postShip_loc = (13,1)
        warpOut_loc  = (2,6)
        postBox_locs = [(8,6),(6,6),(10,6)]
        asteroid_locs = [(8,3.5),(6,3.5),(10,3.5),(8,8.5),(6,8.5),(10,8.5)]
    elif levelNumber == 28:
        # layers 3
        xmax = 16
        ymax = 12
        postShip_loc = (14,6)
        warpOut_loc  = (2,6)
        postBox_locs = [(8,3.7),(6,3.7),(10,3.7),(8,8.3),(6,8.3),(10,8.3)]
        asteroid_locs = [(8,6),(6,6),(10,6)]
    elif levelNumber == 29:
        # bowl
        xmax = 16
        ymax = 12
        postShip_loc = (2,2)
        warpOut_loc  = (14,2)
        postBox_locs = [(8,5.5),(7.5,6),(8.5,6)]
        asteroid_locs = [(7,2),(5,3),(4,5),(4,7),(5.5,8.5),(9,2),(11,3),(12,5),(12,7),(10.5,8.5)]
    elif levelNumber == 30:
        # on asteroids
        xmax = 16
        ymax = 12
        postShip_loc = (14.5,1.5)
        warpOut_loc  = (1.5,10.5)
        postBox_locs = [(3.42444, 1.32993), (4.10728, 8.55708), (9.38505, 6.00344), (12.15835, 9.32917)]
        asteroid_locs = [(2,1.8),(5.5,8),(10.5,5),(13.5,10)]
    ##elif levelNumber == 31:
        ### 
        ##xmax = 
        ##ymax = 
        ##postShip_loc = 
        ##warpOut_loc  = 
        ##postBox_locs = 
        ##asteroid_locs = 
            
    # return level
    return((xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc))

#------------------------------------------------------------
# STANDARD LEVELS
#------------------------------------------------------------

def standardLevel(levelNumber):
    # number of levels
    numLevelsMade = 0
    # check valid level
    assert 1 <= levelNumber and levelNumber <= numLevelsMade, 'requested standard level does not exist'
    
    # return level
    return((xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc))


#------------------------------------------------------------
# RACE LEVELS
#------------------------------------------------------------

def raceLevel(levelNumber):
    # number of levels
    numLevelsMade = 0
    # check valid level
    assert 1 <= levelNumber and levelNumber <= numLevelsMade, 'requested racing level does not exist'
    
    # return level
    return((xmax,ymax,postShip_loc,warpOut_loc,postBox_locs,asteroid_locs,text,text_loc))