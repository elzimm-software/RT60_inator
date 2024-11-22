import numpy as np
import pathlib
from scipy.io import wavfile
from matplotlib.figure import Figure
from pydub import AudioSegment


class Model:
    def __init__(self, file=""):
        if file != '':
            self.file = file
            self.convert_mp3()
            self.duration = self.data.shape[0]/self.samplerate
            self.convert_mono()
        else:
            self.file = None
            self.samplerate = None
            self.data = None
            self.duration = None

    def convert_mono(self):
        if len(self.data.shape) > 1:
            self.mono = np.array([( x[0] + x[1] )/2 for x in self.data]).astype(np.int16)

    def convert_mp3(self):
        if pathlib.Path(self.file).suffix == '.mp3':
            AudioSegment.from_mp3(self.file).export("converted.wav", format="wav")
            self.samplerate, self.data = wavfile.read("converted.wav")
            pathlib.Path("converted.wav").unlink()
        else:
            self.samplerate, self.data = wavfile.read(self.file)

    def gen_waveform_figure(self):
        _fig = Figure(figsize=(5, 4), dpi=100)
        _waveform = _fig.add_subplot(111)
        _x = np.linspace(0., self.duration, self.data.shape[0])
        _waveform.plot(_x, self.data[:,0], label="Left channel")
        if len(self.data.shape) > 1:
            _waveform.plot(_x, self.data[:,1], label="Right channel")
        else:
            _waveform.plot(_x, self.data[:,0], label="Right channel")
        _waveform.legend()
        return _fig


