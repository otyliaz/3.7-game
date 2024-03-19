# make this a csv file
# a list of dictionaries of locations
LOCATIONS_DICT = [{"name": "A",
                   "desc": "the town hall",
                   "dests": ["B", "C"],
                   "items": []},
                  {"name": "B",
                   "desc": "the crime scene",
                   "dests": ["A"],
                   "items": ["Knife"]}
                  ]

# what's the point of this


class Map:
    """Class for the map"""

    def __init__(self, locations):
        self.locations = locations


class Location:
    """A class for locations. Stores location name, description, destinations, items."""

    def __init__(self, name, desc, dests, items):
        self.name = name
        self.desc = desc
        self.dests = dests
        self.items = items

    def __str__(self):
        """Returns a string containing the information for each location"""
        return "You are at {}. {}. You can go to {}.".format(str(self.name),
                                                             str(self.desc),
                                                             ', '.join(
                                                                 str(dest) for dest in self.dests)
                                                             # joins destinations with a comma
                                                             )


locations = [Location(**location) for location in LOCATIONS_DICT]
# splits key value pairs from LOCATIONS_DICT to create location objects stored in the list locations


def get_loc(input_loc):
    """Gets a location object for the name of location"""
    for location in locations:
        if location.name == input_loc:
            return location
    # else
    return None


# player's starting location
START_LOC = get_loc("A")


class Player:
    """Class for the player. Stores the player's current location and inventory."""

    def __init__(self, inv, current_loc=START_LOC):
        # current_loc will be the starting location if not otherwise defined
        self.inv = inv
        self.current_loc = current_loc

    def move(self, input_dest):
        """Changes the player's current_loc to the new location that they input."""

        # if the destination that the player inputs is valid,
        if input_dest.upper() in self.current_loc.dests:
            # get new location object using get_loc
            new_loc = get_loc(input_dest)
            self.current_loc = new_loc
            print(player.current_loc)  # print description of location

        else:
            print("That is not a valid move.")

    def take(self, input_item):
        """If the input item matches an item in the location, 
        append the item to the player inventory and remove from location items"""
        if input_item in self.current_loc.items:
            player.inv.append(input_item)
            self.current_loc.items.remove(input_item)

    def inspect(self, input_item):
        """not take, but pick up and look closely"""
        pass


player = Player([])

# print(player.current_loc)
# player.move("B")
# print(player.current_loc)
# print(player.inv)
# player.take("Knife")
# print(player.inv)
# print(player.current_loc.items)
