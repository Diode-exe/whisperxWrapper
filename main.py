import tkinter as tk
import whisperx

class WhisperXWrapper:
    def __init__(self, model_name: str = "base", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = whisperx.load_model(model_name, device=device)

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhisperX Wrapper")
        self.wrapper = WhisperXWrapper()

if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()
