import numpy as np
import pathlib
from scipy.io import wavfile
from scipy.signal import welch
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pydub import AudioSegment
from utils import digital_to_decibel, high_pass, low_pass, display_error


class Model:
    def __init__(self, file=""):
        if file != '':  # If a file is passed
            self.file = file
            if self.convert_mp3():  # If the file is valid
                self.duration = self.data.shape[0] / self.samplerate  # Calculate duration
                self.low_freq, self.mid_freq, self.high_freq = self.split_freq()  # Split frequencies
                self.low_rt60 = self.compute_rt60_time(self.low_freq)  # Low frequency RT60
                self.mid_rt60 = self.compute_rt60_time(self.mid_freq)  # Mid frequency RT60
                self.high_rt60 = self.compute_rt60_time(self.high_freq)  # High frequency RT60
                self.combined_rt60 = self.compute_rt60_time(self.data)  # Combined RT60 for all frequencies
                print(f"File loaded: {self.file}")
                print(f"Low RT60: {self.low_rt60}, Mid RT60: {self.mid_rt60}, High RT60: {self.high_rt60}")
                print(f"Combined RT60: {self.combined_rt60}")
            else:
                print("Invalid file type")
                self.file = None
                self.samplerate = None
                self.data = None
                self.duration = None
                self.low_freq, self.mid_freq, self.high_freq = None, None, None
                self.low_rt60, self.mid_rt60, self.high_rt60 = None, None, None
                self.combined_rt60 = None
        else:
            print("No file provided")
            self.file = None
            self.samplerate = None
            self.data = None
            self.duration = None
            self.low_freq, self.mid_freq, self.high_freq = None, None, None
            self.low_rt60, self.mid_rt60, self.high_rt60 = None, None, None
            self.combined_rt60 = None

    def split_freq(self):
        _mono = Model.convert_mono(self.data)  # Convert stereo to mono if necessary
        _low = low_pass(high_pass(_mono, 1, self.samplerate), 1000,
                        self.samplerate)  # Low-frequency band (1 Hz to 1000 Hz)
        _mid = low_pass(high_pass(_mono, 1001, self.samplerate), 3000,
                        self.samplerate)  # Mid-frequency band (1001 Hz to 3000 Hz)
        _high = low_pass(high_pass(_mono, 3001, self.samplerate), 20000,
                         self.samplerate)  # High-frequency band (3001 Hz to 20000 Hz)
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
            return np.array([(x[0] + x[1]) / 2 for x in signal]).astype(np.int16)
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
            _waveform.plot(_x, self.data[:, 0], label="Left channel")
            _waveform.plot(_x, self.data[:, 1], label="Right channel")
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

    def gen_low_freq_figure(self):
        fig, ax = plt.subplots()
        _x = np.linspace(0., self.duration, self.low_freq.shape[0])
        ax.plot(_x, self.low_freq)
        ax.set_title("Low Frequency")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig

    def gen_mid_freq_figure(self):
        fig, ax = plt.subplots()
        _x = np.linspace(0., self.duration, self.mid_freq.shape[0])
        ax.plot(_x, self.mid_freq)
        ax.set_title("Mid Frequency")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig

    def gen_high_freq_figure(self):
        fig, ax = plt.subplots()
        _x = np.linspace(0., self.duration, self.high_freq.shape[0])
        ax.plot(_x, self.high_freq)
        ax.set_title("High Frequency")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig

    def gen_combined_freq_figure(self):
        fig, ax = plt.subplots()
        _x = np.linspace(0., self.duration, self.data.shape[0])
        ax.plot(_x, self.data)
        ax.set_title("Combined Frequency")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig

    def get_resonant_frequency(self):
        _mono = Model.convert_mono(self.data)
        frequencies, power = welch(_mono, self.samplerate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        return dominant_frequency
