import tkinter as tk
from tkinter import ttk
import json
import os


# File to save data
DATA_FILE = "raid_spots.json"

# WoW class colors
class_colors = {
    'Death Knight': '#C41E3A',
    'Demon Hunter': '#A330C9',
    'Druid': '#FF7C0A',
    'Hunter': '#AAD372',
    'Mage': '#3FC7EB',
    'Monk': '#00FF98',
    'Paladin': '#F48CBA',
    'Priest': '#FFFFFF',
    'Rogue': '#FFF468',
    'Shaman': '#0070DD',
    'Warlock': '#8787ED',
    'Warrior': '#C69B6D',
    'Evoker': '#33937F'  
}

# List of specs for each class
class_specs = {
    'Death Knight': ['Blood', 'Frost', 'Unholy'],
    'Demon Hunter': ['Havoc', 'Vengeance'],
    'Druid': ['Balance', 'Feral', 'Guardian', 'Restoration'],
    'Evoker': ['Devastation', 'Preservation'],
    'Hunter': ['Beast Mastery', 'Marksmanship', 'Survival'],
    'Mage': ['Arcane', 'Fire', 'Frost'],
    'Monk': ['Brewmaster', 'Mistweaver', 'Windwalker'],
    'Paladin': ['Holy', 'Protection', 'Retribution'],
    'Priest': ['Discipline', 'Holy', 'Shadow'],
    'Rogue': ['Assassination', 'Outlaw', 'Subtlety'],
    'Shaman': ['Elemental', 'Enhancement', 'Restoration'],
    'Warlock': ['Affliction', 'Demonology', 'Destruction'],
    'Warrior': ['Arms', 'Fury', 'Protection']
}

# Initial data for raid spots
raid_spots_template = {
    'Tank 1': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Tank 2': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Healer 1': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Healer 2': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Healer 3': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Healer 4': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Healer 5': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Melee DPS 1': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Melee DPS 2': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Melee DPS 3': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Melee DPS 4': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Melee DPS 5': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Ranged DPS 1': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Ranged DPS 2': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Ranged DPS 3': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Ranged DPS 4': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''},
    'Ranged DPS 5': {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''}
}


# Loads
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Ensure the loaded data has the correct structure (e.g., "Class" field)
            for role, details in raid_spots_template.items():
                if role not in data:
                    data[role] = details
                else:
                    for key in details:
                        if key not in data[role]:
                            data[role][key] = details[key]
            return data
    return raid_spots_template


# Save
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(raid_spots, f)


# Function to update the UI table
def update_table():
    # Clears table
    for row in table.get_children():
        table.delete(row)

    # Updates table with new info
    for role, data in raid_spots.items():
        row_id = table.insert('', 'end', values=(role, data['Player'], data['Class'], data['Spec'], data['ilvl']))

        # Add color to the row
        player_class = data['Class']
        if player_class in class_colors:
            table.tag_configure(player_class, background=class_colors[player_class])
            table.item(row_id, tags=(player_class,))


def update_spec_dropdown(event):
    selected_class = class_select.get()
    spec_select['values'] = class_specs.get(selected_class, [])
    spec_select.set('')


def add_player():
    role = role_select.get()
    player_name = player_entry.get()
    player_class = class_select.get()
    player_spec = spec_select.get()
    player_ilvl = ilvl_entry.get()
    if role in raid_spots and player_name:
        raid_spots[role] = {'Player': player_name, 'Class': player_class, 'Spec': player_spec, 'ilvl': player_ilvl}
        update_table()
        save_data()


def remove_player():
    role = role_select.get()
    if role in raid_spots:
        raid_spots[role] = {'Player': '', 'Class': '', 'Spec': '', 'ilvl': ''}
        update_table()
        save_data()


# Creates window
root = tk.Tk()
root.title("WoW Raid Spots Manager")

# Loads saved data
raid_spots = load_data()

# Frame for the controls
controls_frame = ttk.Frame(root)
controls_frame.pack(pady=10)

# First row of inputs
role_select = ttk.Combobox(controls_frame, values=list(raid_spots.keys()))
role_select.grid(row=0, column=0, padx=5)
role_select.set('Tank 1')  # Default selection

player_entry = ttk.Entry(controls_frame)
player_entry.grid(row=0, column=1, padx=5)
player_entry.insert(0, "Player Name")

class_select = ttk.Combobox(controls_frame, values=list(class_colors.keys()))
class_select.grid(row=0, column=2, padx=5)
class_select.set('Class')

add_button = ttk.Button(controls_frame, text="Add Player", command=add_player)
add_button.grid(row=0, column=3, padx=5)

remove_button = ttk.Button(controls_frame, text="Remove Player", command=remove_player)
remove_button.grid(row=0, column=4, padx=5)

# Second row
spec_select = ttk.Combobox(controls_frame)
spec_select.grid(row=1, column=0, padx=5)
spec_select.set('Spec')

ilvl_entry = ttk.Entry(controls_frame)
ilvl_entry.grid(row=1, column=1, padx=5)
ilvl_entry.insert(0, "ilvl")

class_select.bind("<<ComboboxSelected>>", update_spec_dropdown)

# Table
columns = ('Role', 'Player', 'Class', 'Spec', 'ilvl')
table = ttk.Treeview(root, columns=columns, show='headings', height=17)

# Column headings
table.heading('Role', text='Role')
table.heading('Player', text='Player')
table.heading('Class', text='Class')
table.heading('Spec', text='Spec')
table.heading('ilvl', text='ilvl')

# Column widths
table.column('Role', width=100)
table.column('Player', width=150)
table.column('Class', width=100)
table.column('Spec', width=100)
table.column('ilvl', width=60)

# Loaded Data
update_table()

table.pack(pady=10)

root.mainloop()
