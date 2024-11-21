import tkinter as tk
from tkinter import Tk, ttk
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
            filename = askopenfilename(filetypes=[("Audio files", ".wav .mp3")])
            self.controller.import_clicked(filename)

    def set_active_file(self, filename, duration):
        self.file_name.set("{} : {}s".format(filename, duration))
        self.file_disp.config(text=self.file_name.get())
