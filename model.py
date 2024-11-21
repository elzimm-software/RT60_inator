import numpy as np
from scipy.io import wavfile


class Model:
    def __init__(self, file):
        if file != '':
            #if pathlib.Path(file).suffix == '.mp3':
            #    sound = AudioSegment.from_mp3(file)
            #    sound.export("converted.wav", format="format")
            #    file = "converted.wav"
            self.file = file
            self.samplerate, self.data = wavfile.read(self.file)
            self.duration = round(self.data.shape[0]/self.samplerate, 1)
            if len(self.data.shape) > 1:
                self.data = np.array([( x[0]+x[1])/2 for x in self.data]).astype(np.int16)
        else:
            self.file = None
            self.samplerate = None
            self.data = None
            self.duration = None
