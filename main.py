from controller import Controller
from model import Model
from view import View

from shutil import which
from tkinter import messagebox

if __name__ == "__main__":
    if which("ffmpeg") is None:
        messagebox.showerror("Error", "Could not locate ffmpeg.")
        quit(1)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.root.mainloop()