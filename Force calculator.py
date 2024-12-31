import tkinter as tk
from tkinter import messagebox
import math

def calculate_displacement():
    try:
        length = float(length_entry.get())
        force = float(force_entry.get())
        outer_dia = float(outer_dia_entry.get())
        inner_dia = float(inner_dia_entry.get())
        
        E = 71e9 
        I = (math.pi / 64) * (outer_dia**4 - inner_dia**4)
        
        total_displacement = (force * length**3) / (48 * E * I)
        result_label.config(text=f"Displacement: {total_displacement * 1000:.4f} mm")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Ensure the dimensions are valid and non-zero.")

root = tk.Tk()
root.title("Displacement Calculator - Aluminium 7075")

tk.Label(root, text="Tube Length (m):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Applied Force (N):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
force_entry = tk.Entry(root)
force_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Outer Diameter (m):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
outer_dia_entry = tk.Entry(root)
outer_dia_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Inner Diameter (m):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
inner_dia_entry = tk.Entry(root)
inner_dia_entry.grid(row=3, column=1, padx=10, pady=5)

result_label = tk.Label(root, text="Displacement: ", font=("Arial", 12))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

calculate_button = tk.Button(root, text="Calculate", command=calculate_displacement)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
