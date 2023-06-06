# Configuration

To change the parameters modify config.json

### Explanation of user defined parameters

* __frame_size__ - size of the frame in number of samples, a frame is a set of samples analyzed fo similarity to a DTMF symbol. Too big size of frame will impact performance due to larger FFT being computed
* __frame_step__ - number of samples between frames (frames can overlap)
* __min_symbol_frames__ - the minimum number of frames that have sufficiently low MAE with a symbol, for that symbol to be considered a reliable DTMF reading
* __max_symbol_break__ - maximum number of frames that have lowest MAE with different symbol / do not result in reliable readint in that sequence
* __min_error_ratio__ - the lowest ratio of symbol MAE to average MAE at which reading will be considered reliable
* __read_entire_signal__ - if set to _true_ all samples will be processed
* __max_frames__ - if __read_entire_signal__ is set to _false_ will process specified number of frames (or less if file is shorter)
* __filepath__ - .wav file to be analyzed

Parameters have default values that will be used if not foung in config.json (except for filepath)