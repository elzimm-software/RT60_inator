import tkinter as tk
from tkinter import *
from tkinter import ttk

class View():
    def __init__(self):
        self.root = Tk()
        self.root.title("RT60 Analyzer")
        self.root.minsize(800, 600)
        self.tab_control = ttk.Notebook(self.root)
        self.files = ttk.Frame(self.tab_control)
        self.waveform = ttk.Frame(self.tab_control)
        self.analysis = ttk.Frame(self.tab_control)
        self.tab_control.add(self.files, text="Files")
        self.tab_control.add(self.waveform, text="Waveform")
        self.tab_control.add(self.analysis, text="Analysis")
        self.tab_control.pack(expand=1, fill="both")
        self.file_buttons = ttk.Frame(self.files)
        self.file_buttons.pack(side=tk.TOP, fill="x")
        self.import_button = ttk.Button(self.file_buttons, text="Import")
        self.import_button.pack(side=tk.LEFT)
        self.remove_button = ttk.Button(self.file_buttons, text="Remove")
        self.remove_button.pack(side=tk.LEFT)
        self.set_active_button = ttk.Button(self.file_buttons, text="Set Active")
        self.set_active_button.pack(side=tk.LEFT)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def import_clicked(self):
        if self.controller is not None:
            self.controller.import_file()

    def remove_clicked(self):
        if self.controller is not None:
            self.controller.remove_file()

    def set_active_clicked(self):
        if self.controller is not None:
            self.controller.set_active_file()

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        view.set_controller(self)

    def import_file(self):
        pass

    def remove_file(self):
        pass

    def set_active_file(self):
        pass

class Model:
    def __init__(self):
        pass

if __name__ == "__main__":
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.root.mainloop()