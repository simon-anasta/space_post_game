#!/usr/bin/python

#------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------

# External modules
import json
import os.path

# Internal modules
import config

#------------------------------------------------------------
# Functions

def reset():
    '''creates a new blank json object containing only default values'''
    # initialize
    data = {}
    data['easyControls'] = True
    
    # level records
    data['easyLevelRecords'] = []
    data['hardLevelRecords'] = []
    # fill with blank lists
    for i in range(config.numLevelsMade):
        data['easyLevelRecords'].append([])
        data['hardLevelRecords'].append([])
    
    # total number of deliveries attempted
    data['numAttempts'] = 0
    # total number of crashes
    data['numCrashes'] = 0
    # total number of lost in space
    data['numLost'] = 0
    # total number of early warp outs
    data['numEarly'] = 0
    # total number of deliveries complete
    data['numComplete'] = 0
    
    # return dataset
    return(data)

def loadJson():
    '''loads data file from JSON'''
    if os.path.isfile(config.dataLocation):
        # Read data back
        with open(config.dataLocation, 'r') as f:
            data = json.load(f)
    else:
        # create new blank JSON
        data = reset()
    # give back results
    return(data)

def saveJson(data):
    '''saves data file to JSON'''
    # Writing JSON data
    with open(config.dataLocation, 'w') as f:
        json.dump(data, f)

