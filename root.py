class Root():
    def __init__(self, real, imag, color=(0,0,0,)):
        self.real = real
        self.imag = imag
        self.complex = real + imag * 1j
        self.color = color
        self.radius = 20