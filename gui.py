import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
import os


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



class celemeter:
    def __init__(self, root):
        self.colors = {
            "reset": "\033[0m",
            "debug": "\033[94m",
            "warn": "\033[93m",
            "error": "\033[91m"
        }

        self.temp_file_foder = "temp"
        self.temp_file_extension = ".thorbecke_is_beter"

        self.debug("initializing")
        self.root = root
        self.root.title("Celemeter")
        self.root.geometry("500x500")

        self.debug("creating frames")
        self.top_frame = tk.Frame(self.root)
        self.file_frame = tk.Frame(self.root)
        
        self.debug("creating buttons")
        self.info_button = tk.Button(self.top_frame, text="I", command=self.info)
        self.open_button = tk.Button(self.top_frame, text="Open bestand", command=self.open)
        self.plot_button = tk.Button(self.top_frame, text="Plot", command=self.plot)
        self.close_button = tk.Button(self.root, text="Sluiten", command=self.close)

        self.file_frames = []

        self.debug("gridding")
        self.info_button.grid(row=0, column=0)
        self.open_button.grid(row=0, column=1)
        self.plot_button.grid(row=0, column=2)

        self.top_frame.grid(row=0, column=0)
        self.file_frame.grid(row=1, column=0)
        self.close_button.grid(row=2, column=0, sticky=tk.S)

        self.debug("starting mainloop")
        self.root.mainloop()

    def open(self):
        self.debug("opening filedialog")
        file_paths = tkinter.filedialog.askopenfilenames(title="Open bestand", filetypes=[("tekst bestanden", "*.txt")])
        self.debug(f"file_paths: {file_paths}")
        for file_path in file_paths:
            if self.check_file(file_path):
                self.debug(f'adding "{file_path}"')
                self.add_file(file_path)

    def check_file(self, file_path):
        self.debug(f'checking "{file_path}"')
        try:
            file = open(file_path, "r")
            file.close()
            self.debug(f'file "{file_path}" exists')
            
            openfiles = []
            for file_frame in self.file_frames:
                openfiles.append(file_frame[2].cget("text"))
            
            self.debug(f"openfiles: {openfiles}")
            if file_path in openfiles:
                self.warn(f'file "{file_path}" is already open')
                return False
            else:
                self.debug(f'file "{file_path}" is not already open')
                return True
        except:
            self.warn(f'file "{file_path}" does not exist')
            return False

    def convert_raw_file(self, file_path, temp_file_path):
        self.debug(f'converting "{file_path}", saving to "{temp_file_path}"')
        try:
            if not os.path.exists(self.temp_file_foder):
                os.mkdir(self.temp_file_foder)
                self.debug(f'created "{self.temp_file_foder}"')
            else:
                self.debug(f'"{self.temp_file_foder}" already exists')
            
            if os.path.exists(temp_file_path):
                self.warn(f'temp file "{temp_file_path}" already exists')
                return False
            with open(temp_file_path, "w") as temp_file:
                with open(file_path, "r") as raw_file:
                    for line in raw_file:
                        if line.startswith(">23|01:"):
                            temp_file.write(line.removeprefix(">23|01:").strip() + "\n")
            self.debug(f'processed "{file_path}" -> "{temp_file_path}"')
        except FileNotFoundError:
            self.warn(f'file "{file_path}" does not exist')
        except PermissionError:
            self.warn(f'could not create "{self.temp_file_foder}"')
        except Exception as e:
            self.error(f'could not process "{file_path}": {e}')


    def generate_temp_file_name(self, file_path):
        self.debug(f'generating temp file name for "{file_path}"')
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
        self.debug(f'file_frames: {self.file_frames}')
        self.debug(f'removing "{file_frame}"')
        for i in range(len(self.file_frames)):
            self.debug(f'checking {i}')

            if self.file_frames[i][0] == file_frame and self.file_frames[i][5] != "":
                self.debug(f'removing temp file "{self.file_frames[i][5]}"')
                os.remove(self.file_frames[i][5])
                self.debug(f'removed temp file "{self.file_frames[i][5]}"')
            else:
                self.debug(f'not removing temp file "{self.file_frames[i][5]}"')

            if self.file_frames[i][0] == file_frame:
                self.debug(f'removing {i}')
                self.file_frames.pop(i)
                file_frame.destroy()
                break
            else:
                self.debug(f'not removing {i}')

    def close(self):
        self.debug("closing files")
        for file_frame in self.file_frames:
            self.debug(f'removing "{file_frame[0]}"')
            self.remove(file_frame[0])
        self.debug("closing window")
        self.root.destroy()

    def info(self):
        pass

    def plot(self):
        pass
    
    def debug(self, text):
        print(f"{self.colors['debug']}[DEBUG]: {self.colors['reset']}{text}")

    def warn(self, text):
        print(f"{self.colors['warn']}[WARN]: {self.colors['reset']}{text}")

    def error(self, text):
        print(f"{self.colors['error']}[ERROR]: {self.colors['reset']}{text}")

if __name__ == "__main__":
    root = tk.Tk()
    celemeter(root)
