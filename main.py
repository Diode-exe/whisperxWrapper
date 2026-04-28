# import os

# # 1. Disable the problematic automatic backend loader
# os.environ["TORCH_DEVICE_BACKEND_AUTOLOAD"] = "0"

# # 2. Import torch first
# import torch

# # 3. Manually initialize the Intel backend
# try:
#     import intel_extension_for_pytorch as ipex
# except ImportError:
#     pass

# 4. Now import your other libraries
# import tkinter as tk
import whisperx

class WhisperXWrapper:
    def __init__(self, model_name: str = "base", device: str = "xpu"):
        self.model_name = model_name
        self.device = device
        self.model = whisperx.load_model(model_name, device=device)

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
