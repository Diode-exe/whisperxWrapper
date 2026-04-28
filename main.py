"""This is a simple wrapper around the WhisperX library"""

import tkinter as tk
import threading
from transcribe import WhisperXWrapper

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhisperX Wrapper")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    whisper_transcriber = WhisperXWrapper()
    whisper_transcriber.load_model("base")
    whisper_thread = threading.Thread(target=whisper_transcriber.transcribe_and_align,
                                      args=("dmvsource.mp4",))
    whisper_thread.start()
    gui = GUI()
    gui.run()
