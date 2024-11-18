import tkinter as tk
from importlib.metadata import files
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename


class View():
    def __init__(self):
        self.root = Tk()
        self.root.title("RT60 Analyzer")
        self.root.minsize(800, 600)
        self.tab_control = ttk.Notebook(self.root)
        self.files = ttk.Frame(self.tab_control)
        self.waveform = ttk.Frame(self.tab_control)
        self.analysis = ttk.Frame(self.tab_control)
        self.active_file = ttk.Frame(self.root)
        self.active_file.pack(side=tk.TOP, fill=tk.X)
        self.tab_control.add(self.waveform, text="Waveform")
        self.tab_control.add(self.analysis, text="Analysis")
        self.tab_control.pack(expand=1, fill="both")
        self.import_button = ttk.Button(self.active_file, text="Import", command=self.import_clicked)
        self.import_button.pack(side="right")
        self.file_name = tk.StringVar()
        self.file_disp = ttk.Label(self.active_file)
        self.file_disp.pack(side="left")

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def import_clicked(self):
        if self.controller is not None:
            filename = askopenfilename()
            self.controller.import_clicked(filename)

    def set_active_file(self, filename, duration):
        self.file_name.set("{} : {}".format(filename, duration))
        self.file_disp.config(text=self.file_name.get())

class Controller:
    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        view.set_controller(self)

    def import_clicked(self, filename):
        self.model = Model(filename)
        self.view.set_active_file(self.model.file, self.model.duration)

class Model:
    def __init__(self, file):
        self.file = file
        self.duration = None

if __name__ == "__main__":
    model = Model("./test_files/dorm.wav")
    view = View()
    controller = Controller(model, view)
    view.root.mainloop()