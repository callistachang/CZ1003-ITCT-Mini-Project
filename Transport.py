"""
Authors: Darshini and Adithya
"""

#Coordinates of all bus stops of NTU red and blue line
global red_stops, blue_stops

                    #Bus stop / Waypoint Label     Coordinates
red_stops=[         ("Hall 16"   ,                 (432,97)),
                    ("Hall 14"   ,                 (514,102)),
                    ("Tamarind"  ,                 (620,112)),
                    #Dummy waypoints given to ensure that the distance calculated goes along the actual bus route and not cut across buildings
                    (1           ,                 (746,212)),
                    ("Hall 11"   ,                 (694,210)),
                    ("Hall 8"    ,                 (569,261)),
                    (2           ,                 (494,290)),
                    ("Hall 2"    ,                 (502,329)),
                    ("Hall 1"    ,                 (464,478)),
                    (3           ,                 (458,527)),
                    ("Hall 4"    ,                 (347,501)),
                    (4           ,                 (288,441)),
                    ("Innovation Centre",          (164,489)),
                    ("Hall 7"    ,                 (115,467)),
                    (5           ,                 (52,392)),
                    ("EEE"       ,                 (105,335)),
                    ("SBS"       ,                 (208,202)),
                    ("North Spine",                (313,204)),
                    (6           ,                 (385,220)),
                    (7           ,                 (381,100))]

blue_stops =  [     ( 9,                         (494,289)),
                    ("Hall 6",                   (493,390)),
                    (1,                          (465,483)),
                    ("Opp. Hall 5",              (408,518)),
                    ( 2,                         (290,444)),
                    ("Opp. Innovation Centre",   (240,461)),
                    (3,                          (161,488)),
                    ("School of SPMS",           (165,437)),
                    ( 4,                         (106,381)),
                    ("Opp. WKWSCI",              (103,338)),
                    ("Opp. CEE",                 (194,205)),
                    ( 5,                         (229,172)), 
                    ("Opp. Lee Wee Nam",         (313,202)),
                    (6,                          (378,221)),
                    ("Opp. Hall 3",              (386,167)),
                    ( 7,                         (382,98)),
                    ("Opp. Hall 14",             (431,94)),
                    ("Opp. Hall 23",             (638,115)),
                    ( 8,                         (745,209)),      
                    ("Opp. Hall 10",             (697,213)),
                    ("Opp. Hall 8",              (572,263))]

#To reverse the order of the blue bus stops. Allows the same function to be used for blue and red bus routes
blue_stops = blue_stops[::-1]

#Pythagoras' theorem: sqrt((x1-x2)^2+(y1-y2)^2)
def dist(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5

#Find the nearest bus stop to your current location
def find_nearest(bus_list, coords):
    
    #The first bus stop is assumed to be the nearest bus stop and linear search is done
    nearest = bus_list[0]
    for i in bus_list:
        prev = dist(nearest[1][0], nearest[1][1], coords[0], coords[1])
        
        #String check to ignore the dummy variable where the bus does not stop
        if type(i[0]) == str and dist(i[1][0], i[1][1], coords[0], coords[1]) < prev:
            nearest = i
            
    return nearest

#Return the list of bus stops from your nearest bus stop to the nearest bus stop of the destination
def pathDist(bus_list, start, end):
    
    #Return bus stop nearest to you
    stop1 = find_nearest(bus_list, start)
    stop2 = find_nearest(bus_list, end)
    
    #Return bus stop nearest to the canteen 
    i = bus_list.index(stop1)
    j = bus_list.index(stop2)
    
    #Path of the bus route start from your nearest bus stop
    path = [stop1]
    pathdist = 0
    
    #As long as the bus stop in the route is not the same as the last bus stop, the bus route list is appended
    while i % len(bus_list) != j:
        i -= 1
        path.append(bus_list[i])
        
    #Distance is computed and added to the the total distance
    for k in range(0, len(path)-1):
        pathdist += dist(path[k][1][0], path[k][1][1], path[k+1][1][0], path[k+1][1][1])
    return path, pathdist

#Route and distance for both lists are printed out and compared. 
def mainTransport(start, end):
    red_route, red_dist = pathDist(red_stops, start, end)
    blue_route, blue_dist = pathDist(blue_stops, start, end)
    
    #Route with a shorter distance is returned
    if blue_dist <= red_dist and len(blue_route) > 1:
        return "BLUE", blue_route, blue_dist
    elif red_dist <= blue_dist and len(red_route) > 1:
        return "RED", red_route, red_dist
    else:
        return "WALK"