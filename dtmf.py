from multiprocessing import Pool
from statistics import mode
from symbols import ExemplarySymbols
import scipy.signal as sig
import numpy as np

# class for decoding DTMF signal

# signal is divided into frames (n samples)
# for each frame its PSD is calculated and compared with pure symbols (symbols.py)
# then the resulting sequence is parsed

class DTMFreader:
    def __init__(self, consts, signal, f_samp):
        # passed parameters
        # consts - dictionary containing config values (const.py)
        # signal - audio signal to be anlyzed
        # f_samp - sampling fequency
        
        self.signal = signal
        
        self.frame_size = consts["frame_size"]
        self.frame_step = consts["frame_step"]
        self.min_symbol_frames = consts["min_symbol_frames"]
        self.max_symbol_break = consts["max_symbol_break"]
        self.min_error_ratio = consts["min_error_ratio"]
        self.read_entire_signal = consts["read_entire_signal"]
        self.max_frames = consts["max_frames"]
        
        self.symbols = ExemplarySymbols(self.frame_size, f_samp)
        
    # run method performs all the tasks and returns reqovered sequence
        
    def run(self):
        res = self.read_signal()
    
        reading = list()
    
        for i in res:
            reading.append(i["symbol"])
            
        self.sequence = self.parse_symbols(reading)
        
        return ''.join(self.sequence)
    
    # parse_symbols method coverts result of reading frames into a sequence
        
    def parse_symbols(self, read_results):
                
        symbols_parsed = list()

        i = 0
        n_of_symbols = len(read_results)
        
        while i < n_of_symbols - self.min_symbol_frames:
            
            # analyzing fragment of reading result
            
            analyzed_fragment = read_results[i : i + self.min_symbol_frames]
            most_frequent_symbol = mode(analyzed_fragment)
            
            # whent the most frequent symbol is None the analyzed fragment is too noisy to recover
            
            if most_frequent_symbol == None:
                i += 1
                continue
            
            symbol_count = analyzed_fragment.count(most_frequent_symbol)
            
            # if there are enough occurences of the most frequent symbol in the fragment
            # the symbol is considered to be present in the original signal
            
            if symbol_count >= self.min_symbol_frames - self.max_symbol_break:
                # symbol was read
                symbols_parsed.append(most_frequent_symbol)
                i += self.min_symbol_frames
                
                # if the symbol is present in the next frames it is considered to be the same symbol,
                # and the following reads are skipped
                
                try:
                    while read_results[i : i + self.max_symbol_break].count(most_frequent_symbol) >= self.max_symbol_break // 2:
                        i += self.max_symbol_break // 2
                except IndexError:
                    pass
                    
            
            i += 1
                        
            
        return symbols_parsed
    
    # read_signal method reads the frames in parallel
    
    def read_signal(self):
        
        # determining the number of frames to be read
        
        signal_length_in_frames = int((len(self.signal) - self.frame_size) / self.frame_step)
        
        if self.read_entire_signal:
            n_of_frames = signal_length_in_frames
        else:
            n_of_frames = self.max_frames if self.max_frames <= signal_length_in_frames else signal_length_in_frames
        
        
        # defining function for running in parallel        
        global process_frame
        def process_frame(i):
            frame_index = i * self.frame_step
            return self.read_frame(frame_index)
        
        pool = Pool(processes = 16)
            
        frames_result = pool.map(process_frame, range(n_of_frames))
        return frames_result
    
    # read_frame method reads individual frame and compares it to clear DTMF symbols
        
    def read_frame(self, frame_index: int):
        
        if not isinstance(frame_index, int):
            raise TypeError("frame_index must be int")
        
        # dafining the frame and computing its PSD
        frame = self.signal[frame_index : frame_index + self.frame_size]
        (freqspace, frame_PSD) = sig.periodogram(frame, self.symbols.f_samp, scaling='density')
        frame_max = max(frame_PSD)
        
        errors = list()
        
        # comparing the frame to all DTMF symbols
        
        for i in range(12):
            horz_index = i % 3
            vert_index = i // 3
            
            # to compute MAE correctly the frame is scaled so its max values is the same as the DTMF symbol
            scalar = self.symbols.symbol_maxima[vert_index][horz_index] / frame_max
            
            # mean absolute error
            mae = np.mean(np.abs(self.symbols.PSDs[vert_index][horz_index] - frame_PSD * scalar))
            errors.append(mae)

        
        # characteristics of the mae
        mean_error = np.mean(errors)
        min_error = min(errors)
        mean_to_min_err = mean_error / min_error
        
        # if mean_to_min_err is larger than the value specified in config,
        # the symbol is considered to be read reliably 
        if mean_to_min_err >= self.min_error_ratio:
            index_of_min = errors.index(min_error)
            symbol_read = self.symbols.symbols[index_of_min // 3][index_of_min % 3]
        else:
            symbol_read = None
            
        return {
            "symbol" : symbol_read,
            "error_ratio" : mean_to_min_err
        }        
