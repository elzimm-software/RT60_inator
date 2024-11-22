import tkinter as tk
from tkinter import Tk, ttk
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View():
    def __init__(self):
        self.root = Tk()
        self.root.title("RT60 Analyzer")
        self.root.minsize(800, 600)

        self.tab_control = ttk.Notebook(self.root)
        self.waveform = ttk.Frame(self.tab_control)
        self.analysis = ttk.Frame(self.tab_control)
        self.low_freq = ttk.Frame(self.tab_control)
        self.mid_freq = ttk.Frame(self.tab_control)
        self.high_freq = ttk.Frame(self.tab_control)
        self.combined_freq = ttk.Frame(self.tab_control)
        self.active_file = ttk.Frame(self.root)
        self.active_file.pack(side=tk.TOP, fill=tk.X)

        self.tab_control.add(self.waveform, text="Waveform")
        self.tab_control.add(self.low_freq, text="Low Frequency")
        self.tab_control.add(self.mid_freq, text="Mid Frequency")
        self.tab_control.add(self.high_freq, text="High Frequency")
        self.tab_control.add(self.combined_freq, text="Combined Frequency")
        self.tab_control.add(self.analysis, text="Analysis")
        self.tab_control.pack(expand=1, fill="both")

        self.import_button = ttk.Button(self.active_file, text="Import", command=self.import_clicked)
        self.import_button.pack(side="right")

        self.file_name = tk.StringVar()

        self.file_disp = ttk.Label(self.active_file)
        self.file_disp.pack(side="left")

        self.controller = None

        self.waveform_canvas = None

    def set_controller(self, controller):
        self.controller = controller

    def import_clicked(self):
        if self.controller is not None:
            filename = askopenfilename(filetypes=[("Audio files", ".wav .mp3")])
            self.controller.import_clicked(filename)

    def update_waveform(self):
        if self.waveform_canvas is not None:
            self.waveform_canvas.get_tk_widget().pack_forget()
        self.waveform_canvas = FigureCanvasTkAgg(self.controller.gen_waveform_figure(), master=self.waveform)
        self.waveform_canvas.draw()
        self.waveform_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_active_file(self, filename, duration):
        self.file_name.set("{} : {}s".format(filename, round(duration, 2)))
        self.file_disp.config(text=self.file_name.get())
