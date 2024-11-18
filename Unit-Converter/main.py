import tkinter as tk
from tkinter import ttk

# Conversion factors grouped by categories
conversion_categories = {
    "Distance": {
        "Kilometers": {"Miles": 0.621371, "Feet": 3280.84, "Meters": 1000},
        "Miles": {"Kilometers": 1.60934, "Feet": 5280, "Meters": 1609.34},
        "Feet": {"Kilometers": 0.0003048, "Miles": 0.000189394, "Meters": 0.3048},
        "Meters": {"Kilometers": 0.001, "Miles": 0.000621371, "Feet": 3.28084},
    },
    "Weight": {
        "Pounds": {"Kilograms": 0.453592},
        "Kilograms": {"Pounds": 2.20462},
    },
    "Temperature": {
        "Celsius": {"Fahrenheit": lambda x: (x * 9 / 5) + 32},
        "Fahrenheit": {"Celsius": lambda x: (x - 32) * 5 / 9},
    },
}

# Function to update units based on category selection
def update_units(*args):
    category = category_choice.get()
    units = list(conversion_categories[category].keys())
    from_choice.set(units[0])
    to_choice.set(units[1])
    from_menu['menu'].delete(0, 'end')
    to_menu['menu'].delete(0, 'end')
    for unit in units:
        from_menu['menu'].add_command(label=unit, command=tk._setit(from_choice, unit))
        to_menu['menu'].add_command(label=unit, command=tk._setit(to_choice, unit))

# Function to handle conversion
def convert():
    try:
        value = float(value_entry.get())
        category = category_choice.get()
        from_unit = from_choice.get()
        to_unit = to_choice.get()

        conversion_dict = conversion_categories[category]
        if to_unit in conversion_dict[from_unit]:
            conversion = conversion_dict[from_unit][to_unit]
            if callable(conversion):
                converted = conversion(value)
            else:
                converted = value * conversion
            result_label.config(text=f"{converted:.2f} {to_unit}")
        else:
            result_label.config(text="Conversion not supported")
    except ValueError:
        result_label.config(text="Invalid input")

# Initialize main window
root = tk.Tk()
root.title("Unit Converter")
root.geometry("550x450")
root.configure(bg="#1e1e1e")  # Dark background color

# Styled input field
value_label = tk.Label(root, text="Enter value:", bg="#1e1e1e", fg="#dcdcdc", font=("Helvetica", 14))
value_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
value_entry = ttk.Entry(root, font=("Helvetica", 14))
value_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Category dropdown
category_label = tk.Label(root, text="Category:", bg="#1e1e1e", fg="#dcdcdc", font=("Helvetica", 14))
category_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
category_choice = tk.StringVar(root)
category_choice.set("Distance")
category_menu = ttk.OptionMenu(root, category_choice, "Distance", *conversion_categories.keys())
category_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# From dropdown
from_label = tk.Label(root, text="From:", bg="#1e1e1e", fg="#dcdcdc", font=("Helvetica", 14))
from_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
from_choice = tk.StringVar(root)
from_choice.set("Kilometers")
from_menu = ttk.OptionMenu(root, from_choice, "")
from_menu.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# To dropdown
to_label = tk.Label(root, text="To:", bg="#1e1e1e", fg="#dcdcdc", font=("Helvetica", 14))
to_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
to_choice = tk.StringVar(root)
to_choice.set("Miles")
to_menu = ttk.OptionMenu(root, to_choice, "")
to_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Update dropdown menus when category changes
category_choice.trace('w', update_units)
update_units()

# Convert button
convert_button = ttk.Button(root, text="Convert", command=convert)
convert_button.grid(row=5, column=0, columnspan=2, pady=20)

# Result display
result_label = tk.Label(root, text="", bg="#1e1e1e", fg="#79c6e3", font=("Helvetica", 16, "bold"))
result_label.grid(row=6, column=0, columnspan=2)

# Add padding
for widget in root.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Run main loop
root.mainloop()
