import wave

# Class for reading .wav file

class AudioReader:
    def __init__(self, filename: str):
        
        if not isinstance(filename, str):
            raise TypeError("Filename must be of string type")
        
        self.filename = filename
        self.f_samp = 0
        self.num_samp = 0
        self.signal = []
        self.read_audio_from_file()
        
    def read_audio_from_file(self):
        with wave.open(self.filename, 'r') as wav:
            self.f_samp = wav.getframerate()
            self.num_samp = wav.getnframes()
            self.signal = wav.readframes(self.num_samp)
    
    