import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import time
import sys

SYSTEM_ARGS = sys.argv

DEBUG = False
WARN = False
ERROR = False
COL_NAMES = {
    "1": "Tijd sinds start (s)",
    "2": "Spanning in (V)",

    "6": "Stroomsterkte in (A)",
    "7": "Vermogen in (W)"
}

IMPORTANT = '''
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
        if DEBUG:
            print(f"{self.colors['debug']}[DEBUG {self.type}]: {self.colors['reset']}{text}")    
    def warn(self, text):
        if WARN:
            print(f"{self.colors['warn'] }[WARN  {self.type}]: {self.colors['reset']}{text}")

    def error(self, text):
        if ERROR:
            print(f"{self.colors['error']}[ERROR {self.type}]: {self.colors['reset']}{text}")

class Plotting:
    def __init__(self, x_label="Tijd sinds start (s)", y_label="Waarde", title="Grafiek", col_names=COL_NAMES):
        self.debug = debug(type="plot")
        self.debug.debug(f'x label: "{x_label}", y label: "{y_label}", title: "{title}"')
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.col_names = col_names

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

    def generate_title(self, file_name, y_col):
        self.debug.debug(f"generating title for {file_name} and {y_col}")
        extension_less_file_name = os.path.splitext(os.path.basename(file_name))[0]
        self.debug.debug(f'extension_less_file_name: {extension_less_file_name}')
        if y_col in self.col_names:
            self.debug.debug(f'y_col "{y_col}" is in col_names: {self.col_names[y_col]}')
            return f"{extension_less_file_name} - {self.col_names[y_col]}"
        else:
            self.debug.debug(f'y_col "{y_col}" is not in col_names')
            return f"{extension_less_file_name} - {y_col}"

    def generate_command(self):
        self.debug.debug("generating command")
        self.debug.debug(f'data: {self.data}')
        if not self.data:
            self.debug.warn("no data to plot")
            return

        commands = []
        for file_name, x_col, y_col in self.data:
            commands.append(f'"{file_name.replace("\\", "/")}" using {x_col}:{y_col} with lines title "{self.generate_title(file_name, y_col)}"')
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

        self.debug.debug(f'running `plot {commands}`')

        self.gnuplot.stdin.write(f'plot {commands}\n')
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
            self.debug.warn("gnuplot already closed")

class celemeter:
    def __init__(self, root):
        self.temp_file_foder = "temp"
        self.temp_file_extension = ".thorbecke_is_beter"

        self.file_frames = []
        self.debug = debug(type="main")

        self.debug.debug(IMPORTANT)

        self.initialize_main_ui()

        self.debug.debug(f"initializing gnuplot")
        self.gnuplot = Plotting()


        self.debug.debug("starting mainloop")
        self.root.mainloop()
        self.debug.debug("mainloop ended")

    def initialize_main_ui(self):
        self.debug.debug("initializing")
        self.root = root
        self.root.title("Celemeter")
        self.root.geometry("700x600")

        self.debug.debug("creating frames")
        self.top_frame = tk.Frame(self.root)
        self.file_frame = tk.Frame(self.root)

        self.debug.debug("creating buttons")
        self.info_button = tk.Button(self.top_frame, text="I", command=self.info)
        self.open_button = tk.Button(self.top_frame, text="Open bestand", command=self.open)
        self.plot_button = tk.Button(self.top_frame, text="Plot", command=self.plot)
        self.status_label = tk.Label(self.root, text="thorbecke is beter")
        self.close_button = tk.Button(self.root, text="Sluiten", command=self.close)

        self.debug.debug("gridding")
        self.info_button.grid(row=0, column=0)
        self.open_button.grid(row=0, column=1)
        self.plot_button.grid(row=0, column=2)

        self.top_frame.grid(row=0, column=0)
        self.file_frame.grid(row=1, column=0)
        self.status_label.grid(row=2, column=0, sticky=tk.S)
        self.close_button.grid(row=3, column=0, sticky=tk.S)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def open(self):
        self.debug.debug("opening filedialog")
        file_paths = tk.filedialog.askopenfilenames(title="Open bestand", filetypes=[("tekst bestanden", "*.txt")])
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
        except Exception as e:
            self.debug.error(f'could not check if file "{file_path}" is open: {e}')
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
                self.debug.error(f'temp file "{temp_file_path}" already exists')
                return False
            with open(temp_file_path, "w") as temp_file:
                with open(file_path, "r") as raw_file:
                    for line in raw_file:
                        if line.startswith(">23|01:"):
                            temp_file.write(line.removeprefix(">23|01:").strip() + "\n")
            self.debug.debug(f'processed "{file_path}" -> "{temp_file_path}"')
        except FileNotFoundError:
            self.debug.error(f'file "{file_path}" not found')
        except PermissionError:
            self.debug.warn(f'could not create "{self.temp_file_foder}"')
        except Exception as e:
            self.debug.error(f'could not process "{file_path}": {e}')

    def generate_temp_file_name(self, file_path):
        self.debug.debug(f'generating temp file name for "{file_path}"')
        file_name = os.path.basename(file_path)
        file_name_parts = file_name.split('.')
        timestamp = str(int(time.time()))
        temp_file_name = f"{file_name_parts[0]}_{timestamp}{self.temp_file_extension}"
        return os.path.join(self.temp_file_foder, temp_file_name)

    def add_file(self, file_path):
        temp_file_path = self.generate_temp_file_name(file_path)
        self.convert_raw_file(file_path, temp_file_path)
        file_name = os.path.basename(file_path)

        info_button = tk.Button(self.file_frame, text="I", command=self.info)
        file_name_label = tk.Label(self.file_frame, text=file_name)
        column_entry = tk.Entry(self.file_frame)
        remove_button = tk.Button(self.file_frame, text="X", command=lambda frame=self.file_frame: self.remove(frame))

        info_button.grid(row=0, column=0)
        file_name_label.grid(row=0, column=1)
        column_entry.grid(row=0, column=2)
        remove_button.grid(row=0, column=3)

        self.file_frames.append([self.file_frame, info_button, file_name_label, column_entry, remove_button, temp_file_path])

    def remove(self, file_frame):
        self.debug.debug(f'removing "{file_frame}"')

        for frame in self.file_frames[:]:
            if frame[0] == file_frame:
                self.debug.debug(f'found frame to remove')

                temp_file_path = frame[5]
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.remove(temp_file_path)
                        self.debug.debug(f'removed temp file "{temp_file_path}"')
                    except Exception as e:
                        self.debug.error(f'could not remove temp file "{temp_file_path}": {e}')
                else:
                    self.debug.warn(f'temp file "{temp_file_path}" does not exist')

                frame[0].destroy()
                self.file_frames.remove(frame)
                self.debug.debug(f'successfully removed frame and its temp file')
                return
            else:
                self.debug.debug(f'frame "{frame}" is not the one to remove')

    def close(self):
        self.debug.debug("closing files")
        self.debug.debug(f'file_frames: {self.file_frames}')

        for file_frame in self.file_frames[:]:
            self.debug.debug(f'removing file frame "{file_frame[0]}"')
            self.remove(file_frame[0])

        self.debug.debug("closing gnuplot")
        self.gnuplot.close()

        self.debug.debug("closing window")
        self.root.destroy()

    def info(self):
        pass

    def get_min_max_columns(self, file_frame):
        file = file_frame[5]
        self.debug.debug(f'file: {file}')
        try:
            with open(file, "r") as file:
                first_line = file.readline()
                self.debug.debug(f'first_line: {first_line}')
                data = first_line.split(",")
                min = 0
                max = len(data)
                self.debug.debug(f'min: {min}, max: {max}')
                return min, max
        except Exception as e:
            self.debug.error(f'could not get min and max columns: {e}')
            return 0, 0

    def get_columns(self, file_frame):
        data = file_frame[3].get()
        self.debug.debug(f'data: {data}')
        return data.split(",") if data else []

    def validate_columns(self, file_frame):
        min, max = self.get_min_max_columns(file_frame)
        columns = self.get_columns(file_frame)
        self.debug.debug(f'columns: {columns}')
        if columns:
            for column in columns:
                try:
                    int_column = int(column)
                except Exception as e:
                    self.debug.warn(f'column "{column}" is invalid: {e}')
                    return False
                if int(column) < min or int(column) > max:
                    self.debug.warn(f'column "{column}" is invalid: "{column}" is out of range')
                    return False
        return True

    def plot(self): # the data should look like this: [(temp_file_name, x_col, y_col), ...]
        self.debug.debug("plotting")
        self.gnuplot.data.clear()
        for file_frame in self.file_frames:
            self.debug.debug(f'getting columns for "{file_frame}"')
            columns = self.get_columns(file_frame)
            if not self.validate_columns(file_frame):
                self.debug.warn(f'no columns to plot for "{file_frame}"')
                return
            self.debug.debug(f'valid columns: {columns}')
            if columns:
                for column in columns:
                    self.debug.debug(f'adding column {column} to gnuplot')
                    self.gnuplot.data.append((file_frame[5], 1, int(column)))
            else:
                self.debug.warn(f'no columns to plot for "{file_frame}"')
        self.gnuplot.plot()

if __name__ == "__main__":
    root = tk.Tk()
    celemeter(root)
