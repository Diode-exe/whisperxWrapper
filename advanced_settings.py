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

        self.apply_button = None

    def show_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Advanced Settings")
        self.window.geometry("400x300")

        self.batch_size_label = ttk.Label(self.window, text="Batch Size:")
        self.batch_size_label.pack(pady=5)
        self.batch_size_entry = ttk.Entry(self.window)
        self.batch_size_entry.insert(0, str(self.configuration.batch_size))
        self.batch_size_entry.pack(pady=5)

        self.compute_type_var = tk.StringVar(value=self.configuration.compute_type)
        self.compute_type_label = ttk.Label(self.window, text="Compute Type:")
        self.compute_type_label.pack(pady=5)
        self.compute_type_combobox = ttk.Combobox(self.window,
                                                  values=["int8", "float16", "float32"],
                                                  textvariable=self.compute_type_var,
                                                  state="readonly")
        self.compute_type_combobox.set(self.configuration.compute_type)
        self.compute_type_combobox.pack(pady=5)

        self.device_index_label = ttk.Label(self.window, text="Device Index (for GPU):")
        self.device_index_label.pack(pady=5)
        self.device_index_var = tk.StringVar(value="0")
        self.device_index_entry = ttk.Entry(self.window, textvariable=self.device_index_var)
        self.device_index_entry.pack(pady=5)

        self.apply_button = ttk.Button(self.window, text="Apply", command=self.apply_settings)
        self.apply_button.pack(pady=20)

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
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
