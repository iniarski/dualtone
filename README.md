# Dualatone Recognition

This Python (using numpy and scipy) program will analyze .wav file looking for DTMF patterns and return recovered sequence. 


Dual Tone Multi Frequency (DTMF) is analogue signalization system. A symbol is mapped to two tones (frequencies) as shown below:

```
                 1209 Hz  1336 Hz  1477 Hz
        
        697 Hz     1        2        3
        
        770 Hz     4        5        6     
        
        852 Hz     7        8        9
        
        941 Hz     *        0        #
        
```

---

## Working of the program

* reading user-defined parameters ([more about them](CONFIG.md))
* calculating exemplary Power Specral Densities (PSDs) of pure DTMF symbols (two sinewaves without noise) for each DTMF symbol
* for each frame (n consecutive samples) of the signal read from .wav file the program will calculate mean absolute error (MAE) between frame's PSD and PSDs of DTMF symbols
* if MAE of a symbol is sufficently small compared to average MAE, the sympol with the lowest MAE will be read
* the results of the reading are parsed
* recovered sequence is returned
