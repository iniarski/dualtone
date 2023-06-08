import os.path

# clas for parsing configuration

class ConstParser:
    
    def __init__(self, filepath: str):
        
        self.filepath = filepath
        self.constants = None
        
        if not os.path.exists(self.filepath):
            raise FileNotFoundError("No file: " + self.filepath)
        
        if self.filepath.endswith(".json"):
            self.parse_json()
        else:
            raise RuntimeError("Unsupported file type. Try using .json")
    
    def parse_json(self):
        import json
        
        with open(self.filepath) as json_file:
            self.constants = json.load(json_file)
            
        self.suplement_with_defaults()
            
            
    def suplement_with_defaults(self):
        
        # if a value is not specified in the file, the default is used
        
        def set_default(key, value):
            if key not in self.constants:
                self.constants[key] = value
                
        set_default("frame_size", 2500)
        set_default("frame_step", 500)
        set_default("min_symbol_frames", 25)
        set_default("max_symbol_break", 5)
        set_default("min_error_ratio", 1.05)
        set_default("read_entire_signal", True)
        set_default("max_frames", 100)
        
        # execpt for filepath, that does need to be specified
        
        if "filepath" not in self.constants:
            raise RuntimeError("There is no filepath in " + self.filepath
                               + "\n please specify the .wav file")
        
        
        
        