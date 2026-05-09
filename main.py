"""This is a simple wrapper around the WhisperX library"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import threading

from transcribe import WhisperXWrapper
from config import Config
from advanced_settings import AdvancedSettingsWindow

configuration = Config()

class GUI:
    """Graphical User Interface for the WhisperXWrapper application.
    This class uses tkinter to create a user-friendly interface for selecting audio/video files,
    choosing transcription options, and managing the transcription process. It interacts with a
    `WhisperXWrapper` instance to perform model loading and transcription tasks in background threads,
    ensuring the UI remains responsive. The GUI also includes an advanced settings window for
    additional configuration options."""

    def __init__(self, whisper_x_ref=None):
        """Initialize the GUI and its widgets.

        Args:
            whisper_x_ref: Optional reference to a `WhisperXWrapper` instance
                used to perform model loading and transcription operations.

        This sets up all tkinter widgets, default state variables, and
        prepares the advanced settings window.
        """
        self.file_to_process = None
        self.whisper_thread = None
        self.load_model_thread = None
        self.is_model_loaded = False
        self.check_vars = []

        self.whisper_x_ref = whisper_x_ref
        self.root = tk.Tk()
        self.root.title("WhisperX GUI Wrapper")
        self.root.geometry("500x600")

        self.advanced_settings_window = AdvancedSettingsWindow(self.root, configuration)

        # self.style = ttk.Style(self.root)
        # self.style.theme_use('classic')

        # Main Container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # --- Mode Options ---
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

        self.radio_translate = ttk.Radiobutton(
            self.main_frame,
            text="Translate (To English)",
            variable=self.mode_var,
            value="translate"
        )
        self.radio_translate.pack(anchor="w", padx=10)

        self.diarize_var = tk.BooleanVar(value=False)
        self.diarize = ttk.Checkbutton(
            self.main_frame,
            text="Enable Speaker Diarization",
            variable=self.diarize_var
        )
        self.diarize.pack(anchor="w", padx=10)

        self.alignment_var = tk.BooleanVar(value=True)
        self.alignment = ttk.Checkbutton(
            self.main_frame,
            text="Enable Phoneme Alignment",
            variable=self.alignment_var,
            command=self.warn_no_alignment
        )
        self.alignment.pack(anchor="w", padx=10)

         # --- Language Selection Dropdown ---
        self.language_label = ttk.Label(self.main_frame,
                                        text="Select Language:", font=("Arial", 10, "bold"))
        self.language_label.pack(anchor="e", padx=30)

        self.language_var = tk.StringVar(value="English")

        self.auto_detect_option_var = tk.BooleanVar(value=True)
        self.auto_detect_check = ttk.Checkbutton(
            self.main_frame,
            text="Auto-Detect Language",
            variable=self.auto_detect_option_var,
            command=lambda: self.language_select.config(state="disabled" if self.auto_detect_option_var.get() else "readonly")
        )
        self.auto_detect_check.pack(anchor="e", padx=2)

        self.language_select = ttk.Combobox(
            self.main_frame,
            textvariable=self.language_var,
            values=configuration.supported_languages_longhand,
            state="disabled" if self.auto_detect_option_var.get() else "readonly"  # prevents manual text entry
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

        self.aud_check_var = tk.BooleanVar(value=True)
        self.check_vars.append(self.aud_check_var)
        self.aud_check = ttk.Checkbutton(
            self.output_check_label_frame,
            text="Save as .aud",
            variable=self.aud_check_var,
            command=self.monitor_all_checkbox_state
        )
        self.aud_check.pack(anchor="w", padx=10)

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

        self.btn_settings = ttk.Button(self.main_frame, text="Advanced Settings",
                                       command=self.advanced_settings_window.show_window)
        self.btn_settings.pack(fill="x", pady=5)

    def start_transcription(self):
        """Begin model loading (background) and start transcription flow.

        If no file is selected a warning is shown. Otherwise the run button
        is disabled and the model load is started in a daemon thread. The
        method then kicks off a polling loop (`monitor_load_thread`) which
        will continue once model loading completes.
        """
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
        """Poll the model loading thread until it finishes.

        This method schedules itself on the Tk event loop with `after(100)`
        while the loading thread is alive. When loading completes it updates
        the UI and triggers the transcription step.
        """
        if self.load_model_thread.is_alive():
            # Thread is still working, check again in 100ms
            self.root.after(100, self.monitor_load_thread)
        else:
            # Model is loaded! Now start the actual transcription
            self.btn_run.config(text="Transcribing...")
            self.run_actual_transcription()

    def run_actual_transcription(self):
        """Start the transcription task in a background thread.

        Builds the list of selected output formats from the checkbox variables
        and then starts a daemon thread which calls `transcribe_and_align` on
        the `whisper_x_ref`. When transcription finishes the UI is re-enabled
        and a completion message is shown.
        """
        output_formats = [fmt for fmt, var in [
            ("srt", self.srt_check_var), ("vtt", self.vtt_check_var),
            ("txt", self.txt_check_var), ("json", self.json_check_var),
            ("tsv", self.tsv_check_var), ("aud", self.aud_check_var)
        ] if var.get()]

        def trans_task():
            if self.auto_detect_option_var.get():
                print("Auto-detecting language...")
                self.whisper_x_ref.transcribe_and_align(
                    self.file_to_process,
                    language=None,  # Let whisperx auto-detect the language
                    diarize=self.diarize_var.get(),
                    output_formats=output_formats,
                    task=self.mode_var.get(),
                    temperature=configuration.temperature
                )
            else:
                print(f"Using selected language: {self.language_var.get()}")
                self.whisper_x_ref.transcribe_and_align(
                    self.file_to_process,
                    language=self.language_var.get(),
                    diarize=self.diarize_var.get(),
                    output_formats=output_formats,
                    task=self.mode_var.get(),
                    temperature=configuration.temperature
                )
            # Re-enable the UI on completion
            self.root.after(0, lambda: self.btn_run.config(state="normal", text="Start Processing"))
            self.root.after(0, lambda: messagebox.showinfo("Done", "Transcription Complete!"))

        self.whisper_thread = threading.Thread(target=trans_task, daemon=True)
        self.whisper_thread.start()

    def select_file(self):
        """Open a file dialog to choose an audio/video file to process.

        The selected path is stored in `self.file_to_process`. If the user
        cancels the dialog the value will be an empty string.
        """
        self.file_to_process = filedialog.askopenfilename(
            title="Select Audio/Video File",
            filetypes=[("Audio/Video Files", "*.mp4 *.mp3 *.wav *.m4a"), ("All Files", "*.*")]
        )

    def toggle_all_checkboxes(self):
        """Set or clear all individual format checkboxes.

        When the "Save in All Formats" checkbox is toggled this helper sets
        each individual output-format variable to the same boolean value.
        """
        if self.all_formats_var.get():
            for var in self.check_vars:
                var.set(True)
        else:
            for var in self.check_vars:
                var.set(False)

    def monitor_all_checkbox_state(self):
        """Keep the "Save in All Formats" checkbox state in sync.

        Called when any individual format checkbox changes; this updates the
        master `all_formats_var` so it reflects whether all formats are
        currently selected or not.
        """
        if all(var.get() for var in self.check_vars):
            self.all_formats_var.set(True)
        else:
            self.all_formats_var.set(False)

    def warn_no_alignment(self):
        if not configuration.suppress_no_align_warning:
            # user just checked the box
            # so don't show the warning
            # because alignment is now enabled
            if not self.alignment_var.get():
                messagebox.showwarning(
                    "Alignment Disabled",
                    "Warning. Phoneme alignment is currently disabled.\n"
                    "This means the output subtitles may drift from the audio.\n"
                    "If you want to enable alignment, please check the 'Enable Phoneme Alignment' box.\n"
                    "Note that enabling alignment may increase processing time and resource usage, especially on larger models or longer audio files.\n"
                    "Suppress this warning by changing self.suppress_no_align_warning to True in config.py\n"
                    "if you don't want to see it again."
                )

    def run(self):
        """Enter the Tk main event loop and handle KeyboardInterrupt.

        This wraps `mainloop()` in a try/except so a SIGINT (Ctrl+C) will
        gracefully stop and destroy the Tk root window instead of leaving the
        process in an inconsistent state.
        """
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
