"""
Author: Adithya
"""

from Dictionary import returnDict
from inputscreen import main
from outputscreen import gotoOutput
from Backend import sortList, filterFood
from Transport import mainTransport
from pathdisplay import main_path

#Loads dictionary (food database)
global dict_food
dict_food = returnDict()

#Function to get coordinates of user's end destination
def getEndCoords(tag):
    return dict_food[tag][len(dict_food[tag])-1]

#Main console
while True:
    
    #Get user's inputs in the form of a tuple, storing into inputVars
    #(int x-coord location, int y-coord location, str food preference, float min budget, float max budget)
    inputVars = main() 
    
    #If user presses top right X button in the input screen, program closes
    if inputVars == "QUIT":
        quit()
    
    inputTag = inputVars[2] #User's food preference
    
    #If user didn't leave food preference blank, capitalize first letter
    #Else, store as an empty string
    if inputTag:
        inputTag = inputTag.upper()
    else:
        inputTag = ""
    
    inputX = inputVars[0] #User's x-coord location
    inputY = inputVars[1] #User's y-coord location
    inputFloor = inputVars[3] #User's min budget
    inputCeiling = inputVars[4] #User's max budget
    
    #Backend operations
    can_dict = filterFood(dict_food, inputTag, inputFloor, inputCeiling) #Searches food database by user's food and price inputs, creates new dict can_dict
    sortedls = sortList(inputX, inputY, can_dict) #Sorts can_dict by nearest distance to user
    
    value = None
    
    while True:
        #After searching and sorting, show results on the output screen
        output = gotoOutput(inputTag, can_dict, sortedls)
        
        #If user presses top right X button in output screen, program closes
        if output == "QUIT":
            quit()
        
        #If user presses back button in output screen, go back to input screen and initialize variables
        elif output == -1:
            inputX = None
            inputY = None
            inputFloor = None
            inputCeiling = None
            inputTag = ""
            break

        else:
            start = (inputX, inputY) #Get user's current location as a tuple (x-coord, y-coord)
            end = tuple(getEndCoords(sortedls[output][0])) #Get user's end destination as a tuple (x-coord, y-coord)
            path = mainTransport(start, end) #Returns coordinates showing ideal transport route for user
            value = main_path(path, start, end) #Shows a graphic of this path on a new screen (transport screen)
        
        #If user presses back button in transport screen, go back to output screen
        if value == "BACK":
            continue
        
        #If user presses top right X button in transport screen, go back to output screen
        elif value == "QUIT":
            quit()