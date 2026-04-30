"""This is a simple wrapper around the WhisperX library"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading

from transcribe import WhisperXWrapper

class GUI:
    def __init__(self, whisper_x_ref=None):
        self.file_to_process = None

        self.whisper_x_ref = whisper_x_ref
        self.root = tk.Tk()
        self.root.title("WhisperX GUI Wrapper")
        self.root.geometry("500x400")

        # self.style = ttk.Style(self.root)
        # self.style.theme_use('classic')

        # Main Container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # --- Radio Button Section (Model Selection) ---
        self.style_label = ttk.Label(self.main_frame,
                                     text="Transcription Mode:", font=("Arial", 10, "bold"))
        self.style_label.pack(anchor="w", pady=(0, 5))

        self.mode_var = tk.StringVar(value="transcribe")

        self.radio_transcribe = ttk.Radiobutton(
            self.main_frame,
            text="Transcribe (Same Language)",
            variable=self.mode_var,
            value="transcribe"
        )
        self.radio_transcribe.pack(anchor="w", padx=10)

        # self.radio_translate = ttk.Radiobutton(
        #     self.main_frame,
        #     text="Translate (To English)",
        #     variable=self.mode_var,
        #     value="translate"
        # )
        # self.radio_translate.pack(anchor="w", padx=10)
        
        self.language = tk.StringVar(value="option1")
        self.language_select = ttk.Combobox(
            self.main_frame,
            textvariable=self.language,
            values=["option1", "option2", "option3"],
            state="readonly"  # prevents manual text entry
        )
        self.language_select.pack(anchor="e")

        # --- Separator ---
        self.sep = ttk.Separator(self.main_frame, orient="horizontal")
        self.sep.pack(fill="x", pady=20)

        # --- Action Buttons ---
        self.btn_select_file = ttk.Button(self.main_frame, text="Select Audio/Video File",
                                          command=self.select_file)
        self.btn_select_file.pack(fill="x", pady=5)

        self.btn_run = ttk.Button(self.main_frame, text="Start Processing",
                                  command=self.start_transcription)
        self.btn_run.pack(fill="x", pady=5)

        self.btn_settings = ttk.Button(self.main_frame, text="Advanced Settings")
        self.btn_settings.pack(fill="x", pady=5)

    def start_transcription(self):
        if not self.file_to_process:
            messagebox.showwarning("No File Selected", "Please select a file to process.")
            return

        self.whisper_x_ref.load_model()
        whisper_thread = threading.Thread(target=lambda: self.whisper_x_ref.transcribe_and_align(self.file_to_process, self.mode_var.get()))
        whisper_thread.start()

    def select_file(self):
        self.file_to_process = filedialog.askopenfilename(
            title="Select Audio/Video File",
            filetypes=[("Audio/Video Files", "*.mp4 *.mp3 *.wav *.m4a"), ("All Files", "*.*")]
        )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    whisper_transcriber = WhisperXWrapper()
    gui = GUI(whisper_x_ref=whisper_transcriber)
    gui.run()
