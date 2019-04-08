"""
Author: Callista
"""

import pygame as pg
import pickle
import collections
import os.path

###################################
# VARIABLES STORING INFORMATION
###################################

#tuples storing dimensions
bg_dimens = (1450, 850)
box_dimens = (400, 40)
btn1_dimens = (150, 50)
btn2_dimens = (380, 50)
map_scaled_dimens = (900, 612) 
pointer_scaled_dimens = (31, 49)

#tuples storing RGB values
bg_color = (240, 240, 240)
box_color = (210, 210, 210)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)

#tuples storing box/button coordinates
food_box_coords = (950, 70)
floor_box_coords = (950, 160)
ceiling_box_coords = (950, 250)
submit_btn_coords = (950, 540)
reset_btn_coords = (1150, 540)
suggest_btn_coords = (30, 705)
history_btn_coords = (30, 765)

#tuples storing text coordinates
food_text_coords = (950, 40)
floor_text_coords = (950, 130)
ceiling_text_coords = (950, 220)
submit_text_coords = (985, 555)
reset_text_coords = (1185, 555)
suggest_text_coords = (40, 720)
history_text_coords = (40, 780)

#lists storing multiple tuples of text coordinates
box_coords_list = [food_text_coords, floor_text_coords, ceiling_text_coords, submit_text_coords, 
                   reset_text_coords, suggest_text_coords, history_text_coords]
instr_coords_list = [(950, y_coord) for y_coord in range(320, 320+30*7, 30)]

#list of types of food present in our database
food_tags = ["western", "chinese", "malay", "korean", "indian", "japanese", "thai", "halal", 
             "fast food", "snacks", "beverages", "chicken rice", "noodles", "mixed rice"]

#################################
# FUNCTIONS FOR READABILITY
#################################

#a function that creates text boxes
def display_text(message, coords, font, color):
    screen.blit(font.render(message, True, color), coords)

#a function that creates input boxes and buttons
def display_box(coords, dimens):
    return pg.draw.rect(screen, box_color, (coords, dimens))

#a function that returns where the user clicks
def user_click(coords):
    if 0 <= coords[0] <= map_scaled_dimens[0] and 0 <= coords[1] <= map_scaled_dimens[1]:
        return 'map'
    if food_input_box.collidepoint(coords):
        return 'food input'
    if floor_input_box.collidepoint(coords):
        return 'floor price input'
    if ceiling_input_box.collidepoint(coords):
        return 'ceiling price input'
    if submit_btn.collidepoint(coords):
        return 'submit'
    if reset_btn.collidepoint(coords):
        return 'reset'
    if suggest_btn.collidepoint(coords):
        return 'suggest'
    if history_btn.collidepoint(coords):
        return 'show history'
        
#a function that (re)initializes variables storing user's inputs
def initialize_user_input():
    global user_pos, food_user_input, floor_user_input, ceiling_user_input
    
    user_pos = None
    food_user_input = None
    floor_user_input = None
    ceiling_user_input = None

##############################################################################
# FUNCTIONS FOR PICKLING/RECORDING PAST USER INPUTS (AUTO-SUGGESTION FEATURE)
##############################################################################

def read_save_file():
    #if savefile.out (backup file storing user's past inputs) didn't exist, create a new one
    if os.path.isfile("savefile.out") == False:
        history_list = []
        save_file = open("savefile.out", "wb")
        pickle.dump(history_list, save_file)
        save_file.close()
    save_file = open("savefile.out", "rb")
    history_list = pickle.load(save_file)
    save_file.close()
    return history_list

def write_save_file(list):
    save_file = open("savefile.out", "wb")
    pickle.dump(list, save_file)
    save_file.close()
    
#upon submission of inputs, the user's inputs are stored into savefile.out
def save_user_input(choice_tuple):
    history_list = read_save_file()
    history_list.insert(0, choice_tuple) #appends the user's choice onto the beginning of the list
    write_save_file(history_list)

