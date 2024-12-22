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

        self.file_frames = []

        self.info_button.pack()
        self.open_button.pack()

        self.top_frame.pack()
        self.file_frame.pack()

        self.root.mainloop()

    def open(self):
        file_path = tkinter.filedialog.askopenfilename(title="Open bestand", filetypes=[("tekst bestanden", "*.txt")])
        if file_path:
            print(file_path)
            self.add_file(file_path)

    def add_file(self, file_path):
        file_frame = tk.Frame(self.file_frame)
        info_button = tk.Button(file_frame, text="I", command=self.info)
        file_name_label = tk.Label(file_frame, text=file_path)
        column_entry = tk.Entry(file_frame)
        remove_button = tk.Button(file_frame, text="X", command=self.remove)
        
        info_button.pack()
        file_name_label.pack()
        column_entry.pack()
        remove_button.pack()

        self.file_frames.append(file_frame)
        file_frame.pack()


    def remove(self):
        pass
    
    def info(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    celemeter(root)
