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

    # def inspect(self, input_item):
    # """not take, but pick up and look closely"""
    # if input_item in self.current.loc.items:
    # pass
        # TODO this


player = Player([])

# ------------Tkinter stuff---------------------

# create tkinter window
root = tk.Tk()

# changes title of the window
root.title('Game Window')  # EDIT this

# changes size of the window
root.geometry('600x400')
root.resizable(True, True)

# create text widget and specify size
main_text = Text(root, fg="blue", height="1px")
# place at row0, sticky="nsew" makes it fill the whole grid
main_text.grid(row=0, column=0, sticky="nsew")
# insert text that i want to display
main_text.insert('1.0', player.current_loc)
# user can't edit the text
main_text['state'] = 'disabled'

# create a vertical scrollbar for the text box next to it
text_scrollbar = Scrollbar(root, orient="vertical", command=main_text.yview)
# sticks the scrollbar to north and south of its grid
text_scrollbar.grid(row=0, column=1, sticky="ns")

# configure the text widget to use the scrollbar
main_text.config(yscrollcommand=text_scrollbar.set)

# create frame around buttons
button_frame = tk.Frame(root, bg="light grey")
button_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# makes text row and buttons row the same ratio
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# gives the text column (column0) priority over the scrollbar column
root.grid_columnconfigure(0, weight=1)


def clear_button_frame():
    """Clears the button frame after a button is clicked"""
    for widget in button_frame.winfo_children():  # .winfo_children gets each children widget of the frame
        widget.destroy()


def tkinter_update_move(dest):
    """Moves player when button is clicked, adds new text, and replaces buttons"""
    player.move(dest)
    update_loc_text()
    clear_button_frame()
    create_main_move_button()


def create_move_buttons():
    """"Makes separate buttons for each location. Runs after main move button is clicked"""

    for dest in player.current_loc.dests:
        sub_move_button = ttk.Button(
            button_frame,
            text=f"move to {dest}",
            # dest=dest sets the variable before the loop repeats
            command=lambda dest=dest: tkinter_update_move(dest)
        )

        sub_move_button.pack()


def update_loc_text():
    """Adds new text to the main text box when the player moves."""
    main_text.config(state='normal')  # enables the text widget
    # inserts new text at end of old text with 2 new lines
    main_text.insert('end', '\n\n' + str(player.current_loc))
    main_text.see('end')  # scrolls to end of text box
    main_text.config(state='disabled')  # re-disables the text widget


def create_main_move_button():
    """Creates main move button"""
    main_move_button = ttk.Button(
        button_frame,
        text='Move',
        # command = creates new buttons for each direction
        command=lambda: [clear_button_frame(), create_move_buttons()]
    )

    main_move_button.pack(anchor="center")


# creates main move button
create_main_move_button()

# keeps the tkinter window displaying
root.mainloop()
