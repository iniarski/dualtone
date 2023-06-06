from multiprocessing import Pool
from statistics import mode
from symbols import ExemplarySymbols
import scipy.signal as sig
import numpy as np


class DTMFreader:
    def __init__(self, consts, signal, f_samp):
        
        self.signal = signal
        
        self.frame_size = consts["frame_size"]
        self.frame_step = consts["frame_step"]
        self.min_symbol_frames = consts["min_symbol_frames"]
        self.max_symbol_break = consts["max_symbol_break"]
        self.min_error_ratio = consts["min_error_ratio"]
        self.read_entire_signal = consts["read_entire_signal"]
        self.max_frames = consts["max_frames"]
        
        self.symbols = ExemplarySymbols(self.frame_size, f_samp)
        
    def run(self):
        res = self.read_signal()
    
        reading = list()
    
        for i in res:
            reading.append(i["symbol"])
            
        self.sequence = self.parse_symbols(reading)
        
        return ''.join(self.sequence)
        
    def parse_symbols(self, read_results):
                
        symbols_parsed = list()

        i = 0
        n_of_symbols = len(read_results)
        
        while i < n_of_symbols - self.min_symbol_frames:
            
            analyzed_fragment = read_results[i : i + self.min_symbol_frames]
            most_frequent_symbol = most_frequent(analyzed_fragment)
            
            if most_frequent_symbol == None:
                i += 1
                continue
            
            symbol_count = analyzed_fragment.count(most_frequent_symbol)
            
            if symbol_count >= self.min_symbol_frames - self.max_symbol_break:
                # symbol was read
                symbols_parsed.append(most_frequent_symbol)
                i += self.min_symbol_frames
                
                try:
                    while read_results[i : i + self.max_symbol_break].count(most_frequent_symbol) >= self.max_symbol_break // 2:
                        i += self.max_symbol_break // 2
                except IndexError:
                    pass
                    
            
            i += 1
                        
            
        return symbols_parsed
    
    
    def read_signal(self):
        
        signal_length_in_frames = int((len(self.signal) - self.frame_size) / self.frame_step)
        
        if self.read_entire_signal:
            n_of_frames = signal_length_in_frames
        else:
            n_of_frames = self.max_frames if self.max_frames <= signal_length_in_frames else signal_length_in_frames
                
        global process_frame
        def process_frame(i):
            frame_index = i * self.frame_step
            return self.read_frame(frame_index)
        
        pool = Pool(processes = 16)
            
        frames_result = pool.map(process_frame, range(n_of_frames))
        return frames_result
        
    def read_frame(self, frame_index: int):
        
        if not isinstance(frame_index, int):
            raise TypeError("frame_index must be int")
        
        
        frame = self.signal[frame_index : frame_index + self.frame_size]
        (freqspace, frame_PSD) = sig.periodogram(frame, self.symbols.f_samp, scaling='density')
        frame_max = max(frame_PSD)
        
        errors = list()
        
        for i in range(12):
            horz_index = i % 3
            vert_index = i // 3
            
            scalar = self.symbols.symbol_maxima[vert_index][horz_index] / frame_max
            
            # mean absolute error
            mae = np.mean(np.abs(self.symbols.PSDs[vert_index][horz_index] - frame_PSD * scalar))
            errors.append(mae)

        
        mean_error = np.mean(errors)
        min_error = min(errors)
        mean_to_min_err = mean_error / min_error
        
        if mean_to_min_err >= self.min_error_ratio:
            index_of_min = errors.index(min_error)
            symbol_read = self.symbols.symbols[index_of_min // 3][index_of_min % 3]
        else:
            symbol_read = None
            
        return {
            "symbol" : symbol_read,
            "error_ratio" : mean_to_min_err
        }        

        
def most_frequent(List):
    return mode(List)