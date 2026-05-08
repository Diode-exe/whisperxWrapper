import tkinter as tk
from tkinter import ttk, messagebox

class AdvancedSettingsWindow:
    def __init__(self, parent, configuration):
        self.parent = parent
        self.configuration = configuration
        self.window = None

        self.batch_size_label = None
        self.batch_size_entry = None

        self.compute_type_var = None
        self.compute_type_label = None
        self.compute_type_combobox = None

        self.device_index_var = None
        self.device_index_label = None
        self.device_index_entry = None

        self.speakers_options_frame = None

        self.min_frame = None

        self.enable_min_speaker_var = None
        self.enable_min_speaker_check = None
        self.enable_max_speaker_var = None
        self.enable_max_speaker_check = None

        self.min_speakers_var = None
        self.min_speakers_label = None
        self.min_speakers_entry = None

        self.max_frame = None

        self.max_speakers_var = None
        self.max_speakers_label = None
        self.max_speakers_entry = None

        self.apply_button = None

    def show_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Advanced Settings")
        self.window.geometry("500x400")

        self.batch_size_label = ttk.Label(self.window, text="Batch Size:", anchor="w")
        self.batch_size_label.pack(pady=(0, 5), anchor="w", padx=10)
        self.batch_size_entry = ttk.Entry(self.window)
        self.batch_size_entry.insert(0, str(self.configuration.batch_size))
        self.batch_size_entry.pack(pady=(0, 5), anchor="w", padx=10)

        self.compute_type_var = tk.StringVar(value=self.configuration.compute_type)
        self.compute_type_label = ttk.Label(self.window, text="Compute Type:")
        self.compute_type_label.pack(pady=(0, 5), anchor="w", padx=10)
        self.compute_type_combobox = ttk.Combobox(self.window,
                                                  values=["int8", "float16", "float32"],
                                                  textvariable=self.compute_type_var,
                                                  state="readonly")
        self.compute_type_combobox.set(self.configuration.compute_type)
        self.compute_type_combobox.pack(pady=(0, 5), anchor="w", padx=10)

        self.device_index_label = ttk.Label(self.window, text="Device Index (for GPU):")
        self.device_index_label.pack(pady=(0, 5), anchor="w", padx=10)
        self.device_index_var = tk.StringVar(value="0")
        self.device_index_entry = ttk.Entry(self.window, textvariable=self.device_index_var)
        self.device_index_entry.pack(pady=(0, 5), anchor="w", padx=10)

        self.speakers_options_frame = ttk.LabelFrame(self.window, text="Speaker Diarization Options")
        self.speakers_options_frame.pack(pady=10, fill="x", expand=False, anchor="w", padx=10)

        # Create vertical sub-frames so each checkbox appears above its entry
        self.min_frame = ttk.Frame(self.speakers_options_frame)
        self.min_frame.pack(side="left", padx=10, pady=5, fill="y", expand=True)

        self.enable_min_speaker_var = tk.BooleanVar(value=False)
        self.enable_min_speaker_check = ttk.Checkbutton(self.min_frame,
                                text="Enable Minimum Speakers",
                                variable=self.enable_min_speaker_var,
                                command=self.toggle_min_speakers)
        self.enable_min_speaker_check.pack(anchor="n")

        self.min_speakers_label = ttk.Label(self.min_frame, text="Minimum Speakers (for diarization):")
        self.min_speakers_label.pack(anchor="n", pady=(6, 0))
        self.min_speakers_var = tk.StringVar(value="")
        self.min_speakers_entry = ttk.Entry(self.min_frame, textvariable=self.min_speakers_var)
        self.min_speakers_entry.pack(anchor="n", pady=(0, 6))
        # start disabled until enabled by the checkbox
        self.min_speakers_entry.config(state="disabled")

        self.max_frame = ttk.Frame(self.speakers_options_frame)
        self.max_frame.pack(side="right", padx=10, pady=5, fill="y", expand=True)

        self.enable_max_speaker_var = tk.BooleanVar(value=False)
        self.enable_max_speaker_check = ttk.Checkbutton(self.max_frame,
                                text="Enable Maximum Speakers",
                                variable=self.enable_max_speaker_var,
                                command=self.toggle_max_speakers)
        self.enable_max_speaker_check.pack(anchor="n")

        self.max_speakers_label = ttk.Label(self.max_frame, text="Maximum Speakers (for diarization):")
        self.max_speakers_label.pack(anchor="n", pady=(6, 0))
        self.max_speakers_var = tk.StringVar(value="10")
        self.max_speakers_entry = ttk.Entry(self.max_frame, textvariable=self.max_speakers_var)
        self.max_speakers_entry.pack(anchor="n", pady=(0, 6))
        # start disabled until enabled by the checkbox
        self.max_speakers_entry.config(state="disabled")

        self.apply_button = ttk.Button(self.window, text="Apply", command=self.apply_settings)
        self.apply_button.pack(pady=20)

    def toggle_min_speakers(self):
        if self.enable_min_speaker_var.get():
            self.min_speakers_entry.config(state="normal")
        else:
            self.min_speakers_entry.config(state="disabled")
            self.min_speakers_var.set("None")

    def toggle_max_speakers(self):
        if self.enable_max_speaker_var.get():
            self.max_speakers_entry.config(state="normal")
        else:
            self.max_speakers_entry.config(state="disabled")
            self.max_speakers_var.set("10")

    def apply_settings(self):
        """Apply the advanced settings entered by the user."""
        try:
            batch_size = int(self.batch_size_entry.get())
            if batch_size <= 1:
                messagebox.showerror("Invalid Input", "Batch size must be greater than 1.")
                self.window.focus()
                return
            self.configuration.batch_size = batch_size
            self.configuration.compute_type = self.compute_type_var.get()
            self.configuration.device_index = self.device_index_var.get()
            self.configuration.min_speakers = self.min_speakers_var.get()
            self.configuration.max_speakers = self.max_speakers_var.get()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
