#from pydub import AudioSegment

from controller import Controller
from model import Model
from view import View

if __name__ == "__main__":
    model = Model("./test_files/dorm.wav")
    view = View()
    controller = Controller(model, view)
    view.root.mainloop()