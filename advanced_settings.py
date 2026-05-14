import tkinter as tk
from tkinter import ttk, messagebox

class AdvancedSettingsWindow:
    def __init__(self, parent, configuration):
        self.parent = parent
        self.configuration = configuration
        self.window = None

        # Widgets
        self.batch_size_label = None
        self.batch_size_entry = None

        self.compute_type_label = None
        self.compute_type_combobox = None

        self.device_index_label = None
        self.device_index_entry = None

        self.temperature_label = None
        self.temperature_entry = None

        self.beam_size_label = None
        self.beam_size_entry = None

        self.enable_min_speaker_check = None
        self.enable_max_speaker_check = None

        self.min_speakers_label = None
        self.min_speakers_entry = None

        self.max_speakers_label = None
        self.max_speakers_entry = None

        self.apply_button = None

        # Tkinter variables (avoid None and allow .get()/.set())
        self.compute_type_var = tk.StringVar(value=getattr(self.configuration, 'compute_type', 'float32'))
        self.device_index_var = tk.StringVar(value=str(getattr(self.configuration, 'device_index', '')))
        self.enable_min_speaker_var = tk.BooleanVar(value=False)
        self.enable_max_speaker_var = tk.BooleanVar(value=False)
        self.min_speakers_var = tk.StringVar(value=str(getattr(self.configuration, 'min_speakers', 'None')))
        self.max_speakers_var = tk.StringVar(value=str(getattr(self.configuration, 'max_speakers', '10')))
        self.temperature_var = tk.StringVar(value=str(getattr(self.configuration, 'temperature', '0.0')))
        self.beam_size_var = tk.StringVar(value=str(getattr(self.configuration, 'beam_size', '1')))

    def show_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Advanced Settings")
        self.window.geometry("500x600")
        # Use a single grid-based content frame for predictable column alignment
        content = ttk.Frame(self.window, padding=10)
        content.grid(row=0, column=0, sticky="nsew")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Two logical columns (label/input) on left and right, so 4 grid columns total
        content.columnconfigure(1, weight=1)
        content.columnconfigure(3, weight=1)

        # Row 0: Batch Size (left) | Compute Type (right)
        self.batch_size_label = ttk.Label(content, text="Batch Size:")
        self.batch_size_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.batch_size_entry = ttk.Entry(content, width=6)
        self.batch_size_entry.insert(0, str(self.configuration.batch_size))
        self.batch_size_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.compute_type_label = ttk.Label(content, text="Compute Type:")
        self.compute_type_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.compute_type_combobox = ttk.Combobox(content,
                              values=["int8", "float16", "float32"],
                              textvariable=self.compute_type_var,
                              state="readonly",
                              width=17)
        self.compute_type_combobox.set(self.configuration.compute_type)
        self.compute_type_combobox.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        # Row 1: Device Index (left) | Temperature (right)
        self.device_index_label = ttk.Label(content, text="Device Index (for GPU):")
        self.device_index_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.device_index_entry = ttk.Entry(content, textvariable=self.device_index_var)
        self.device_index_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.temperature_label = ttk.Label(content, text="Temperature:")
        self.temperature_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.temperature_entry = ttk.Entry(content, textvariable=self.temperature_var, width=8)
        self.temperature_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        # Row 2: Beam size (left)
        self.beam_size_label = ttk.Label(content, text="Beam Size:")
        self.beam_size_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.beam_size_entry = ttk.Entry(content, textvariable=self.beam_size_var, width=6)
        self.beam_size_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Row 3: Minimum speakers
        self.enable_min_speaker_check = ttk.Checkbutton(content,
                text="Enable Minimum Speakers",
                variable=self.enable_min_speaker_var,
                command=self.toggle_min_speakers)
        self.enable_min_speaker_check.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.min_speakers_label = ttk.Label(content, text="Minimum Speakers (for diarization):")
        self.min_speakers_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.min_speakers_entry = ttk.Entry(content, textvariable=self.min_speakers_var)
        self.min_speakers_entry.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.min_speakers_entry.config(state="disabled")

        # Row 4: Maximum speakers
        self.enable_max_speaker_check = ttk.Checkbutton(content,
                text="Enable Maximum Speakers",
                variable=self.enable_max_speaker_var,
                command=self.toggle_max_speakers)
        self.enable_max_speaker_check.grid(row=7, column=0, sticky="w", padx=5, pady=5)

        self.max_speakers_label = ttk.Label(content, text="Maximum Speakers (for diarization):")
        self.max_speakers_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.max_speakers_entry = ttk.Entry(content, textvariable=self.max_speakers_var)
        self.max_speakers_entry.grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.max_speakers_entry.config(state="disabled")

        # Row 5: Apply button centered
        self.apply_button = ttk.Button(content, text="Apply", command=self.apply_settings)
        self.apply_button.grid(row=10, column=0, columnspan=4, pady=15)

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
            self.configuration.temperature = float(self.temperature_var.get())
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
