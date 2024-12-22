import tkinter as tk

root = tk.Tk()
root.title('AAHAHAHAHAHA')

window_width = 600
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# List of strings to display

first_message = """ 




|||||                                   |||||
|||||                                   |||||
|||||                                   |||||
|||||                                   |||||
|||||                                   |||||

[----------]
"""
second_message = """ 

---------------


|||||                              |||||
|||||                              |||||
|||||                              |||||
|||||                              |||||
|||||                              |||||

[==-------]
"""

third_message = """ 

---------------
      -----    

|||||                         |||||
|||||                         |||||
|||||                         |||||
|||||                         |||||
|||||                         |||||

[====-----]
"""

fourth_message = """ 

---------------
---------------

|||||                    |||||
|||||                    |||||
|||||                    |||||
|||||                    |||||
|||||                    |||||

[======---]
"""

fifth_message = """ 

###############
###############

#####            #####
#####            #####
#####            #####
#####            #####
#####            #####

[==========]
"""

sixth_message = """ 

###############
###############

#####            #####
#####            #####
#####            #####
#####            #####
#####            #####

Celemeter™ 
Thorbecke is beter
"""

texts = [
    first_message,
    second_message,
    third_message,
    fourth_message,
    fifth_message,
    sixth_message
]

current_index = 0
update_count = 0  # Counter to keep track of updates

# Function to update the text
def update_text():
    global current_index, update_count
    if update_count < 6:  # Only update text 5 times
        label.config(text=texts[current_index])  # Update the label text
        current_index = (current_index + 1) % len(texts)  # Move to the next text in the list
        update_count += 1  # Increment the counter
        root.after(1000, update_text)  # Schedule this function to run again after 1 second

label = tk.Label(root, text="", anchor="center")
label.pack()

update_text()

root.mainloop()
