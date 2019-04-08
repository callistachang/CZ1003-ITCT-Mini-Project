"""
Author: Adithya
"""

#To get the distance by Pythagoras' Theorem
def getDist(xu, yu, xd, yd):
    return ((xu-xd)**2 + (yu-yd)**2) ** (0.5)

#Search food by price and tag (linear search algorithm)
def filterFood(dict_food, tag, floor, ceiling):
    can = {}
    
    #If no food preference tag is inputted by user, linear search to find all types of food within the given price range 
    if not tag:
        for menu in dict_food:
            for food_detail in dict_food[menu]:
                if type(food_detail) == tuple: #Ignores co-ordinates stored as nested list
                    for food_tag in food_detail[2]:
                        if floor <= food_detail[1][1] and ceiling >= food_detail[1][0]:
                            if menu not in can:
                                can[menu] = [(food_detail[0], food_detail[1], dict_food[menu][len(dict_food[menu])-1])]
                            else:
                                can[menu].append((food_detail[0], food_detail[1], dict_food[menu][len(dict_food[menu])-1]))
                                
    #If food preference tag is inputted by user, search by tag and price range together 
    else:
        for menu in dict_food:
            for food_detail in dict_food[menu]:
                if type(food_detail) == tuple: #Ignores co-ordinates stored as nested list
                    for food_tag in food_detail[2]:
                        if tag == food_tag and floor <= food_detail[1][1] and ceiling >= food_detail[1][0]:
                            if menu not in can:
                                can[menu]= [(food_detail[0], food_detail[1], dict_food[menu][len(dict_food[menu])-1])]
                            else:
                                can[menu].append((food_detail[0], food_detail[1], dict_food[menu][len(dict_food[menu])-1]))
                                
    #Returns a Dictionary with stall name, price range, co-ordinates
    return can 

#After searching, results are sorted by distance (bubble sort algorithm)
def sortList(x, y, dic): 
    ls = []
    
    #Converts Dictionary to List so it can be sorted
    for i in dic: 
        ls.append((i, getDist(x, y, dic[i][0][2][0], dic[i][0][2][1])))
        
    #Uses BubbleSort
    for h in range(len(ls)-1, 0, -1):
        swap = 0
        for i in range (h):
            if ls[i][1] > ls[i+1][1]:
                x = ls[i]
                ls[i] = ls[i+1]
                ls[i+1] = x
                swap = 1
        if swap == 0: #no swaps means list is sorted
            break 
        
    return ls