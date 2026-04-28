"""This is a simple wrapper around the WhisperX library"""

import tkinter as tk
import threading
from transcribe import WhisperXWrapper

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhisperX Wrapper")
        self.root.geometry("1000x1000")
        start_button = tk.Button(self.root,
                                 text="Start Transcription", command=self.start_transcription)
        start_button.pack(pady=20)

    def start_transcription(self):
        whisper_transcriber = WhisperXWrapper()
        whisper_transcriber.load_model()
        whisper_thread = threading.Thread(target=whisper_transcriber.transcribe_and_align,
                                          args=("output.mp4",))
        whisper_thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
