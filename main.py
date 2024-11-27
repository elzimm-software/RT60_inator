from controller import Controller
from model import Model
from view import View
from utils import display_error

from shutil import which
from tkinter import messagebox

if __name__ == "__main__":
    if which("ffmpeg") is None:
        display_error("Could not locate ffmpeg.")
        quit(1)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.root.mainloop()