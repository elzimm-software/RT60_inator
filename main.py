import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import numpy
from scipy.io import wavfile
import pathlib
#from pydub import AudioSegment
import scipy.io as scio
import numpy as np


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

class Controller:
    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        view.set_controller(self)

    def import_clicked(self, filename):
        new_model = Model(filename)
        if new_model.file is not None:
            self.model = new_model
            self.view.set_active_file(self.model.file, self.model.duration)

class Model:
    def __init__(self, file):
        if file != '':
            #if pathlib.Path(file).suffix == '.mp3':
            #    sound = AudioSegment.from_mp3(file)
            #    sound.export("converted.wav", format="format")
            #    file = "converted.wav"
            self.file = file
            self.samplerate, self.data = wavfile.read(self.file)
            self.duration = round(self.data.shape[0]/self.samplerate, 1)
            if len(self.data.shape) > 1:
                self.data = np.array([(x[0]+x[1])/2 for x in self.data]).astype(np.int16)
        else:
            self.file = None
            self.samplerate = None
            self.data = None
            self.duration = None

if __name__ == "__main__":
    model = Model("./test_files/dorm.wav")
    view = View()
    controller = Controller(model, view)
    view.root.mainloop()