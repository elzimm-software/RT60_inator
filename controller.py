from model import Model


class Controller:
    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        view.set_controller(self)

    def gen_waveform_figure(self):
        return self.model.gen_waveform_figure()

    def gen_intensity_figure(self):
        return self.model.gen_intensity_figure()

    def import_clicked(self, filename):
        new_model = Model(filename)
        if new_model.file is not None:
            self.model = new_model
            self.view.set_active_file(self.model.file, self.model.duration)
            self.view.update_waveform()
            self.view.update_intensity()

    def get_resonant_frequency(self):
        return self.model.get_resonant_frequency()

    def get_difference(self):
        return self.model.combined_rt60 - .5