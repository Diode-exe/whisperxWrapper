"""This is a simple wrapper around the WhisperX library"""

import tkinter as tk
from tkinter import ttk
import threading
from transcribe import WhisperXWrapper

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhisperX GUI Wrapper")
        self.root.geometry("500x400")

        # Main Container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # --- Radio Button Section (Model Selection) ---
        self.style_label = ttk.Label(self.main_frame, text="Transcription Mode:", font=("Arial", 10, "bold"))
        self.style_label.pack(anchor="w", pady=(0, 5))

        self.mode_var = tk.StringVar(value="transcribe")

        self.radio_transcribe = ttk.Radiobutton(
            self.main_frame,
            text="Transcribe (Same Language)",
            variable=self.mode_var,
            value="transcribe"
        )
        self.radio_transcribe.pack(anchor="w", padx=10)

        self.radio_translate = ttk.Radiobutton(
            self.main_frame,
            text="Translate (To English)",
            variable=self.mode_var,
            value="translate"
        )
        self.radio_translate.pack(anchor="w", padx=10)

        # --- Separator ---
        self.sep = ttk.Separator(self.main_frame, orient="horizontal")
        self.sep.pack(fill="x", pady=20)

        # --- Action Buttons ---
        self.btn_select_file = ttk.Button(self.main_frame, text="Select Audio/Video File")
        self.btn_select_file.pack(fill="x", pady=5)

        self.btn_run = ttk.Button(self.main_frame, text="Start Processing")
        self.btn_run.pack(fill="x", pady=5)

        self.btn_settings = ttk.Button(self.main_frame, text="Advanced Settings")
        self.btn_settings.pack(fill="x", pady=5)

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
