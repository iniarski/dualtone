import numpy as np
import scipy.signal as sig

class ExemplarySymbols:
    
    def __init__(self, frame_size: int, f_samp: int):
        
        # The passed parameters are:
        
        # frame_size - number of samples
        # f_samp - sampling frequency
        
        if not isinstance(frame_size, int):
            raise TypeError("frame_size must be an integer")
        if not isinstance(f_samp, int):
            raise TypeError("f_samp must be an integer")
        
        """"
        This class creates exemplary spectrum of the DTMF symbols:
        
                 1209 Hz  1336 Hz  1477 Hz
        
        697 Hz     1        2        3
        
        770 Hz     4        5        6     
        
        852 Hz     7        8        9
        
        941 Hz     *        0        #
        
        
        Which will be compared with the original signal for similarity
        
        NOTE: Comparison will be done on PSD, not spectrum itself.
              Phase infomation is redundant for DTMF recognition
        
        """

        self.frame_size = frame_size
        self.f_samp = f_samp

        self.vert_freqs = [697, 770, 852, 941]
        self.horz_freqs = [1209, 1336, 1477]
        
        self.symbols = [['1', '2', '3'],
                        ['4', '5', '6'],
                        ['7', '8', '9'],
                        ['*', '0', '#']]        
        
        self.PSDs = list()
        self.symbol_maxima = [[0] * 3] * 4
        
        # Calculating PSD of the symbols
        
        for i in range(4):
            
            # vert_index = i
            temp_row = list()
            
            for j in range(3):
                # horz_index = j
                symbol = self.calculate_symbol_PSD(j, i)
                temp_row.append(symbol)
                
                self.symbol_maxima[i][j] = max(symbol)
                
            self.PSDs.append(temp_row)

    
    def calculate_symbol_PSD(self, horz_index: int, vert_index: int):
        
        if not isinstance(horz_index, int):
            raise TypeError("horz_index must be an integer")
        if not isinstance(vert_index, int):
            raise TypeError("vert_index must be an integer")
        
        freq1 = self.horz_freqs[horz_index] / self.f_samp
        freq2 = self.vert_freqs[vert_index] / self.f_samp
        
        timespace = np.linspace(0, self.frame_size - 1, num = self.frame_size)
        
        # Symbol in time domain
        
        symbol = np.sin(2 * np.pi * freq1 * timespace) + np.sin(2 * np.pi * freq2 * timespace)
        
        
        # Power Spectral Density of the symbol
        (freqspace, PSD) = sig.periodogram(symbol, self.f_samp, scaling='density')
        
        # This piece plots PSD of a symbol
        """
        if horz_index == vert_index == 2:
            import matplotlib.pyplot as plt
            
            plt.figure("Symbol PSD")
            plt.plot(freqspace, PSD, ds = "steps")
            title = "DTMF symbol " + self.symbols[vert_index][horz_index] + " PSD"
            plt.title(title)
            plt.grid(True)
            plt.xlabel("f[Hz]")
            plt.show()
        """
        return PSD
    
