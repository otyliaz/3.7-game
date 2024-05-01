"""This is my game for NCEA Level 3 Digital Technologies 3.7 91906 by OTYLIA ZENG
"""

import tkinter as tk
from tkinter import *

# make this a csv file
# a list of dictionaries of locations
LOCATIONS_DICT = [
    {"name": "cell",
        "desc": "You are in the prison cell assigned to you. It contains a sink, a toilet, your bed, a desk, and a chair. Your cell door is open and it leads to the dormitory.",
        "dests": ["dorm"],
        "inspectables": {"sink": "The sink is made of stainless steel and has a leaky faucet.",
                         "bed": "Under the thin mattress, you find a crudely made steel crowbar. It is wide and thin, seemingly left behind by whoever previously lived in your cell.",
                         "desk": "It is a simple wooden table bolted to the walls.",
                         "chair": "The wooden chair is bolted to the floor.",
                         "door": "You see nothing special about the door.",
                         "toilet": "The toilet is a standard porcelain toilet, its surface showing signs of heavy use and occasional cleaning."},
        "items": []  # adds crowbar when bed is inspected
     },
    {"name": "dorm",
        "desc": "You are in the dormitory, a large room with many doors leading to the rooms of other prisoners. The door to your cell is to the west and the main hallway is to the east.",
        "dests": ["cell", "hallway"],
        "inspectables": {"door": "You try the door to another inmate's cell, but it is locked."},
        "items": []
     },
    {
        "name": "hallway",
        "desc": "You are in the dimly lit hallway leading to different communal areas of the prison. You can see the cafeteria to the north and the workshop to the south. The dormitory is to the west.",
        "dests": ["dorm", "cafeteria", "workshop"],
        "inspectables": {},
        "items": []
    },
    {
        "name": "cafeteria",
        "desc": "You find yourself in the cafeteria. It is filled with people lining up to get their daily serving of food. You are served some unappetising bread, meat, and soup. To the east is a door leading to the courtyard, and the hallway is to the south. Directly to the north is the kitchen.",
        "dests": ["hallway", "kitchen", "yard"],
        "inspectables": {"bread": "A stale piece of bread.",
                         "soup": "Watery, tasteless soup.",
                         "meat": "A slimy piece of unidentifiable meat.",
                         "door": "You see nothing special about the door.",
                         "food": "You are served some unappetising bread, meat, and soup."},
        "items": ["bread", "meat"]
    },
    {
        "name": "yard",
        "desc": "You are in the courtyard, an enclosed outdoor area surrounded by a barbed wire fence where you can get your daily exercise. There are a group of inmates gathered around, gossiping. There is a passage leading to the cafeteria to the west.",
        "dests": ["cafeteria"],
        "inspectables": {"fence": "You notice a small hole under the fence, but it is a little bit too small for your body to fit through. There is a security guard watching over the prisoners."},
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
    },  # EDIT the items and inspect
    {
        "name": "workshop",
        "desc": "A noisy room full of labour. You can hear machinery sounds in the background as inmates work on projects under the supervision of guards. The hallway is to the north.",
        "dests": ["hallway"],
        "inspectables": {"machine": "Out of all the old, creaky machines, you notice welding machines, sewing machines, drills, and saws."},
        "items": ["drill", "saw"]
    }
]


class Location:
    """A class for locations. Stores location name, description, destinations, items."""

    def __init__(self, name, desc, dests, inspectables, items):
        self.name = name
        self.desc = desc
        self.dests = dests
        self.inspectables = inspectables
        self.items = items

    def __str__(self):
        """Returns a string containing the information for each location."""
        return f"You are in the {str(self.name)}. \n{str(self.desc)}"
    # \nYou can go to {', '.join(str(dest) for dest in self.dests)}.

    def inspect(self, input_item):
        """Prints out more information about an item in the location."""

        # if they inspect bed in the cell for the first time,
        if self.name == "cell" and input_item == "bed":
            if "bed" not in player.inspected_items:
                self.items.append("crowbar")

            if "crowbar" in player.inv:
                return "There is nothing else of interest about the bed."

        if input_item in self.inspectables:
            # adds input_item to the inspected set
            player.inspected_items.add(input_item)
            return self.inspectables[input_item]

        else:
            return "You can't inspect any such thing."


locations = [Location(**location) for location in LOCATIONS_DICT]
# splits key value pairs from LOCATIONS_DICT to create location objects stored in the list locations


def get_loc(input_loc):
    """Gets a location object for the name of location."""
    for location in locations:
        if location.name == input_loc:
            return location
    # else
    return None


# player's starting location
START_LOC = get_loc("cell")