#suggests food, floor price input and ceiling price input based on user's past 10 inputs
def display_suggestions():
    global taking_user_input, food_user_input, floor_user_input, ceiling_user_input
    
    history_list = read_save_file()
    taking_user_input = False
    
    #suggestion is made only based off the last 10 choices the user made
    if len(history_list) > 10:
        history_list = history_list[:10]
    
    #if user didn't leave the input boxes for food/floor price/ceiling price blank (prevents the skew of suggestions);
    #put the data in 3 separate lists respectively
    past_food_inputs_list = [user_input[2] for user_input in history_list if user_input[2]]
    past_floor_inputs_list = [user_input[3] for user_input in history_list if user_input[3] != -1]
    past_ceiling_inputs_list = [user_input[4] for user_input in history_list if user_input[4] != 10000]
    
    #displays the most common food preference out of the user's past choices
    try:
        food_user_input = collections.Counter(past_food_inputs_list).most_common(1)[0][0]
        display_user_input(food_box_coords, food_user_input)
    except IndexError:
        pass
    
    #displays the average floor price inputs out of the user's past choices
    try: 
        floor_user_input = str(round(sum(past_floor_inputs_list) / len(past_floor_inputs_list), 2))
        display_user_input(floor_box_coords, floor_user_input)
    except ZeroDivisionError:
        pass
    
    #displays the average ceiling price inputs out of the user's past choices
    try:
        ceiling_user_input = str(round(sum(past_ceiling_inputs_list) / len(past_ceiling_inputs_list), 2))
        if floor_user_input and floor_user_input > ceiling_user_input: #makes sure that avg ceiling price can't be less than avg floor price
            ceiling_user_input = floor_user_input
        display_user_input(ceiling_box_coords, ceiling_user_input)
    except ZeroDivisionError:
        pass

#displays the user's past 5 submitted choices on the screen
def show_history():
    history_list = read_save_file()
    
    #only the last 5 user choices will be shown
    if len(history_list) > 5:
        history_list = history_list[:5]
        
    #coordinates where the text will be displayed on the screen
    history_coords_list = [(430, y_coord) for y_coord in range(720, 720+20*5, 20)]

    #converting all of the user's inputs into string data types so they can be displayed
    history_str_list = [[str(i) for i in user_input] for user_input in history_list]
    
    #displaying past 5 choices on the screen, formatted using f-string
    display_text("(DISPLAYING YOUR LAST FIVE CHOICES MADE)", (430, 690), small_font, BLACK)
    for j in range(len(history_list)):
        choice = f'{j+1}. Coordinates: ({history_str_list[j][0]}, {history_str_list[j][1]}), Food type: {history_str_list[j][2].capitalize()},  Budget: {history_str_list[j][3]}-{history_str_list[j][4]}'
        display_text(choice, history_coords_list[j], small_font, BLACK)

############################################
# FUNCTION TO INITIALIZE SCREEN/STATIC GUI
############################################

def initialize_screen():
    global screen, map_img, food_input_box, floor_input_box, ceiling_input_box, submit_btn, reset_btn, suggest_btn, history_btn
    
    #initializes the background screen
    screen = pg.display.set_mode(bg_dimens)
    screen.fill(bg_color)
    
    #displays the title of program at top left
    pg.display.set_caption("CZ1003 Mini Project (Adithya, Darshini, Callista)")
    
    #displays the NTU map on the screen (scaled down)
    map_img = pg.image.load('assets/ntu_campus.jpg')
    map_img = pg.transform.scale(map_img, map_scaled_dimens) 
    screen.blit(map_img, (0, 0))
    
    #displays input boxes and buttons on the screen
    food_input_box = display_box(food_box_coords, box_dimens)
    floor_input_box = display_box(floor_box_coords, box_dimens)
    ceiling_input_box = display_box(ceiling_box_coords, box_dimens)
    submit_btn = display_box(submit_btn_coords, btn1_dimens)
    reset_btn = display_box(reset_btn_coords, btn1_dimens)
    suggest_btn = display_box(suggest_btn_coords, btn2_dimens)
    history_btn = display_box(history_btn_coords, btn2_dimens)
    
    #text to be displayed on screen
    box_text_list = ["What type of food would you like to eat?", "Your minimum budget:", "Your maximum budget:",
                     "Submit", "Reset", "Auto-input based on past 10 choices", "Display last 5 choices made"]
    instr_text_list = ["Instructions:",
                       "- Click on the MAP to indicate where you are currently.",
                       "- Click on the BOXES to type in your input.",
                       "   Press ENTER to finalize your input. (Input turns green)",
                       "   Once you are done, click the SUBMIT button.",
                       "- You must AT LEAST indicate your LOCATION on the map.",
                       "   Other fields are not necessary."]
    
    #displays all the strings in box_text_list and instr_text_list
    for i in range(len(box_text_list)): 
        display_text(box_text_list[i], box_coords_list[i], big_font, BLACK)
    for j in range(len(instr_text_list)): 
        display_text(instr_text_list[j], instr_coords_list[j], small_font, BLACK)
    
    #other helpful messages to be displayed on the screen
    display_text("(ERROR OUTPUT MESSAGES, IF ANY)", (950, 615), small_font, BLACK)
    display_text("(POSSIBLE INPUT CATEGORIES)", (20, 630), small_font, BLACK)
    display_text(', '.join(food_tags), (20, 660), small_font, BLACK)

    pg.display.update()

