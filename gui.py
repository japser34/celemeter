import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
import os
import subprocess


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



class debug:
    def __init__(self, type, colors={"reset": "\033[0m", "debug": "\033[94m", "warn": "\033[93m", "error": "\033[91m"}):
        self.colors = colors
        self.type = type

    def debug(self, text):
        print(f"{self.colors['debug']}[DEBUG {self.type}]: {self.colors['reset']}{text}")
    
    def warn(self, text):
        print(f"{self.colors['warn'] }[WARN  {self.type}]: {self.colors['reset']}{text}")
    
    def error(self, text):
        print(f"{self.colors['error']}[ERROR {self.type}]: {self.colors['reset']}{text}")

class Plotting:
    def __init__(self, x_label="Tijd sinds start (s)", y_label="Waarde", title="Grafiek"):
        self.debug = debug(type="plot")
        self.debug.debug(f'x label: "{x_label}", y label: "{y_label}", title: "{title}"')
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

        self.data = []

        self.gnuplot = subprocess.Popen(["gnuplot"], stdin=subprocess.PIPE, text=True)

        self.gnuplot.stdin.write(f"""
                                 set terminal qt enhanced
                                 set datafile separator comma
                                 set mouse
                                 set grid
                                 set xlabel "{self.x_label}"
                                 set ylabel "{self.y_label}"
                                 set title "{self.title}"
                                 """)
        self.gnuplot.stdin.flush()

    def generate_command(self):
        if not self.data:
            self.debug.warn("no data to plot")
            return

        commands = []
        for file_name, x_col, y_col in self.data:
            commands.append(f'plot "{file_name}" using {x_col}:{y_col} with lines title "{file_name}.{y_col}"')
            self.debug.debug(f'plotting "{file_name}" using {x_col}:{y_col} with lines title "{file_name}.{y_col}"')
        
        return ", ".join(commands)

    def plot(self):
        if not self.data:
            self.debug.warn("no data to plot")
            return

        commands = self.generate_command()
        if not commands:
            self.debug.warn("no commands to plot")
            return
    
        self.gnuplot.stdin.write(f'plot {commands}')
        self.gnuplot.stdin.flush()

    def close(self):
        if self.gnuplot:
            self.debug.debug("closing gnuplot")
            self.gnuplot.stdin.write("exit\n")
            self.gnuplot.stdin.flush()
            self.gnuplot.wait()
            self.gnuplot = None
            self.debug.debug("closed gnuplot")
        else:
            self.debug.debug("gnuplot already closed")

