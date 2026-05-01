"""This is a simple wrapper around the WhisperX library"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading

from transcribe import WhisperXWrapper
from config import Config

configuration = Config()

class GUI:
    def __init__(self, whisper_x_ref=None):
        self.file_to_process = None
        self.whisper_thread = None
        self.load_model_thread = None
        self.is_model_loaded = False
        self.check_vars = []

        self.whisper_x_ref = whisper_x_ref
        self.root = tk.Tk()
        self.root.title("WhisperX GUI Wrapper")
        self.root.geometry("500x500")

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

        self.diarize_var = tk.BooleanVar(value=False)
        self.diarize = ttk.Checkbutton(
            self.main_frame,
            text="Enable Speaker Diarization",
            variable=self.diarize_var
        )
        self.diarize.pack(anchor="w", padx=10)

        # self.radio_translate = ttk.Radiobutton(
        #     self.main_frame,
        #     text="Translate (To English)",
        #     variable=self.mode_var,
        #     value="translate"
        # )
        # self.radio_translate.pack(anchor="w", padx=10)

        self.language_label = ttk.Label(self.main_frame,
                                        text="Select Language:", font=("Arial", 10, "bold"))
        self.language_label.pack(anchor="e", padx=30)

        self.language_var = tk.StringVar(value="English")
        self.language_select = ttk.Combobox(
            self.main_frame,
            textvariable=self.language_var,
            values=configuration.supported_languages_longhand,
            state="readonly"  # prevents manual text entry
        )
        self.language_select.pack(anchor="e")

        # --- Model Selection Dropdown ---
        self.model_select_var = tk.StringVar(value=configuration.model_name)
        self.model_select_label = ttk.Label(self.main_frame,
                                            text="Select Model:", font=("Arial", 10, "bold"))
        self.model_select_label.pack(anchor="e", padx=55)

        self.model_select = ttk.Combobox(
            self.main_frame,
            textvariable=self.model_select_var,
            values=configuration.models,
            state="readonly"  # prevents manual text entry
        )
        self.model_select.pack(anchor="e")

        # --- Output Format Checkboxes ---
        self.output_check_frame = ttk.Frame(self.main_frame)
        self.output_check_frame.pack(fill="x", pady=20, anchor="w")
        self.output_check_label_frame = ttk.LabelFrame(self.output_check_frame,
                                                       text="Output Formats", padding="10")
        self.output_check_label_frame.pack(anchor="w", padx=10)

        self.all_formats_var = tk.BooleanVar(value=True)
        self.all_formats_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save in All Formats",
            variable=self.all_formats_var,
            command=self.toggle_all_checkboxes
        )
        self.all_formats_check.pack(anchor="w", padx=10)

        self.srt_check_var = tk.BooleanVar(value=True)
        self.check_vars.append(self.srt_check_var)
        self.srt_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save as .srt",
            variable=self.srt_check_var,
            command=self.monitor_all_checkbox_state
        )
        self.srt_check.pack(anchor="w", padx=10)

        self.vtt_check_var = tk.BooleanVar(value=True)
        self.check_vars.append(self.vtt_check_var)
        self.vtt_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save as .vtt",
            variable=self.vtt_check_var,
            command=self.monitor_all_checkbox_state
        )
        self.vtt_check.pack(anchor="w", padx=10)

        self.txt_check_var = tk.BooleanVar(value=True)
        self.check_vars.append(self.txt_check_var)
        self.txt_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save as .txt",
            variable=self.txt_check_var,
            command=self.monitor_all_checkbox_state
        )
        self.txt_check.pack(anchor="w", padx=10)

        self.json_check_var = tk.BooleanVar(value=True)
        self.check_vars.append(self.json_check_var)
        self.json_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save as .json",
            variable=self.json_check_var,
            command=self.monitor_all_checkbox_state
        )
        self.json_check.pack(anchor="w", padx=10)

        self.tsv_check_var = tk.BooleanVar(value=True)
        self.check_vars.append(self.tsv_check_var)
        self.tsv_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save as .tsv",
            variable=self.tsv_check_var,
            command=self.monitor_all_checkbox_state
        )
        self.tsv_check.pack(anchor="w", padx=10)

        # # --- Separator ---
        # self.sep = ttk.Separator(self.main_frame, orient="horizontal")
        # self.sep.pack(fill="x", pady=20)

        # --- Action Buttons ---
        self.btn_select_file = ttk.Button(self.main_frame, text="Select Audio/Video File",
                                          command=self.select_file)
        self.btn_select_file.pack(fill="x", pady=5)

        self.btn_run = ttk.Button(self.main_frame, text="Start Processing",
                                  command=self.start_transcription)
        self.btn_run.pack(fill="x", pady=5)

        # self.btn_settings = ttk.Button(self.main_frame, text="Advanced Settings")
        # self.btn_settings.pack(fill="x", pady=5)

    def start_transcription(self):
        if not self.file_to_process:
            messagebox.showwarning("No File Selected", "Please select a file to process.")
            return

        # Disable the run button so they don't click it twice
        self.btn_run.config(state="disabled")
        self.btn_run.config(text="Loading Model...")

        # Start loading the model in a background thread
        # Note: Added a wrapper to set the flag when done
        def load_task():
            self.whisper_x_ref.load_model(model_name=self.model_select_var.get())
            self.is_model_loaded = True

        self.load_model_thread = threading.Thread(target=load_task, daemon=True)
        self.load_model_thread.start()

        # Start the "polling" function to wait for the thread without .join()
        self.monitor_load_thread()

    def monitor_load_thread(self):
        """Checks if the model loading thread is finished every 100ms."""
        if self.load_model_thread.is_alive():
            # Thread is still working, check again in 100ms
            self.root.after(100, self.monitor_load_thread)
        else:
            # Model is loaded! Now start the actual transcription
            self.btn_run.config(text="Transcribing...")
            self.run_actual_transcription()

    def run_actual_transcription(self):
        output_formats = [fmt for fmt, var in [
            ("srt", self.srt_check_var), ("vtt", self.vtt_check_var),
            ("txt", self.txt_check_var), ("json", self.json_check_var),
            ("tsv", self.tsv_check_var)
        ] if var.get()]

        def trans_task():
            self.whisper_x_ref.transcribe_and_align(
                self.file_to_process,
                language=self.language_var.get(),
                diarize=self.diarize_var.get(),
                output_formats=output_formats
            )
            # Re-enable the UI on completion
            self.root.after(0, lambda: self.btn_run.config(state="normal", text="Start Processing"))
            self.root.after(0, lambda: messagebox.showinfo("Done", "Transcription Complete!"))

        self.whisper_thread = threading.Thread(target=trans_task, daemon=True)
        self.whisper_thread.start()

    def select_file(self):
        self.file_to_process = filedialog.askopenfilename(
            title="Select Audio/Video File",
            filetypes=[("Audio/Video Files", "*.mp4 *.mp3 *.wav *.m4a"), ("All Files", "*.*")]
        )

    def toggle_all_checkboxes(self):
        if self.all_formats_var.get():
            for var in self.check_vars:
                var.set(True)
        else:
            for var in self.check_vars:
                var.set(False)

    def monitor_all_checkbox_state(self):
        if all(var.get() for var in self.check_vars):
            self.all_formats_var.set(True)
        else:
            self.all_formats_var.set(False)

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Interrupted by user. Closing application...")
            self.root.quit()
            self.root.destroy()

if __name__ == "__main__":
    whisper_transcriber = WhisperXWrapper()
    gui = GUI(whisper_x_ref=whisper_transcriber)
    gui.run()
