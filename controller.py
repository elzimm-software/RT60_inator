from model import Model


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
