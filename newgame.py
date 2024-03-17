#make this a csv file
locations_dict = [{"name":"A",
                   "desc": "the town hall",
                   "dests":["B", "C"],
                   "items":""},
                  {"name":"B",
                   "desc":"the crime scene",
                   "dests":["A"],
                   "items":"Knife"}
                  ]

#what's the point of this
class Map:    
    """Class for the map"""
    def __init__(self, locations):
        self.locations = locations

class Location:
    def __init__(self, name, desc, dests, items):
        self.name =  name
        self.desc = desc
        self.dests = dests
        self.items = items 
        
    def __str__(self):
        """Prints out the information for each location"""
        return "You are at {}. {}. You can go to {}.".format(str(self.name),
                                                             str(self.desc),
                                                             ', '.join(str(dest) for dest in self.dests)
                                                             )
    
locations = [Location(**location) for location in locations_dict]
#splits key value pairs from locations_dict to create location objects stored in the list locations

def get_loc(input):
    """Gets a location object for any name"""
    for location in locations:
        if location.name == input:
            return location
    #else
    return None

#player's starting location
START_LOC = get_loc("A")

class Player:
    """Class for the player. Stores the player's current location and inventory."""
        
    def __init__(self, inv, current_loc=START_LOC):
        self.inv = inv
        self.current_loc = current_loc
                
    # @property
    # def current_loc(self): 
    #     print("getting location")
    #     return self._current_loc
    
    # @current_loc.setter
    # def current_loc(self, new_loc):
    #     print("setting location")
    #     self._current_loc = new_loc
    
    def move(self, input_dest):
        """Changes the player's current_loc to the new location that they input."""

        if input_dest in self.current_loc.dests:
            new_loc = get_loc(input_dest)
            self.current_loc = new_loc
            print(player.current_loc)

        else:
            print("That is not a valid move.")
            

player = Player([])

#def get_loc(input):
   # """gets the location from locations list"""
   # for location in locations:
   #     if location.name == "":
   #         return location

   # return None

print(player.current_loc)
player.move("B")
if "B" in START_LOC.dests:
    print("yess valid")
print(player.current_loc)
