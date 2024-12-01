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
        self.intensity = ttk.Frame(self.tab_control)
        self.low_freq = ttk.Frame(self.tab_control)
        self.mid_freq = ttk.Frame(self.tab_control)
        self.high_freq = ttk.Frame(self.tab_control)
        self.combined_freq = ttk.Frame(self.tab_control)
        self.analysis = ttk.Frame(self.tab_control)

        self.tab_control.add(self.waveform, text="Waveform")
        self.tab_control.add(self.intensity, text="Intensity")
        self.tab_control.add(self.low_freq, text="Low Frequency")
        self.tab_control.add(self.mid_freq, text="Mid Frequency")
        self.tab_control.add(self.high_freq, text="High Frequency")
        self.tab_control.add(self.combined_freq, text="Combined Frequency")
        self.tab_control.add(self.analysis, text="Analysis")

        self.tab_control.pack(expand=1, fill="both")

        # Active file frame with an import button
        self.active_file = ttk.Frame(self.root)
        self.active_file.pack(side=tk.TOP, fill=tk.X)

        # Create the import button
        self.import_button = ttk.Button(self.active_file, text="Import", command=self.import_clicked)
        self.import_button.pack(side="right")

        # Display file name
        self.file_name = tk.StringVar()
        self.file_disp = ttk.Label(self.active_file)
        self.file_disp.pack(side="left")

        # Controller reference
        self.controller = None

        # Canvas for graphs
        self.waveform_canvas = None
        self.intensity_canvas = None
        self.low_freq_canvas = None
        self.mid_freq_canvas = None
        self.high_freq_canvas = None
        self.combined_freq_canvas = None

    def set_controller(self, controller):
        self.controller = controller

    def import_clicked(self):
        if self.controller is not None:
            filename = askopenfilename(filetypes=[("Audio files", ".wav .mp3")])  # Opens the file dialog
            if filename:  # Check if the user selected a file
                print(f"Selected file: {filename}")  # Debugging line
                self.controller.import_clicked(filename)

    def update_waveform(self, fig):
        if self.waveform_canvas is not None:
            self.waveform_canvas.get_tk_widget().pack_forget()
        self.waveform_canvas = FigureCanvasTkAgg(fig, master=self.waveform)
        self.waveform_canvas.draw()
        self.waveform_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_intensity(self, fig):
        if self.intensity_canvas is not None:
            self.intensity_canvas.get_tk_widget().pack_forget()
        self.intensity_canvas = FigureCanvasTkAgg(fig, master=self.intensity)
        self.intensity_canvas.draw()
        self.intensity_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_low_freq(self, fig):
        if self.low_freq_canvas is not None:
            self.low_freq_canvas.get_tk_widget().pack_forget()
        self.low_freq_canvas = FigureCanvasTkAgg(fig, master=self.low_freq)
        self.low_freq_canvas.draw()
        self.low_freq_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_mid_freq(self, fig):
        if self.mid_freq_canvas is not None:
            self.mid_freq_canvas.get_tk_widget().pack_forget()
        self.mid_freq_canvas = FigureCanvasTkAgg(fig, master=self.mid_freq)
        self.mid_freq_canvas.draw()
        self.mid_freq_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_high_freq(self, fig):
        if self.high_freq_canvas is not None:
            self.high_freq_canvas.get_tk_widget().pack_forget()
        self.high_freq_canvas = FigureCanvasTkAgg(fig, master=self.high_freq)
        self.high_freq_canvas.draw()
        self.high_freq_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_combined_freq(self, fig):
        if self.combined_freq_canvas is not None:
            self.combined_freq_canvas.get_tk_widget().pack_forget()
        self.combined_freq_canvas = FigureCanvasTkAgg(fig, master=self.combined_freq)
        self.combined_freq_canvas.draw()
        self.combined_freq_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_analysis(self, text):
        label = ttk.Label(self.analysis, text=text)
        label.pack(side="top")

    def set_active_file(self, filename, duration):
        self.file_name.set("{} : {}s".format(filename, round(duration, 2)))
        self.file_disp.config(text=f"{self.file_name.get()}, "
                                   f"resonant frequency: {self.controller.get_resonant_frequency()} Hz, "
                                   f"difference: {self.controller.get_difference()}s\n"
                                   f"Low RT60: {self.controller.model.low_rt60}, "
                                   f"Mid RT60: {self.controller.model.mid_rt60}, "
                                   f"High RT60: {self.controller.model.high_rt60}, "
                                   f"Combined RT60: {self.controller.model.combined_rt60}")