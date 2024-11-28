import numpy as np
import pathlib
from scipy.io import wavfile
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pydub import AudioSegment
from utils import digital_to_decibel, high_pass, low_pass, display_error


class Model:
    def __init__(self, file=""):
        if file != '':
            self.file = file
            if self.convert_mp3():
                self.duration = self.data.shape[0]/self.samplerate
                self.low_freq, self.mid_freq, self.high_freq = self.split_freq()
                self.low_rt60 = self.compute_rt60_time(self.low_freq)
                self.mid_rt60 = self.compute_rt60_time(self.mid_freq)
                self.high_rt60 = self.compute_rt60_time(self.high_freq)
                self.combined_rt60 = self.compute_rt60_time(self.data)
                print(self.combined_rt60)
                print(self.low_rt60, self.mid_rt60, self.high_rt60)
            else:
                display_error("Invalid file type.")
                self.file = None
                self.samplerate = None
                self.data = None
                self.duration = None
                self.low_freq,self.mid_freq,self.high_freq = None, None, None
                self.low_rt60, self.mid_rt60, self.high_rt60 = None, None, None
                self.combined_rt60 = None
        else:
            self.file = None
            self.samplerate = None
            self.data = None
            self.duration = None
            self.low_freq, self.mid_freq, self.high_freq = None, None, None
            self.low_rt60, self.mid_rt60, self.high_rt60 = None, None, None
            self.combined_rt60 = None

    def split_freq(self):
        _mono = Model.convert_mono(self.data)
        _low = low_pass(high_pass(_mono, 1, self.samplerate), 1000, self.samplerate)
        _mid = low_pass(high_pass(_mono, 1001, self.samplerate), 3000, self.samplerate)
        _high = low_pass(high_pass(_mono, 3001, self.samplerate), 20000, self.samplerate)
        return _low, _mid, _high

    def compute_rt60_time(self, signal):
        _mono = Model.convert_mono(signal)
        _decibel = np.array([(digital_to_decibel(x)) for x in _mono]).astype(np.int16)
        _max = np.max(_decibel)
        _max_index = np.where(_decibel == _max)[0][0]
        _5_under_index = np.where(_decibel[_max_index:] == _max - 5)[0][0]
        _25_under_index = np.where(_decibel[_5_under_index:] == _max - 25)[0][0]
        _rt20_time = (_25_under_index - _5_under_index) / self.samplerate
        return _rt20_time * 3

    @staticmethod
    def convert_mono(signal):
        if len(signal.shape) > 1:
            return np.array([( x[0] + x[1] )/2 for x in signal]).astype(np.int16)
        else:
            return signal

    def convert_mp3(self):
        ext = pathlib.Path(self.file).suffix.lower()
        if ext == '.mp3':
            AudioSegment.from_mp3(self.file).export("converted.wav", format="wav")
            self.samplerate, self.data = wavfile.read("converted.wav")
            pathlib.Path("converted.wav").unlink()
            return True
        elif ext == '.wav':
            self.samplerate, self.data = wavfile.read(self.file)
            return True
        else:
            return False

    def gen_waveform_figure(self):
        _fig = Figure(figsize=(5, 4), dpi=100)
        _waveform = _fig.add_subplot(111)
        _x = np.linspace(0., self.duration, self.data.shape[0])
        if len(self.data.shape) > 1:
            _waveform.plot(_x, self.data[:,0], label="Left channel")
            _waveform.plot(_x, self.data[:,1], label="Right channel")
            _waveform.legend()
            _waveform.set_xlabel("Time (s)")
            _waveform.set_ylabel("Amplitude")
        else:
            _waveform.plot(_x, self.data)
        return _fig


    def gen_intensity_figure(self):
        fig, ax = plt.subplots()
        _mono = Model.convert_mono(self.data)
        spectrum, freqs, t, im = ax.specgram(_mono, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = fig.colorbar(im, ax=ax)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        return fig