from model import Model


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        view.set_controller(self)

    def import_clicked(self, filename):
        print(f"Controller received filename: {filename}")  # Debugging line
        new_model = Model(filename)
        if new_model.file is not None:  # Check if the file is valid
            self.model = new_model  # Set the model to the new model
            self.view.set_active_file(self.model.file, self.model.duration)  # Update the file display label
            self.view.update_waveform(self.model.gen_waveform_figure())  # Update the waveform graph
            self.view.update_intensity(self.model.gen_intensity_figure())  # Update the intensity graph
            self.view.update_low_freq(self.model.gen_low_freq_figure())  # Update the low-frequency graph
            self.view.update_mid_freq(self.model.gen_mid_freq_figure())  # Update the mid-frequency graph
            self.view.update_high_freq(self.model.gen_high_freq_figure())  # Update the high-frequency graph
            self.view.update_combined_freq(self.model.gen_combined_freq_figure())  # Update the combined frequency graph
            self.view.update_analysis(f"Low RT60: {self.model.low_rt60}\nMid RT60: {self.model.mid_rt60}\nHigh RT60: {self.model.high_rt60}\nCombined RT60: {self.model.combined_rt60}")  # Update analysis
        else:
            print("Failed to load file")  # Debugging line

    def gen_waveform_figure(self):
        return self.model.gen_waveform_figure()

    def gen_intensity_figure(self):
        return self.model.gen_intensity_figure()

    def get_resonant_frequency(self):
        return self.model.get_resonant_frequency()

    def get_difference(self):
        if self.model.combined_rt60 is not None:
            return self.model.combined_rt60 - 0.5
        else:
            return 0  # or some default value when RT60 is not available