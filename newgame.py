import tkinter as tk
from tkinter import *

# make this a csv file
# a list of dictionaries of locations
LOCATIONS_DICT = [
    {
        "name": "cell",
        "desc": "Your prison cell. It contains a sink, a toilet, your bed, a desk, and a chair. Your cell door is open and it leads to the prison hallway.",
        "dests": ["hallway"],
        "inspectables": {"sink": "The sink is made of stainless steel and has a leaky faucet.",
                         "bed": "Under the mattress, you find a crudely made steel crowbar. It is wide and thin, seemingly left behind by whoever previously lived in your cell.",
                         "desk": "It is a simple wooden table bolted to the walls.",
                         "chair": "The wooden chair is bolted to the floor."},
        "items": ["crowbar"]
    },
    {
        "name": "hallway",
        "desc": "A dimly lit hallway leading to different areas of the prison, as well as doors leading to other cells. You can see the cafeteria to the north and the workshop to the south. The door to your cell is to the west.",
        "dests": ["cafeteria", "workshop", "cell"],
        "inspectables": {"door": "You try the door to another inmate's cell, but it is locked."},
        "items": []
    },
    {
        "name": "cafeteria",
        "desc": "The prison cafeteria. To the east is a door leading to the courtyard, and the hallway is to the south. Directly to the north is the kitchen.",
        "dests": ["hallway", "yard"],
        "inspectables": {"bread": "A stale piece of bread.",
                         "soup": "Watery, tasteless soup.",
                         "meat": "A slimy piece of unidentifiable meat."},
        "items": ["bread", "meat"]
    },
    {
        "name": "yard",
        "desc": "An enclosed outdoor area surrounded by barbed wire, where inmates get their daily exercise. There is a passage leading to the cafeteria to the west.",
        "dests": ["cafeteria"],
        "inspectables": {},
        "items": []
    },
    {
        "name": "kitchen",
        "desc": "The kitchen is supervised by guards while inmates are working frantically, rushing to cook meals out for the others. There are rows of kitchen counters, along with multiple stoves and ovens. To the south, the cafeteria is directly connected.",
        "dests": ["cafeteria"],
        "inspectables": {"counter": "On the counter, there is an empty chopping board and a vegetable knife.", "stove": "Your average cooking stovetop.", "oven": "The ovens are filled with trays of food."},
        "items": ["knife", "chopping board"]
    },
    {
        "name": "workshop",
        "desc": "A noisy room full of labour. You can hear machinery sounds in the background as inmates work on projects under the supervision of guards. The hallway is to the north.",
        "dests": ["hallway"],
        "inspectables": {"machine": "Out of all the old, creaky machines, you notice welding machines, sewing machines, drills, and saws."},
        "items": ["drill", "saw"]
    }
]

# what's the point of this


class Map:
    """Class for the map"""

    def __init__(self, locations):
        self.locations = locations


class Location:
    """A class for locations. Stores location name, description, destinations, items."""

    def __init__(self, name, desc, dests, inspectables, items):
        self.name = name
        self.desc = desc
        self.dests = dests
        self.inspectables = inspectables
        self.items = items

    def __str__(self):
        """Returns a string containing the information for each location"""
        return f"You are at {str(self.name)}. \n{str(self.desc)} \nYou can go to {', '.join(str(dest) for dest in self.dests)}."


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
START_LOC = get_loc("cell")


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
        """Prints out more information about an item in the location."""
        if input_item in self.current_loc.inspectables:
            print(self.current_loc.inspectables[input_item])


player = Player([])

# ------------Tkinter stuff---------------------

# create tkinter window
root = tk.Tk()

# changes title of the window
root.title('⛓️👮 Prison Escape! 👮⛓️')

img = PhotoImage(file='siren.png')
root.iconphoto(True, img)

# changes size of the window
root.geometry('600x400')
root.resizable(True, True)

# create text widget and specify size
# min height is 1px so the textbox will fill remaining space in grid
main_text = Text(root, fg="blue", height=1, padx=10, pady=5)
# place at row0, sticky="nsew" makes it fill the whole grid
main_text.grid(row=0, column=0, sticky="nsew", columnspan=2)
# insert text that i want to display
main_text.insert('1.0', player.current_loc)
# user can't edit the text
main_text['state'] = 'disabled'

# create a vertical scrollbar for the text box next to it
text_scrollbar = Scrollbar(root, orient="vertical", command=main_text.yview)
# sticks the scrollbar to north and south of its grid
text_scrollbar.grid(row=0, column=2, sticky="ns")

# FIX the wording of the text

# configure the text widget to use the scrollbar
main_text.config(yscrollcommand=text_scrollbar.set)

# create frame around buttons
button_frame = tk.Frame(root, bg="light grey", padx=10, pady=10)
button_frame.grid(row=1, column=0, sticky="nsew")

# entry is a one line text input widget
entry = Entry(root, )
entry.grid(row=1, column=1, columnspan=2, sticky="ew")

# -----------------ratios/weights of grid---------
# keeps text row and buttons row the same ratio when resizing window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# gives the text column (column0) priority over the scrollbar column
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


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

    # makes buttons evenly sized in the frame
    rel_height = 1 / len(player.current_loc.dests)

    # for each destination,
    # enumerate returns (button number, destination)
    for i, dest in enumerate(player.current_loc.dests):
        # offset value for each button so they can stack on top of each other
        # for example, if there are 2 buttons, the first will be offset by 0.25,
        # and the second will be by 0.75, which positions them both with equal spacing
        rely_value = (i + 0.5) * rel_height
        sub_move_button = tk.Button(
            button_frame,
            text=f"move to {dest}",
            # dest=dest sets the variable before the loop repeats
            command=lambda dest=dest: tkinter_update_move(dest)
        )

        sub_move_button.place(relx=0.5, rely=rely_value,
                              relwidth=1, relheight=rel_height, anchor=CENTER)


def update_loc_text():
    """Adds new text to the main text box when the player moves."""
    main_text.config(state='normal')  # enables the text widget
    # inserts new text at end of old text with 2 new lines
    main_text.insert('end', '\n\n' + str(player.current_loc))
    main_text.see('end')  # scrolls to end of text box
    main_text.config(state='disabled')  # re-disables the text widget


def create_main_move_button():
    """Creates main move button"""
    main_move_button = tk.Button(
        button_frame,
        text='Move',
        # command = creates new buttons for each direction
        command=lambda: [clear_button_frame(), create_move_buttons()]
    )

    # main_move_button.place(relx=.5, rely=.5, anchor="c") #centres the move button in its grid
    main_move_button.pack(fill=BOTH, expand=True)


# creates main move button
create_main_move_button()

# keeps the tkinter window displaying
root.mainloop()
