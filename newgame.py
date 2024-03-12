#player's starting location
START_LOC = "Town Hall"

#make this a csv file
locations_dict = [{"name":"Town Hall",
                   "desc": "the town hall",
                   "dirs":{"north": "Crime Scene", "down":"Basement"},
                   "items":""},
                  {"name":"Crime Scene",
                   "desc":"the crime scene",
                   "dirs":{"south": "Town"},
                   "items":"Knife"}
                  ]


#what's the point of this
class Map:    
    """Class for the map"""
    def __init__(self, locations):
        self.locations = locations


class Location:
    def __init__(self, name, desc, dirs, items):
        self.name =  name
        self.desc = desc
        self.dirs = dirs
        self.items = items 
        
    def __str__(self):
        """Prints out the information for each location"""
        return "You are at {}. {}".format(str(self.name), str(self.desc))

class Player:
    """Class for the player. Stores the player's current location and inventory."""
        
    def __init__(self, current_loc, inv):
        self.current_loc = current_loc
        self.inv = inv
        
    def move(self, current_loc, direction):
        """Changes the player's current_loc to the new location based on the direction that they input."""
        pass
    
player = Player(START_LOC, [])

locations = [Location(**location) for location in locations_dict]
#splits key value pairs from locations_dict to create location objects stored in the list locations

print(str(locations[0]))