"""
Authors: Callista and Darshini
"""

import pygame as pg

#Information of variables used
bg_dimens = (1450, 850)
map_scaled_dimens = (900, 612) 
bg_color = (240, 240, 240)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
cyan = (0, 120, 255)

#Initialise pygame
pg.init()

#Import the text font in two different sizes 
largeText = pg.font.Font('fonts/Kingthings_Calligraphica_2.ttf', 40)
smallText = pg.font.Font('fonts/Kingthings_Calligraphica_2.ttf', 20)

def dist(x1,y1,x2,y2):
    return ((x1-x2) ** 2 + (y1-y2) ** 2) ** 0.5

#Draw a circle to mark the bus stops of the route taken
def draw_point(color, coords):
    pg.draw.circle(screen, color, coords, 10, 2)
    pg.draw.circle(screen, color, coords, 5)

#Draw points along transport route
def draw_path(path, start, end):
    global screen
    
    #Initialize background
    screen = pg.display.set_mode(bg_dimens)
    screen.fill(bg_color)
    
    #Display map
    map_img = pg.image.load('assets/ntu_campus.jpg')
    map_img = pg.transform.scale(map_img, map_scaled_dimens) 
    screen.blit(map_img, (0, 0))
    
    #Display back button
    pg.draw.rect(screen, cyan, (1000, 400, 200, 80))
    screen.blit(largeText.render("BACK", True, black), (1050, 420))
    
    #Display text at your start and end location   
    draw_point(black, start)
    screen.blit(smallText.render("<START>", True, black), (start[0], start[1]+10))
    draw_point(black, end)
    screen.blit(smallText.render("<END>", True, black), (end[0], end[1]+10))
    
    #Display which route to take
    if path[0] == 'BLUE':
        screen.blit(largeText.render("TAKE THE BLUE LINE", True, blue), (1000, 300))
    elif path[0] == 'RED':
        screen.blit(largeText.render("TAKE THE RED LINE", True, red), (1000, 300))
    elif path == 'WALK':
        screen.blit(largeText.render("WALK", True, black), (1050, 300))
    
    start_labelled = False
    end_labelled = False
    reversed_path = path[1][::-1]
    
    #Display bus stop points according to color (red/blue)
    if path[0] == 'BLUE':
        for i in range(len(path[1])):
            #Circle to mark bus stop is only printed out at the bus stops, not at dummy variable 
            if type(path[1][i][0]) == str:
                draw_point(blue, path[1][i][1])
                
                #labels walking guide from user's location to nearest bus stop
                #labels name of first bus stop for easier navigation
                if not start_labelled:
                    screen.blit(smallText.render(path[1][i][0], True, black), (path[1][i][1][0], path[1][i][1][1]))
                    pg.draw.line(screen, black, start, path[1][i][1], 2)
                    start_labelled = True
            
            #labels walking guide from final bus stop to user's destination
            #labels name of final bus stop for easier navigation
            if type(reversed_path[i][0]) == str and not end_labelled:
                screen.blit(smallText.render(reversed_path[i][0], True, black), (reversed_path[i][1][0], reversed_path[i][1][1]))
                pg.draw.line(screen, black, reversed_path[i][1], end, 2)
                end_labelled = True                
                
    elif path[0] == 'RED':
        for i in range(len(path[1])):
            if type(path[1][i][0]) == str:
                draw_point(red, path[1][i][1])
                if not start_labelled:
                    screen.blit(smallText.render(path[1][i][0], True, black), (path[1][i][1][0], path[1][i][1][1]))
                    pg.draw.line(screen, black, start, path[1][i][1], 2)
                    start_labelled = True
            
            if type(reversed_path[i][0]) == str and not end_labelled:
                screen.blit(smallText.render(reversed_path[i][0], True, black), (reversed_path[i][1][0], reversed_path[i][1][1]))
                pg.draw.line(screen, black, reversed_path[i][1], end, 2)
                end_labelled = True  

    #Line is drawn from start location to end location if walking           
    elif path == 'WALK':
        pg.draw.line(screen, black, start, end, 2)

    pg.display.update()

#Return boolean for whether user clicked back button
def userClicksBack(coords):
    if 1000 <= coords[0] <= 1200 and 400 <= coords[1] <= 480:
        return True

#main program
def main_path(path, start, end):
    
    loop = True
    draw_path(path, start, end)
    
    while loop:
        for event in pg.event.get():
            
            #Check whether user clicks quit
            if event.type == pg.QUIT:
                pg.quit()
                return "QUIT"
            
            #Check whether user clicks back 
            if event.type == pg.MOUSEBUTTONDOWN:
                if userClicksBack(event.pos):
                    return "BACK"