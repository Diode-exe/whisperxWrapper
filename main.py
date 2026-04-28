"""This is a simple wrapper around the WhisperX library"""

import torch
from omegaconf.listconfig import ListConfig
from omegaconf.dictconfig import DictConfig

# Tell PyTorch that OmegaConf objects are safe to unpickle
# this is safe because we control the code and data,
# but be cautious if loading from untrusted sources
torch.serialization.add_safe_globals([ListConfig, DictConfig])

# import tkinter as tk
import whisperx

class WhisperXWrapper:
    def __init__(self, model_name: str = "base"):
        # 1. Main transcription model MUST be 'cpu' for CTranslate2 compatibility
        self.device = "cpu"
        # 2. Alignment can often still use 'xpu' if you pass it later
        self.compute_type = "int8" # Best for CPU performance

        print(f"Initializing WhisperX on {self.device}...")
        self.model = whisperx.load_model(
            model_name,
            device=self.device,
            compute_type=self.compute_type
        )

# class GUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("WhisperX Wrapper")
#         self.wrapper = WhisperXWrapper()

if __name__ == "__main__":
    # gui = GUI()
    # gui.root.mainloop()
    wrapper = WhisperXWrapper()
    print(f"Loaded WhisperX model: {wrapper.model_name} on device: {wrapper.device}")