##############################################
# FUNCTIONS TO MAKE GUI DYNAMIC/INTERACTIVE
##############################################
    
def get_user_location(pos):
    #reinitializes map in case user reclicks on the map at a new location (to erase the prev pointer icon)
    screen.blit(map_img, (0, 0))
    
    #displays user coordinates on the top left display screen, formatted using f-string
    display_text(f'User Co-Ordinates: {pos}', (10, 10), big_font, BLACK)
    
    #displays pointer icon on the map (scaled down)
    pointer_img = pg.image.load('assets/pointer_icon.png') 
    pointer_img = pg.transform.scale(pointer_img, pointer_scaled_dimens)
    
    #user click coordinates are adjusted to correspond with tip of pointer icon
    adjusted_coords = (pos[0]-pointer_scaled_dimens[0]/2, pos[1]-pointer_scaled_dimens[1])
    screen.blit(pointer_img, adjusted_coords)
    
#gets and displays user's text inputs from the GUI (in real time as the user types)
def display_user_input(coords, message):
    global taking_user_input
    
    event = pg.event.poll()
    
    #allows the user to close the program [even though the user hasn't finalized his input/broke from the loop]
    if event.type == pg.QUIT:
        pg.quit()
    
    if event.type == pg.KEYDOWN:
        key = event.key
        
        #if the user presses backspace, the last character he typed is deleted
        if key == pg.K_BACKSPACE:
            message = message[:-1]
            
        #if the user presses enter, his input is finalized
        elif key == pg.K_RETURN:
            taking_user_input = False
            
        #if the user enters an input too long for the text box (35 characters), no more characters can be added
        elif len(message) > 35:
            return message
        
        #if the user presses on an alphanumeric/apostrophe/space/hyphen key, the character is added on to the user's input
        elif pg.K_0 <= key <= pg.K_9 or pg.K_a <= key <= pg.K_z or key in [pg.K_QUOTE, pg.K_SPACE, pg.K_MINUS, pg.K_PERIOD]:
            message += chr(key)
            
        #if the user presses any other invalid key (e.g. Ctrl key), nothing happens
        else:
            return message
    
    #reinitializes the input box to prevent text overlap in the GUI after backspacing and typing again
    display_box(coords, box_dimens)
    
    #displays the user's message key by key on the box; if the user has finalized his input, the text turns from black to green, loop ends
    if taking_user_input:
        display_text(message + "|", coords, big_font, BLACK)
    else:
        display_text(message, coords, big_font, GREEN)

    pg.display.update()
    
    return message

