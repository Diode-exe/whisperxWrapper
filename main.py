"""This is a simple wrapper around the WhisperX library"""

import os
import torch
# from omegaconf.listconfig import ListConfig
# from omegaconf.dictconfig import DictConfig

os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

# Tell PyTorch that OmegaConf objects are safe to unpickle
# this is safe because we control the code and data,
# but be cautious if loading from untrusted sources
# torch.serialization.add_safe_globals([ListConfig, DictConfig])

# import tkinter as tk
import whisperx

class WhisperXWrapper:
    def __init__(self, model_name: str = "base"):
        self.device = "cpu"       # Transcription engine (CTranslate2)
        self.align_device = "xpu" # Alignment engine (PyTorch)
        self.compute_type = "int8"

        print(f"Loading Transcription model on {self.device}...")
        self.model = whisperx.load_model(
            model_name,
            device=self.device,
            compute_type=self.compute_type
        )

    def transcribe_and_align(self, audio_path):
        # 1. Transcribe (CPU-bound)
        audio = whisperx.load_audio(audio_path)
        result = self.model.transcribe(audio, batch_size=16)

        # 2. Align (GPU-bound on your Arc iGPU!)
        print(f"Aligning on {self.align_device}...")
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=self.align_device
        )

        # This part will now use those 1.12 GiB XPU wheels you installed!
        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            self.align_device,
            return_char_alignments=False
        )
        return result

# class GUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("WhisperX Wrapper")
#         self.wrapper = WhisperXWrapper()

if __name__ == "__main__":
    # gui = GUI()
    # gui.root.mainloop()
    wrapper = WhisperXWrapper()
    # print(f"Loaded WhisperX model: {wrapper.model_name} on device: {wrapper.device}")
    print("WhisperX model loaded successfully!")
