import numpy as np
from scipy.io import wavfile
from matplotlib.figure import Figure


class Model:
    def __init__(self, file=""):
        if file != '':
            #if pathlib.Path(file).suffix == '.mp3':
            #    sound = AudioSegment.from_mp3(file)
            #    sound.export("converted.wav", format="format")
            #    file = "converted.wav"
            self.file = file
            self.samplerate, self.data = wavfile.read(self.file)
            self.duration = round(self.data.shape[0]/self.samplerate, 1)
            if len(self.data.shape) > 1:
                self.mono = np.array([( x[0]+x[1])/2 for x in self.data]).astype(np.int16)
        else:
            self.file = None
            self.samplerate = None
            self.data = None
            self.duration = None

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