class Player:
    """Class for the player. Stores the player's current location and inventory."""

    def __init__(self, inv, current_loc=START_LOC, inspected_items=set(), win=None):
        # current_loc will be the starting location if not otherwise defined
        # stores inspected items in a set -> items cannot be repeated
        # win variable will change to True or False if they win or lose
        self.inv = inv
        self.current_loc = current_loc
        self.inspected_items = inspected_items
        self.win = win
        self.bread_thrown = False

    def move(self, input_dest):
        """Changes the player's current_loc to the new location that they input."""

        # if the destination that the player inputs is valid,
        if input_dest in self.current_loc.dests:
            # get new location object using get_loc
            new_loc = get_loc(input_dest)
            self.current_loc = new_loc
            return self.current_loc  # return description of location

        else:
            return "That is not a valid move."

    def take(self, input_item):
        """If the input item matches an item in the location, append the item to the player inventory and remove from location items."""
        if input_item in self.inv:
            return "You already have this item!"

        if input_item in self.current_loc.items:
            self.inv.append(input_item)
            self.current_loc.items.remove(input_item)
            return f"You pick up the {input_item} and put it in your pocket."

        else:
            return "You can't take any such thing."

    def use(self, input_item):
        """Conditions for every item that can be used."""
        # don't need to check if item is in inventory because it will only show on gui if it is in inventory

        # if they are in the yard and have already inspected the fence,
        if self.current_loc.name == "yard" and "fence" in player.inspected_items:

            # they can throw the bread
            if input_item == "bread":
                self.bread_thrown = True
                self.inv.remove(input_item)  # removes item from inventory
                return "You throw the piece of bread at the gathering of people in the corner of the yard, causing a commotion amongst them. This attracts the guards, who go over to check out the fight. "

            if input_item == "crowbar":
                # if they use the crowbar after distracting the guard with bread, they win
                if self.bread_thrown == True:
                    self.win = True
                    return

                else:
                    # if they use the crowbar without distracting the guard, they lose
                    self.win = False
                    return

        return "You don't know how to use that item."


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
root.minsize(500, 400)
root.resizable(True, True)


def main():
    """Runs the game."""

    for widget in root.winfo_children():
        widget.destroy()

    main_text_frame = tk.Frame(root)
    main_text_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # create text widget and specify size
    # min height is 1px so the textbox will fill remaining space in grid
    main_text = Text(main_text_frame, fg="blue", height=1,
                     padx=10, pady=5, wrap="word")

    # create frame around move buttons
    move_frame = tk.Frame(root, bg="light grey", padx=10, pady=10)
    move_frame.grid(row=1, column=0, sticky="nsew", rowspan=2)

    # create a vertical scrollbar for the text box next to it
    text_scrollbar = Scrollbar(
        main_text_frame, orient="vertical", command=main_text.yview)

    # sticks the scrollbar to north and south of its grid
    text_scrollbar.pack(side=RIGHT, fill='y')

    # place at row0, sticky="nsew" makes it fill the whole grid
    main_text.pack(expand=True, fill=BOTH, side=LEFT)
    # insert text that i want to display
    main_text.insert('1.0', player.current_loc)
    # user can't edit the text
    main_text['state'] = 'disabled'

    # FIX the wording of the text

    # configure the text widget to use the scrollbar
    main_text.config(yscrollcommand=text_scrollbar.set)

    # create frame around entry input boxes
    entry_frame = tk.Frame(root)
    entry_frame.grid(row=1, column=1, pady=5, sticky="nswe")

    def inspect_action():
        """Updates the main text box when the player inspects something."""
        inspect_input = inspect_entry.get().lower()

        if inspect_input:
            update_text(player.current_loc.inspect(inspect_input))
        else:
            update_text("Please enter an item to inspect.")

        inspect_entry.delete(0, 'end')

    # entry is a one line text input widget
    inspect_entry = Entry(entry_frame, highlightbackground="black",
                          highlightthickness=1)
    inspect_entry.grid(row=0, column=0, sticky="ew", padx=5)

    inspect_btn = Button(entry_frame, text="Inspect!",
                         width=10, command=inspect_action)
    inspect_btn.grid(row=0, column=1, pady=1, padx=(0, 5))

    def take_action():
        """Updates the main text box and inventory when the player takes something."""
        take_input = take_entry.get().lower()

        if take_input:
            result = player.take(take_input)
            update_text(result)
            update_inv_display()
        else:
            update_text("Please enter an item to take.")

        take_entry.delete(0, 'end')

    # take_frame = tk.Frame(entry_frame)
    # take_frame.pack(fill=BOTH, padx=5)

    take_entry = Entry(entry_frame, highlightbackground="black",
                       highlightthickness=1)
    # take_entry.pack(side="left", fill=X, expand=True)
    take_entry.grid(row=1, column=0, sticky="ew", padx=5)

    take_btn = Button(entry_frame, text="Take!", width=10, command=take_action)
    # take_btn.pack(side="right", padx=(5, 0))
    take_btn.grid(row=1, column=1, pady=1, padx=(0, 5))

    entry_frame.grid_columnconfigure(0, weight=1)

    inv_frame = tk.Frame(root)
    inv_frame.grid(row=2, column=1, sticky="nswe")
    inv_frame.grid_propagate(False)

    inv_heading_label = Label(
        inv_frame, text="Click to Use an Item in Your Inventory:")
    inv_heading_label.grid(row=0, sticky="nwe")