#input error handling
def run_error_checks():
    global user_pos, food_user_input, floor_user_input, ceiling_user_input
    
    initialize_screen()
    pass_error_checks = True
    error_coords_list = [(950, y_coord) for y_coord in range(645, 645+30*5, 30)]

    #if user didn't indicate his current location, show error message
    if user_pos == None:
        display_text("[!] You must click on the map to indicate where you are currently.", error_coords_list[0], small_font, RED)
        pg.display.update()
        pass_error_checks = False
    
    #if user didn't leave preferred food choice blank;
    #check if he inputted a type of food that exists in the database, else show error message
    if food_user_input and food_user_input not in food_tags:
        display_text("[!] No such type of food exists in our database.", error_coords_list[1], small_font, RED)
        pg.display.update()
        pass_error_checks = False
    
    #if user didn't leave floor/ceiling price inputs blank;
    #check if he inputted a valid data type (int/float), else show error message
    if floor_user_input:
        try:
            floor_user_input = float(floor_user_input)
        except ValueError:
            display_text("[!] Please enter an integer/float as your min budget value.", error_coords_list[2], small_font, RED)
            pg.display.update()
            pass_error_checks = False
    if ceiling_user_input:
        try:
            ceiling_user_input = float(ceiling_user_input)
        except ValueError:
            display_text("[!] Please enter an integer/float as your max budget value.", error_coords_list[3], small_font, RED)
            pg.display.update()
            pass_error_checks = False
    
    #if user's floor price input is greater than the ceiling price input, show error message
    if isinstance(floor_user_input, float) and isinstance(ceiling_user_input, float) and floor_user_input > ceiling_user_input:
        display_text("[!] Your min budget cannot be larger than your max budget.", error_coords_list[4], small_font, RED)
        pg.display.update()
        pass_error_checks = False
    
    #if user left food/ceiling price inputs blank;
    #set default values for floor/ceiling price inputs
    if not floor_user_input:
        floor_user_input = -1.0
    if not ceiling_user_input:
        ceiling_user_input = 10000.0
    
    #if user passes all error checks;
    #the function all of his inputs as a tuple to be processed by the backend code and outputted on the output screen;
    #else reset all of his inputs to None since he has to retry typing in new valid inputs
    if pass_error_checks:
        user_input_tuple = (user_pos[0], user_pos[1], food_user_input, floor_user_input, ceiling_user_input)
        save_user_input(user_input_tuple)
        return user_input_tuple
    else:
        initialize_user_input()

#a function that records any user interaction with the screen, making the GUI dynamic & interactive
#ultimately returns user's input location/food preference/floor price budget/ceiling price budget, which will be passed to the backend
def interactive_interface():
    global taking_user_input, user_pos, food_user_input, floor_user_input, ceiling_user_input
    
    while True:
        
        for event in pg.event.get():
    
            #closes the program if you click the top-right 'X'
            if event.type == pg.QUIT:
                pg.quit()
                return "QUIT"
    
            elif event.type == pg.MOUSEBUTTONDOWN:
                
                taking_user_input = True
                user_input = ""
                
                #displays user coordinates and pointer icon if user clicks anywhere on the map
                if user_click(event.pos) == 'map':
                    user_pos = event.pos
                    get_user_location(user_pos)
                
                #if user clicks on the food/floor price/ceiling price input boxes, he can start typing his input
                elif user_click(event.pos) == 'food input':
                    while taking_user_input:
                        user_input = display_user_input(food_box_coords, user_input)
                    food_user_input = user_input
                    
                elif user_click(event.pos) == 'floor price input':
                    while taking_user_input:
                        user_input = display_user_input(floor_box_coords, user_input)
                    floor_user_input = user_input
                    
                elif user_click(event.pos) == 'ceiling price input':
                    while taking_user_input:
                        user_input = display_user_input(ceiling_box_coords, user_input)
                    ceiling_user_input = user_input
                    
                #if the user clicks the reset button, the screen and input variables will be reinitialized
                elif user_click(event.pos) == 'reset':
                    initialize_screen()
                    initialize_user_input()
                
                #displays suggestions based on past 10 records stored in savefile.out
                elif user_click(event.pos) == 'suggest':
                    display_suggestions()
                
                #displays last 5 choices from savefile.out
                elif user_click(event.pos) == 'show history':
                    show_history()

                #submits after running error checks
                elif user_click(event.pos) == 'submit':
                    pass_error_checks = run_error_checks()
                    
                    if pass_error_checks:
                        user_input_tuple = (user_pos[0], user_pos[1], food_user_input, floor_user_input, ceiling_user_input)
                        save_user_input(user_input_tuple)
                        return user_input_tuple
                    
                    else:
                        initialize_user_input()
                    
                pg.display.update()

#####################
# MAIN PROGRAM
#####################

def main():
    global big_font, small_font
    
    pg.init()
    big_font = big_font = pg.font.SysFont('fonts/freesandbold.ttf', 30)
    small_font = pg.font.SysFont('fonts/freesandbold.ttf', 22)
    
    initialize_user_input()
    initialize_screen()
    
    output = interactive_interface()
    
    return output

#[DEBUGGING] runs the main function whenever the user runs program straight from inputscreen.py, prints out user_input_tuple
if __name__ == '__main__':
    while True:
        print(main())