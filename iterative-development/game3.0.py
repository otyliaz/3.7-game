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
                         "chair": "The wooden chair is bolted to the floor.",
                         "door": "You see nothing special about the door."},
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
        "desc": "The prison cafeteria. It is filled with people lining up to get their daily serving of food. You are served some unappetising bread, meat, and soup. To the east is a door leading to the courtyard, and the hallway is to the south. Directly to the north is the kitchen.",
        "dests": ["hallway", "yard", "kitchen"],
        "inspectables": {"bread": "A stale piece of bread.",
                         "soup": "Watery, tasteless soup.",
                         "meat": "A slimy piece of unidentifiable meat.",
                         "door": "You see nothing special about the door.",
                         "food": "You are served some unappetising bread, meat, and soup."},
        "items": ["bread", "meat"]
    },
    {
        "name": "yard",
        "desc": "An enclosed outdoor area surrounded by a barbed wire fence, where inmates get their daily exercise. There are a group of inmates gathered around, talking. There is a passage leading to the cafeteria to the west.",
        "dests": ["cafeteria"],
        "inspectables": {"fence": "You notice a small hole under the fence, but it is a little bit too small for your body to fit through."},
        "items": []
    },
    {
        "name": "kitchen",
        "desc": "The kitchen is supervised by guards while inmates are working frantically, rushing to cook meals out for the others. There are rows of kitchen counters, along with multiple stoves and ovens. To the south, the cafeteria is directly connected.",
        "dests": ["cafeteria"],
        "inspectables": {"counter": "On the counter, there is an empty chopping board and a vegetable knife.",
                         "stove": "Your average cooking stovetop.",
                         "oven": "The ovens are filled with trays of food."},
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
        return f"You are at {str(self.name)}. \n{str(self.desc)}"
    # \nYou can go to {', '.join(str(dest) for dest in self.dests)}.


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
            return f"You pick up the {input_item} and put it in your pocket."

        else:
            return "You can't take any such thing."

    def inspect(self, input_item):
        """Prints out more information about an item in the location."""
        if input_item in self.current_loc.inspectables:
            return self.current_loc.inspectables[input_item]

        else:
            return f"You can't see any such thing."


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
main_text = Text(root, fg="blue", height=1, padx=10, pady=5, wrap="word")
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

# create frame around move buttons
move_frame = tk.Frame(root, bg="light grey", padx=10, pady=10)
move_frame.grid(row=1, column=0, sticky="nsew", rowspan=2)

# create frame around entry input boxes
entry_frame = tk.Frame(root)
entry_frame.grid(row=1, column=1, columnspan=2, sticky="new")


def inspect_action():
    """Updates the main text box when the player inspects something."""
    inspect_input = inspect_entry.get().lower()

    if inspect_input:
        update_text(player.inspect(inspect_input))
    else:
        update_text("Please enter an item to inspect.")

    inspect_entry.delete(0, 'end')


inspect_frame = tk.Frame(entry_frame)
inspect_frame.pack(side="top")

# entry is a one line text input widget
inspect_entry = Entry(inspect_frame)
inspect_entry.pack(side="left")

inspect_btn = Button(inspect_frame, text="Inspect!", command=inspect_action)
inspect_btn.pack(side="right")

# TODO inventory


def take_action():
    """Updates the main text box ***and inventory*** when the player takes something."""
    take_input = take_entry.get().lower()
    result = player.take(take_input)
    update_text(result)
    inv_text_update()
    take_entry.delete(0, 'end')


take_frame = tk.Frame(entry_frame)
take_frame.pack()

take_entry = Entry(take_frame)
take_entry.pack(side="left")

take_btn = Button(take_frame, text="Take!", command=take_action)
take_btn.pack(side="right")

inv_frame = tk.Frame(root)
inv_frame.grid(row=2, column=1, columnspan=2)

inv_heading_label = Label(inv_frame, text="Your Inventory:")
inv_heading_label.pack()

inv_text = Text(inv_frame, width=2, height=2,
                highlightthickness=0, borderwidth=0, bg="white", wrap="word")
inv_text.pack(fill='both')
inv_text.insert('1.0', """Your Inventory: """)


def inv_text_update():
    """Updates the inventory box when a new item is added"""
    inv_text.config(state="normal")
    inv_text.delete("1.0", "end")

    if player.inv:
        for item in player.inv:
            inv_text.insert(END, item.title() + "\n")
    else:
        inv_text.insert(END, "Your inventory is empty.")

    inv_text.config(state="disabled")


inv_text_update()
inv_text.config(state="disabled")

# -----------------ratios/weights of grid---------
# keeps text row and buttons row the same ratio when resizing window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=1)

# gives the text column (column0) priority over the scrollbar column
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


def clear_move_frame():
    """Clears the move button frame after a button is clicked"""
    for widget in move_frame.winfo_children():  # .winfo_children gets each children widget of the frame
        widget.destroy()


def update_text(new_string):
    """Adds new text to the main text box."""
    main_text.config(state='normal')  # enables the text widget
    # inserts new text at end of old text with 2 new lines
    main_text.insert('end', '\n\n' + str(new_string))
    main_text.see('end')  # scrolls to end of text box
    main_text.config(state='disabled')  # re-disables the text widget


def tkinter_update_move(dest):
    """Moves player when button is clicked, adds new text, and replaces buttons"""
    player.move(dest)
    update_text(player.current_loc)
    clear_move_frame()
    create_main_move_button()


def create_main_move_button():
    """Creates main move button"""
    main_move_button = tk.Button(
        move_frame,
        text='Move',
        # command = creates new buttons for each direction
        command=lambda: [clear_move_frame(), create_move_buttons()]
    )

    # main_move_button.place(relx=.5, rely=.5, anchor="c") #centres the move button in its grid
    main_move_button.pack(fill=BOTH, expand=True)


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
            move_frame,
            text=f"move to {dest}",
            # dest=dest sets the variable before the loop repeats
            command=lambda dest=dest: tkinter_update_move(dest)
        )

        sub_move_button.place(relx=0.5, rely=rely_value,
                              relwidth=1, relheight=rel_height, anchor=CENTER)


# creates main move button
create_main_move_button()

# keeps the tkinter window displaying
root.mainloop()
