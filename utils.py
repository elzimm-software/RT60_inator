import numpy as np
from scipy.signal import butter, filtfilt
from tkinter import messagebox

def display_error(message):
    messagebox.showerror("Error", message)

def low_pass(signal, cut, fs):
    nyq = 0.5 * fs
    normal_cut = cut / nyq
    b, a = butter(4, normal_cut, btype='lowpass')
    return filtfilt(b, a, signal)

def high_pass(signal, cut, fs):
    nyq = 0.5 * fs
    normal_cut = cut / nyq
    b, a = butter(4, normal_cut, btype='highpass')
    return filtfilt(b, a, signal)

def digital_to_decibel(signal: int):
    if signal > 0:
        return np.log10(signal) * 10
    else:
        return 0

def decibel_to_digital(decibel):
    return pow(10, decibel / 10)