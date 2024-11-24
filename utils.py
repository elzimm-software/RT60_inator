import numpy as np


def digital_to_decibel(signal: int):
    if signal > 0:
        return np.log10(signal) * 10
    else:
        return 0

def decibel_to_digital(decibel):
    return pow(10, decibel / 10)