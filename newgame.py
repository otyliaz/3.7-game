import tkinter as tk
from tkinter import *
from tkinter import ttk

# make this a csv file
# a list of dictionaries of locations
LOCATIONS_DICT = [{"name": "A",
                   "desc": "the town hall",
                   "dests": ["B", "C"],
                   "items": []},
                  {"name": "B",
                   "desc": "the crime scene",
                   "dests": ["A"],
                   "items": ["Knife"]},
                  {"name": "C",
                   "desc": "another place",
                   "dests": ["B"],
                   "items": []}
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
        return f"You are at {str(self.name)}. \n{str(self.desc)}. \nYou can go to {', '.join(str(dest) for dest in self.dests)}."


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
        if input_dest in self.current_loc.dests:
            # get new location object using get_loc
            new_loc = get_loc(input_dest)
            self.current_loc = new_loc
            return player.current_loc  # return description of location

        else:
            return "That is not a valid move."

    def take(self, input_item):
        """If the input item matches an item in the location, 
        append the item to the player inventory and remove from location items"""
        if input_item in self.current_loc.items:
            player.inv.append(input_item)
            self.current_loc.items.remove(input_item)

    def inspect(self, input_item):
        """not take, but pick up and look closely"""
        if input_item in self.current.loc.items:
            pass
        # TODO this


player = Player([])

# ------------Tkinter stuff---------------------

# create tkinter window
root = tk.Tk()

# changes title of the window
root.title('Game Window')

# changes size of the window
root.geometry('600x400')
root.resizable(False, False)

# create text widget and specify size
main_text = Text(root, height=10, width=52, fg="blue")
main_text.pack()
# insert text that i want to display
main_text.insert('1.0', player.current_loc)
# user can't edit the text
main_text['state'] = 'disabled'

button_frame = tk.Frame(root, highlightbackground="green",
                        bg="blue", width=200, height=200)
button_frame.pack()

# ADD need to make a frame that has all the buttons in it so i can frame.clear() each time to clear the previous buttons
# frame that has the text and the buttons. widget for text at top and frame for buttons under the text.
# should use grid instead pack


def move_button():
    """"Makes separate buttons for each location. Runs after main move button is clicked"""

    for dest in player.current_loc.dests:
        go_button = ttk.Button(
            button_frame,
            text=f"move to {dest}",
            # dest=dest sets the variable before the loop repeats
            command=lambda dest=dest: [player.move(dest), update_loc_text()]
        )

        go_button.pack()


def update_loc_text():
    main_text.config(state='normal')  # enables the text widget
    # inserts new text at end of old text with 2 new lines
    main_text.insert('end', '\n\n' + str(player.current_loc))


# button for main move
move_button = ttk.Button(
    button_frame,
    text='Move',
    command=move_button  # command = creates new buttons for each direction
)
move_button.pack()

# keeps the tkinter window displaying
root.mainloop()