class celemeter:
    def __init__(self, root):
        self.temp_file_foder = "temp"
        self.temp_file_extension = ".thorbecke_is_beter"

        self.file_frames = []
        self.debug = debug(type="main")


        self.initialize_main_ui()

        self.debug.debug(f"initializing gnuplot")
        self.gnuplot = Plotting()


        self.debug.debug("starting mainloop")
        self.root.mainloop()

    def loading_animation(self):
        self.debug.debug("loading animation")



    def initialize_main_ui(self):
        self.debug.debug("initializing")
        self.root = root
        self.root.title("Celemeter")
        self.root.geometry("500x500")

        self.debug.debug("creating frames")
        self.top_frame = tk.Frame(self.root)
        self.file_frame = tk.Frame(self.root)
        
        self.debug.debug("creating buttons")
        self.info_button = tk.Button(self.top_frame, text="I", command=self.info)
        self.open_button = tk.Button(self.top_frame, text="Open bestand", command=self.open)
        self.plot_button = tk.Button(self.top_frame, text="Plot", command=self.plot)
        self.close_button = tk.Button(self.root, text="Sluiten", command=self.close)

        self.debug.debug("gridding")
        self.info_button.grid(row=0, column=0)
        self.open_button.grid(row=0, column=1)
        self.plot_button.grid(row=0, column=2)

        self.top_frame.grid(row=0, column=0)
        self.file_frame.grid(row=1, column=0)
        self.close_button.grid(row=2, column=0, sticky=tk.S)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def open(self):
        self.debug.debug("opening filedialog")
        file_paths = tkinter.filedialog.askopenfilenames(title="Open bestand", filetypes=[("tekst bestanden", "*.txt")])
        self.debug.debug(f"file_paths: {file_paths}")
        for file_path in file_paths:
            if self.check_file(file_path):
                self.debug.debug(f'adding "{file_path}"')
                self.add_file(file_path)

    def check_file(self, file_path):
        self.debug.debug(f'checking "{file_path}"')
        try:
            file = open(file_path, "r")
            file.close()
            self.debug.debug(f'file "{file_path}" exists')
            
            openfiles = []
            for file_frame in self.file_frames:
                openfiles.append(file_frame[2].cget("text"))
            
            self.debug.debug(f"openfiles: {openfiles}")
            if file_path in openfiles:
                self.debug.warn(f'file "{file_path}" is already open')
                return False
            else:
                self.debug.debug(f'file "{file_path}" is not already open')
                return True
        except:
            self.debug.warn(f'file "{file_path}" does not exist')
            return False

    def convert_raw_file(self, file_path, temp_file_path):
        self.debug.debug(f'converting "{file_path}", saving to "{temp_file_path}"')
        try:
            if not os.path.exists(self.temp_file_foder):
                os.mkdir(self.temp_file_foder)
                self.debug.debug(f'created "{self.temp_file_foder}"')
            else:
                self.debug.debug(f'"{self.temp_file_foder}" already exists')
            
            if os.path.exists(temp_file_path):
                self.debug.warn(f'temp file "{temp_file_path}" already exists')
                return False
            with open(temp_file_path, "w") as temp_file:
                with open(file_path, "r") as raw_file:
                    for line in raw_file:
                        if line.startswith(">23|01:"):
                            temp_file.write(line.removeprefix(">23|01:").strip() + "\n")
            self.debug.debug(f'processed "{file_path}" -> "{temp_file_path}"')
        except FileNotFoundError:
            self.debug.warn(f'file "{file_path}" does not exist')
        except PermissionError:
            self.debug.warn(f'could not create "{self.temp_file_foder}"')
        except Exception as e:
            self.debug.error(f'could not process "{file_path}": {e}')


    def generate_temp_file_name(self, file_path):
        self.debug.debug(f'generating temp file name for "{file_path}"')
        return f"{self.temp_file_foder}/{file_path.split('/')[-1].split('.')[0]}{self.temp_file_extension}"

    def add_file(self, file_path):
        temp_file_path = self.generate_temp_file_name(file_path)
        self.convert_raw_file(file_path, temp_file_path)
    
        file_frame = tk.Frame(self.file_frame)
        info_button = tk.Button(file_frame, text="I", command=self.info)
        file_name_label = tk.Label(file_frame, text=file_path)
        column_entry = tk.Entry(file_frame)
        remove_button = tk.Button(file_frame, text="X", command=lambda: self.remove(file_frame))
        
        info_button.grid(row=0, column=0)
        file_name_label.grid(row=0, column=1)
        column_entry.grid(row=0, column=2)
        remove_button.grid(row=0, column=3)

        self.file_frames.append([file_frame, info_button, file_name_label, column_entry, remove_button, temp_file_path])
        file_frame.pack()



    def remove(self, file_frame):
        if file_frame in self.file_frames:
            self.debug.debug(f'removing "{file_frame}"')

            # Extract the actual frame widget
            frame_widget = file_frame[0]  # This is the Tkinter Frame object

            # Remove the temp file
            temp_file_path = file_frame[5]
            if temp_file_path:  # Only proceed if temp file exists
                if os.path.exists(temp_file_path):
                    self.debug.debug(f'removing temp file "{temp_file_path}"')
                    try:
                        os.remove(temp_file_path)
                        self.debug.debug(f'removed temp file "{temp_file_path}"')
                    except Exception as e:
                        self.debug.warn(f'could not remove temp file "{temp_file_path}": {e}')
            
            # Destroy the frame widget
            frame_widget.destroy()  # This destroys the Tkinter Frame widget
            self.file_frames.remove(file_frame)  # Remove the frame from the list

        else:
            self.debug.debug(f'not removing "{file_frame}" because it is already removed')



    def close(self):
        self.debug.debug("closing files")
        self.debug.debug(f'file_frames: {self.file_frames}')
        
        # Track removed files to avoid removing them twice
        for file_frame in self.file_frames[:]:  # Iterate over a copy of the list
            self.remove(file_frame)
        
        self.debug.debug("closing window")
        self.root.destroy()

    def info(self):
        pass

    def get_column(self, file_frame):
        self.debug.debug(f'getting column for "{file_frame}"')
        data = file_frame[3].get()
        
        return file_frame[2].cget("text")

    def plot(self): # the data should look like this: [(file_name, x_col, y_col), ...]
        self.debug.debug("plotting")
        for file_frame in self.file_frames:
            self.gnuplot.data.append((file_frame[5], 0, self.get_column(file_frame)))
        self.gnuplot.plot()

if __name__ == "__main__":
    root = tk.Tk()
    celemeter(root)
