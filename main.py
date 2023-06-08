import numpy as np
from audio import AudioReader
from const import ConstParser
from dtmf import DTMFreader

def main():
    
    # parsing configuration from .json
    const = ConstParser("config.json").constants
    
    # reading audio file
    audio_reader = AudioReader(const["filepath"])
    
    f_samp = audio_reader.f_samp
    signal = np.frombuffer(audio_reader.signal, dtype=np.int16)
    
    # creating DTMFreader and decoding the signal
    dtmf = DTMFreader(const, signal, f_samp)
    result = dtmf.run()
    
    print(result)
        
        
    
    

if __name__ == "__main__":
    main()
