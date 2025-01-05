import tkinter as tk
from tkinter import messagebox
import math


'''
#####################
#####################


#######       #######
#######       #######
#######       #######
#######       #######
#######       #######
#######       #######
#######       #######
#######       #######
'''

# PIPE DISPLACEMENT ####################################################################################################################

def calculate_displacement():
    try:
        
        length = float(entries["Tube Length"].get())
        force = float(entries["Applied Force"].get())
        outer_dia = float(entries["Outer Diameter"].get())
        inner_dia = float(entries["Inner Diameter"].get())
        
        E = 71e9 
        I = (math.pi / 64) * (outer_dia**4 - inner_dia**4)
        
        total_displacement = (force * length**3) / (48 * E * I)
        result_label.config(text=f"Displacement: {total_displacement * 1000:.4f} mm")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Ensure the dimensions are valid and non-zero.")

#######################################################################################################################################

def create_displacement_gui():
    global entries, result_label 
    root = tk.Tk()
    root.title("Displacement Calculator - Aluminium 7075")
    
    
    entries = {}  
    parameters = ["Tube Length", "Applied Force", "Outer Diameter", "Inner Diameter"]
    for i, param in enumerate(parameters):
        tk.Label(root, text=f"{param}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[param] = entry 
    
    result_label = tk.Label(root, text="Displacement: ", font=("Arial", 12))
    result_label.grid(row=len(parameters), column=0, columnspan=2, pady=10)
    
    calculate_button = tk.Button(root, text="Calculate", command=calculate_displacement)
    calculate_button.grid(row=len(parameters)+1, column=0, columnspan=2, pady=10)
    
    root.mainloop()

# MINIMUM WALL THICKNESS ###############################################################################################################

def calculate_wall_thickness():
    try:
        external_pressure = float(entries["External pressure"].get())
        outer_diameter = float(entries["Outer diameter"].get())
        E = 71.7e9
        v = 0.33

        denominator = math.sqrt(3 * (1 - v**2))
        thickness = (external_pressure * outer_diameter * denominator) / (2 * E)

        result_label.config(text=f"Minimum wall thickness: {thickness * 1000:.4f} mm")
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Ensure the dimensions are valid and non-zero.")

#######################################################################################################################################

def create_thickness_gui():
    global entries, result_label 
    root = tk.Tk()
    root.title("Minimum wall thickness calculator - Aluminium 7075")
    
    entries = {} 
    parameters = ["External pressure", "Outer diameter"]
    for i, param in enumerate(parameters):
        tk.Label(root, text=f"{param}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[param] = entry  
    
    
    result_label = tk.Label(root, text="Minimum thickness: ", font=("Arial", 12))
    result_label.grid(row=len(parameters), column=0, columnspan=2, pady=10)
    
    
    calculate_button = tk.Button(root, text="Calculate", command=calculate_wall_thickness)
    calculate_button.grid(row=len(parameters)+1, column=0, columnspan=2, pady=10)
    
    
    root.mainloop()

# MENU #################################################################################################################################

user_input = input("Enter command: ").strip().lower()
if user_input == "displacement, aluminium 7050":
    create_displacement_gui()
if user_input == "wall thickness, aluminium 7050":
    create_thickness_gui()
else:
    print("Command not recognized. Please enter a valid command to proceed.")
