import numpy as np

class Root():
    def __init__(self, real, imag, index, color=(0,0,0,)):
        self.real = real
        self.imag = imag
        self.complex = np.complex128(real + imag * 1j)
        self.color = color
        self.radius = 20
        self.index = index