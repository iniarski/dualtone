import numpy as np
from audio import AudioReader
from const import ConstParser
from dtmf import DTMFreader

def main():
    
    const = ConstParser("config.json").constants
    
    audio_reader = AudioReader(const["filepath"])
    
    f_samp = audio_reader.f_samp
    signal = np.frombuffer(audio_reader.signal, dtype=np.int16)
    
    dtmf = DTMFreader(const, signal, f_samp)
    result = dtmf.run()
    
    print(result)
        
        
    
    

if __name__ == "__main__":
    main()
