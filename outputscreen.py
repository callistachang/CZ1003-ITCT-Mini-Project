"""
Author: Darshini
"""

import pygame

#Initialize screen 
display_width = 1450
display_height = 850
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('CZ1003 Project Output')

#Initialize variables 
black = (0, 0, 0)
blue = (0, 120, 255)
white = (255, 255, 255)
grey = (150, 150, 150)
green = (0, 255, 0)
yellow = (255, 255, 0)
darkgreen = (0, 150, 150)

#Return boolean for whether user clicked back button
def userClicksBack(coords):
    if 600 <= coords[0] <= 800 and 400 <= coords[1] <= 480:
        return True

#Creates a textbox 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#Import text font and display the messages
def message_display(text, centre_tuple, size):
    largeText = pygame.font.Font('fonts/Kingthings_Calligraphica_2.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = centre_tuple
    gameDisplay.blit(TextSurf, TextRect)
 
#Display top 5 results with each result option a button
def displayResults(can, sortedls):
    global buttons
    buttons = [None, None, None, None, None] #Buttons initialised as null, to be initialised as pygame objects if needed
    
    #Color of the display rectngle to alternate between grey and dark green
    for i in range(len(sortedls)):
        if i == 5:
            break
        if i % 2 == 0: #alternates colours
            colour = grey
        else:
            colour = darkgreen
            
        #Draw button for each result that is displayed
        buttons[i] = pygame.draw.rect(gameDisplay, colour, (50, 120*(i+1)+50, 500, 120))
        
        #Displays canteen info with distance calculated in the backend
        message1 = sortedls[i][0] + " | Distance: " + str(int(sortedls[i][1]))
        message_display(message1, (250+50, 120*(i+1)+12+50), 25)
        count = 1
        
        #For each result,top 3 food option and price is displayed
        for j in can[sortedls[i][0]]:
            if type(j) == tuple and count <= 3:
                message2 = j[0] + " | Price: $" + str(j[1][0]) + " to $" + str(j[1][1])
                message_display(message2, (250+50, 120*(i+1)+12+count*25+50), 20)
                count += 1

#Function to define the buttons
def gotoOutput(tag, can, sortedls):
    
    loop = True
    
    while loop:
        
        for event in pygame.event.get():
            
            #Checks if user clicks quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #Checks if user clicks back button
                if userClicksBack(event.pos):
                    return -1
                
                #Checks if user clicks on the results 
                #Main Console returns the transport page 
                if buttons[0] != None and buttons[0].collidepoint(event.pos):
                    return 0
                if buttons[1] != None and buttons[1].collidepoint(event.pos):
                    return 1
                if buttons[2] != None and buttons[2].collidepoint(event.pos):
                    return 2
                if buttons[3] != None and buttons[3].collidepoint(event.pos):
                    return 3
                if buttons[4] != None and buttons[4].collidepoint(event.pos):
                    return 4
        
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, yellow, (50, 50, 500, 120))
        
        #Display text 
        message_display("Your 5 Nearest Hangouts", (250+50, 30+50), 40)
        message_display("Click for Transport Options: " + tag, (250+50, 70+50), 30)
        pygame.draw.rect(gameDisplay, blue, (600, 400, 200, 80))
        message_display("BACK", (700, 440), 40)
        displayResults(can, sortedls)

        pygame.display.update()