# FIX HELP idk why the label is to the left
    inv_items_frame = tk.Frame(inv_frame)
    inv_items_frame.grid(row=1)

    def use_action(item):
        """Updates main text and inventory when the player uses an item."""

        result = player.use(item)

        if player.win == True:
            win_window()
            return

        if player.win == False:
            lose_window()
            return

        update_text(result)
        update_inv_display()

    def update_inv_display():
        """Updates inventory display when an item is used or taken."""

        for widget in inv_items_frame.winfo_children():
            widget.destroy()

        # for item in player.inv:
        #     item_button = Button(inv_items_frame, text=item.title(),
        #                          command=lambda item=item: use_action(item))
        #     item_button.pack(side=LEFT)

        for i, item in enumerate(player.inv):
            item_button = Button(inv_items_frame, text=item.title(),
                                 command=lambda item=item: use_action(item))
            item_button.grid(row=0, column=i, sticky="ns", padx=5)

    def clear_move_frame():
        """Clears the move button frame after a button is clicked."""
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
        """Moves player when button is clicked, adds new text, and replaces buttons."""
        player.move(dest)
        update_text(player.current_loc)
        clear_move_frame()
        create_main_move_button()

    def create_main_move_button():
        """Creates main move button"""
        main_move_button = tk.Button(
            move_frame,
            text='Move', width=20,
            # command = creates new buttons for each direction
            command=lambda: [clear_move_frame(), create_move_buttons()]
        )

        # main_move_button.place(relx=.5, rely=.5, anchor="c") #centres the move button in its grid
        main_move_button.pack(fill=BOTH, expand=True)

    def create_move_buttons():
        """"Makes separate buttons for each location. Runs after main move button is clicked."""

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
                text=f"Move to the {dest}",
                # dest=dest sets the variable before the loop repeats
                command=lambda dest=dest: tkinter_update_move(dest)
            )

            sub_move_button.place(relx=0.5, rely=rely_value,
                                  relwidth=1, relheight=rel_height, anchor=CENTER)

    # creates main move button
    create_main_move_button()

    # -----------------ratios/weights of grid---------
    # keeps text row and buttons row the same ratio when resizing window
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)

    # gives the text column (column0) priority over the scrollbar column
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    # -----------------------------------------------------------------


def start_window():
    """The starting screen."""

    description_label = tk.Label(
        root, text="Welcome to Prison Escape!\n\n"
        "You have been unjustfully imprisoned at the local prison with a life sentence."
        "\nExplore the prison and use anything around you to find your way out!",
        font=("Helvetica", 14), wraplength=500)
    description_label.place(relx=0.5, rely=0.3, anchor=CENTER)

    start_button = Button(root, text="PLAY NOW!", font=(
        "Helvetica", 14), bg="#4CAF50", fg="white", padx=10, pady=5, activebackground="#45a049", activeforeground="white", command=main)
    start_button.place(relx=0.5, rely=0.6, anchor=CENTER)


def win_window():
    """The win screen."""

    for widget in root.winfo_children():
        widget.destroy()

    win_label = tk.Label(
        root, text="Congratulations, You Win!", font=("Helvetica", 20), fg="green")
    win_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    win_text = tk.Label(
        root, text="You seize this moment to dig under the fence with your crowbar, enlargening the hole. "
        "After a few tense moments, you succeed, and with a final effort, you squeeze through to the other side. "
        "As you emerge into the night, you take a deep breath of freedom, feeling the cool air on your face for the first time in years. "
        "You are now a free person, ready to start a new chapter in your life. Well done, you win!", font=("Helvetica", 14), wraplength=400)
    win_text.place(relx=0.5, rely=0.6, anchor=CENTER)


def lose_window():
    """The lose screen"""

    for widget in root.winfo_children():
        widget.destroy()

    lose_label = tk.Label(
        root, text="Game Over, You Lose!", font=("Helvetica", 20), fg="red")
    lose_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    lose_text = tk.Label(
        root, text="You start to use your crowbar to dig at the hole under the fence. Unfortunately, the guard catches you trying to escape. He knocks you unconscious and drags you back to your cell. Better luck next time!", font=("Helvetica", 14), wraplength=400)
    lose_text.place(relx=0.5, rely=0.6, anchor=CENTER)

    # start_button = Button(root, text="Start the game!", command=game)
    # start_button.pack(anchor=CENTER, expand=True)


start_window()

# keeps the tkinter window displaying
root.mainloop()
