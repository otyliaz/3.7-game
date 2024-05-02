"""This is my game for NCEA Level 3 Digital Technologies 3.7 91906 by OTYLIA ZENG.
"""

import tkinter as tk

# a list of dictionaries of locations
LOCATIONS_DICT = [
    {"name": "cell",
        "desc": "You are in the prison cell assigned to you.\nIt contains a sink, a toilet, your bed, a desk, and a chair.\nYour cell door is open to the east, and it leads to the dormitory.",
        "dests": ["dormitory"],
        "inspectables": {"sink": "The sink is made of stainless steel and has a leaky faucet.",
                         "bed": "Under the thin mattress, you find a crudely made steel crowbar. It is wide and thin, seemingly left behind by whoever previously lived in your cell.",
                         "desk": "It is a simple wooden table bolted to the walls.",
                         "chair": "The wooden chair is bolted to the floor.",
                         "door": "You see nothing special about the door.",
                         "toilet": "The toilet is a standard porcelain toilet, its surface showing signs of heavy use and occasional cleaning."},
        "items": []  # adds crowbar when bed is inspected
     },
    {"name": "dormitory",
        "desc": "You are in the dormitory.\nIt is a large room with many doors leading to the rooms of other prisoners.\nThe door to your cell is to the west and the main hallway is to the east.",
        "dests": ["cell", "hallway"],
        "inspectables": {"door": "You try the door to another inmate's cell, but it is locked."},
        "items": []
     },
    {
        "name": "hallway",
        "desc": "You are in the hallway.\nIt is a dimly lit hallway leading to different communal areas of the prison.\nYou can see the cafeteria to the north and the workshop to the south. The dormitory is to the west.",
        "dests": ["dormitory", "cafeteria", "workshop"],
        "inspectables": {},
        "items": []
    },
    {
        "name": "cafeteria",
        "desc": "You are in the cafeteria.\nIt is filled with people lining up to get their daily serving of food. You are served some unappetising bread, meat, and soup.\nTo the east is a door leading to the courtyard, and the hallway is to the south. Directly to the north is the kitchen.",
        "dests": ["hallway", "kitchen", "courtyard"],
        "inspectables": {"bread": "The bread is stale and hard. However, it isn't hard enough to injure anyone.",
                         "soup": "The soup is watery and tasteless.",
                         "meat": "You pick up the slimy piece of unidentifiable meat, and put it back down.",
                         "door": "You see nothing special about the door.",
                         "food": "You are served some unappetising bread, meat, and soup."},
        "items": ["bread", "meat"]
    },
    {
        "name": "courtyard",
        "desc": "You are in the courtyard.\nIt is an enclosed outdoor area surrounded by a fence, where you get your daily exercise. There are a group of inmates gathered around, gossiping. There is a security guard watching sharply over the prisoners.\nThere is a passage leading to the cafeteria to the west.",
        "dests": ["cafeteria"],
        "inspectables": {"fence": "The barbed wire fence is tall and stretches around the whole yard. You notice a small hole under the fence, but it is a little bit too small for your body to fit through.",
                         "guard": "The guard is watching over the area."},
        "items": []
    },
    {
        "name": "kitchen",
        "desc": "You are in the kitchen.\nThe kitchen is supervised by guards while inmates are working frantically, rushing to cook meals out for the others. There is a loose spoon on the kitchen counter. \nThere is a door to the south that leads directly to the cafeteria. ",
        "dests": ["cafeteria"],
        "inspectables": {"counter": "There is a loose spoon on the kitchen counter.",
                         "stove": "There is nothing special about the stoves.",
                         "oven": "The ovens are filled with trays of food."},
        "items": ["spoon"]
    },
    {
        "name": "workshop",
        "desc": "You are in the workshop.\nYou can hear machines running as inmates work on projects under the supervision of guards. Amongst the mess on the ground, you can spot a worn out piece of paper and a few nails.\nThe door to the hallway is to the north.",
        "dests": ["hallway"],
        "inspectables": {"machine": "Out of all the old, creaky machines, you notice welding machines, sewing machines, drills, and saws.",
                         "paper": 'The old piece of paper seems to be a list of the respective prison guards\' weaknesses, compiled by a previous inmate. Many of the words are faded and worn out, but the one line that you manage to read says:\n"The guard in the courtyard is easily distracted."',
                         "nail": "The small metal nails are scattered over the floor."},
        "items": ["nail", "paper", "wire"]
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
        if self.name == "courtyard" and player.bread_thrown:
            self.desc = "You are in the courtyard.\nIt is an enclosed outdoor area surrounded by a fence, where you get your daily exercise. The security guard is distracted by a fight among a group of inmates. The path to freedom seems imminent.\nThere is a passage leading to the cafeteria to the west."
            self.inspectables["guard"] = "The security guard is distracted by a fight among a group of inmates."

        if self.name == "workshop" and "paper" in player.inv:
            self.desc = "You are in the workshop.\nYou can hear machines running as inmates work on projects under the supervision of guards. Amongst the mess on the ground, you can spot a few nails.\nThe door to the hallway is to the north."

        return f"{str(self.desc)}"
    # \nYou can go to {', '.join(str(dest) for dest in self.dests)}.

    def inspect(self, input_item):
        """Prints out more information about an item in the location."""

        if self.name == "cell" and input_item == "bed":
            # if they inspect bed in the cell for the first time, then add crowbar to available items
            if "bed" not in player.inspected_items:
                self.items.append("crowbar")

            # if they have taken the crowbar,
            elif "crowbar" not in self.items:
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

            if self.current_loc.name == "workshop" and input_item == "paper":
                # if they take the paper from the workshop,
                # then the paper is removed form the location and they can't inspect it
                del self.current_loc.inspectables["paper"]
            # changes the description of the location
                self.current_loc.desc = "You are in the workshop.\nYou can hear machines running as inmates work on projects under the supervision of guards. Amongst the mess on the ground, you can spot a few nails.\nThe door to the hallway is to the north."

            self.inv.append(input_item)
            self.current_loc.items.remove(input_item)
            return f"You pick up the {input_item} and put it in your pocket."

        else:
            return "You can't take any such thing."

    def use(self, input_item):
        """Conditions for every item that can be used."""
        # don't need to check if item is in inventory because it will only show on gui if it is in inventory

        if input_item == "paper":
            return 'The worn out piece of paper reads:\n"The guard in the courtyard is easily distracted."'

        # if they are in the yard and throw the bread, they distract the guard
        if self.current_loc.name == "courtyard" and input_item == "bread":

            self.bread_thrown = True
            self.inv.remove(input_item)  # removes bread from inventory
            return "You throw the piece of bread at the gathering of people in the corner of the yard, causing a commotion amongst them. This attracts the guards, who go over to check out the fight. "

        # if they have seen the hole in the fence, they can use crowbar
        if "fence" in player.inspected_items and input_item == "crowbar":
            # if they use the crowbar after distracting the guard with bread, they win
            if self.bread_thrown == True:
                self.win = True
                return

            else:
                # if they use the crowbar without distracting the guard, they lose
                self.win = False
                return

        return "You don't know how to use that item here."


player = Player([])

# ------------Tkinter stuff---------------------

# create tkinter window
root = tk.Tk()

# changes title of the window
root.title('⛓️👮 Prison Escape! 👮⛓️')

img = tk.PhotoImage(file='siren.png')
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
    main_text = tk.Text(main_text_frame, height=1,
                        padx=10, pady=5, wrap="word", font=("Calibri", 12))

    # create frame around move buttons
    move_frame = tk.Frame(root, bg="light grey", padx=10, pady=10)
    move_frame.grid(row=1, column=0, sticky="nsew", rowspan=2)

    # create a vertical scrollbar for the text box next to it
    text_scrollbar = tk.Scrollbar(
        main_text_frame, orient="vertical", command=main_text.yview)

    # sticks the scrollbar to north and south of its grid
    text_scrollbar.pack(side="right", fill='y')

    # place at row0, sticky="nsew" makes it fill the whole grid
    main_text.pack(expand=True, fill="both", side="left")
    # insert text that i want to display
    main_text.insert('1.0', player.current_loc)
    # user can't edit the text
    main_text['state'] = 'disabled'

    # configure the text widget to use the scrollbar
    main_text.config(yscrollcommand=text_scrollbar.set)

    # create frame around entry input boxes
    entry_frame = tk.Frame(root)
    entry_frame.grid(row=1, column=1, pady=5, sticky="nswe")

    def inspect_action():
        """Updates the main text box when the player inspects something."""
        inspect_input = inspect_entry.get().lower().strip()

        if inspect_input:
            update_text(player.current_loc.inspect(inspect_input))
        else:
            update_text("Please enter an item to inspect.")

        inspect_entry.delete(0, 'end')

    # entry is a one line text input widget
    inspect_entry = tk.Entry(entry_frame, highlightbackground="black",
                             highlightthickness=1, font=("Calibri", 12))
    inspect_entry.grid(row=0, column=0, sticky="ew", padx=5)

    inspect_btn = tk.Button(entry_frame, text="Inspect!", font=("Calibri", 12),
                            width=10, command=inspect_action)
    inspect_btn.grid(row=0, column=1, pady=1, padx=(0, 5))

    def take_action():
        """Updates the main text box and inventory when the player takes something."""
        take_input = take_entry.get().lower().strip()

        if take_input:
            result = player.take(take_input)
            update_text(result)
            update_inv_display()
        else:
            update_text("Please enter an item to take.")

        take_entry.delete(0, 'end')

    # take_frame = tk.Frame(entry_frame)
    # take_frame.pack(fill="both", padx=5)

    take_entry = tk.Entry(entry_frame, highlightbackground="black",
                          highlightthickness=1, font=("Calibri", 12))
    # take_entry.pack(side=""left"", fill=X, expand=True)
    take_entry.grid(row=1, column=0, sticky="ew", padx=5)

    take_btn = tk.Button(entry_frame, text="Take!", width=10,
                         font=("Calibri", 12), command=take_action)
    # take_btn.pack(side="right", padx=(5, 0))
    take_btn.grid(row=1, column=1, pady=1, padx=(0, 5))

    entry_frame.grid_columnconfigure(0, weight=1)

    inv_frame = tk.Frame(root)
    inv_frame.grid(row=2, column=1, sticky="nswe")

    inv_heading_label = tk.Label(
        inv_frame, text="Click to Use an Item in Your Inventory:", font=("Calibri", 12))
    inv_heading_label.grid(row=0, column=0, sticky="nwes")

    inv_items_frame = tk.Frame(inv_frame)
    inv_items_frame.grid(row=1, column=0)

    inv_empty_text = tk.Label(
        inv_items_frame, text="Your Inventory is Empty.", font=("Calibri", 12))
    inv_empty_text.grid(row=0, column=0, sticky="nwes")

    inv_frame.grid_columnconfigure(0, weight=1)
    inv_frame.grid_propagate(False)

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
        #     item_button.pack(side="left")

        if not player.inv:  # if player inventory is empty, i.e after using all items, print that
            inv_empty_text = tk.Label(
                inv_items_frame, text="Your Inventory is Empty.", font=("Calibri", 12))
            inv_empty_text.grid(row=0, column=0, sticky="nwes")

        for i, item in enumerate(player.inv):
            item_button = tk.Button(inv_items_frame, text=item.title(), font=("Calibri", 12),
                                    command=lambda item=item: use_action(item))
            item_button.grid(row=0, column=i, sticky="ns", padx=5, pady=10)

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
            text='Move', width=20, font=("Calibri", 14),
            # command = creates new buttons for each direction
            command=lambda: [clear_move_frame(), create_move_buttons()]
        )

        # main_move_button.place(relx=.5, rely=.5, anchor="c") #centres the move button in its grid
        main_move_button.pack(fill="both", expand=True)

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
                text=f"Move to the {dest}", font=("Calibri", 12),
                # dest=dest sets the variable before the loop repeats
                command=lambda dest=dest: tkinter_update_move(dest)
            )

            sub_move_button.place(relx=0.5, rely=rely_value,
                                  relwidth=1, relheight=rel_height, anchor="center")

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
        font=("Calibri", 14), wraplength=500)
    description_label.place(relx=0.5, rely=0.3, anchor="center")

    start_button = tk.Button(root, text="PLAY NOW!", font=(
        "Calibri", 14), bg="#4CAF50", fg="white", padx=10, pady=5, activebackground="#45a049", activeforeground="white", command=main)
    start_button.place(relx=0.5, rely=0.6, anchor="center")


