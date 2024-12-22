import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox

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
        self.root = root
        self.root.title("Celemeter")
        self.root.geometry("500x500")

        self.top_frame = tk.Frame(self.root)
        self.file_frame = tk.Frame(self.root)

        self.info_button = tk.Button(self.top_frame, text="I", command=self.info)
        self.open_button = tk.Button(self.top_frame, text="Open bestand", command=self.open)
        self.plot_button = tk.Button(self.top_frame, text="Plot", command=self.plot)

        self.file_frames = []

        self.info_button.grid(row=0, column=0)
        self.open_button.grid(row=0, column=1)
        self.plot_button.grid(row=0, column=2)

        self.top_frame.grid(row=0, column=0)
        self.file_frame.grid(row=1, column=0)

        self.root.mainloop()

    def open(self):
        file_paths = tkinter.filedialog.askopenfilenames(title="Open bestand", filetypes=[("tekst bestanden", "*.txt")])
        for file_path in file_paths:
            self.debug(f"file_path: {file_path}")
            self.add_file(file_path)

    def add_file(self, file_path):
        file_frame = tk.Frame(self.file_frame)
        info_button = tk.Button(file_frame, text="I", command=self.info)
        file_name_label = tk.Label(file_frame, text=file_path)
        column_entry = tk.Entry(file_frame)
        remove_button = tk.Button(file_frame, text="X", command=lambda: self.remove(file_frame))
        
        info_button.grid(row=0, column=0)
        file_name_label.grid(row=0, column=1)
        column_entry.grid(row=0, column=2)
        remove_button.grid(row=0, column=3)

        self.file_frames.append([file_frame, info_button, file_name_label, column_entry, remove_button])
        file_frame.pack()


    def remove(self, file_frame):
        self.debug(f"file_frames: {self.file_frames}")
        self.debug(f"removing {file_frame}")
        for i in range(len(self.file_frames)):
            self.debug(f"checking {i}")
            if self.file_frames[i][0] == file_frame:
                self.debug(f"removing {i}")
                self.file_frames.pop(i)
                file_frame.destroy()
                break

    def info(self):
        pass

    def plot(self):
        pass
    
    def debug(self, text):
        print(f"[DEBUG]: {text}")

    def warn(self, text):
        print(f"[WARN]: {text}")

if __name__ == "__main__":
    root = tk.Tk()
    celemeter(root)