def win_window():
    """The win screen."""

    for widget in root.winfo_children():
        widget.destroy()

    win_label = tk.Label(
        root, text="Congratulations, You Win!", font=("Calibri", 20), fg="green")
    win_label.place(relx=0.5, rely=0.2, anchor="center")

    win_text = tk.Label(
        root, text="You seize this moment to dig under the fence with your crowbar, enlargening the hole. "
        "After a few tense moments, you succeed, and with a final effort, you squeeze through to the other side. "
        "As you emerge into the night, you take a deep breath of freedom, feeling the cool air on your face for the first time in years. "
        "You are now a free person, ready to start a new chapter in your life. Well done, you win!", font=("Calibri", 14), wraplength=400)
    win_text.place(relx=0.5, rely=0.6, anchor="center")


def lose_window():
    """The lose screen"""

    for widget in root.winfo_children():
        widget.destroy()

    lose_label = tk.Label(
        root, text="Game Over, You Lose!", font=("Calibri", 20), fg="red")
    lose_label.place(relx=0.5, rely=0.2, anchor="center")

    lose_text = tk.Label(
        root, text="You start to use your crowbar to dig at the hole under the fence. Unfortunately, the guard catches you trying to escape. He knocks you unconscious and drags you back to your cell. Better luck next time!", font=("Calibri", 14), wraplength=400)
    lose_text.place(relx=0.5, rely=0.6, anchor="center")

    # start_button = Button(root, text="Start the game!", command=game)
    # start_button.pack(anchor="center", expand=True)


start_window()

# keeps the tkinter window displaying
root.mainloop()
