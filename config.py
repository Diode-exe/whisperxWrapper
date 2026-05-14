"""Runtime configuration for WhisperX wrapper.

Imports static constants (models, languages) from constants.py and manages
runtime-tunable settings with JSON persistence.
"""

import json
import os
from constants import MODELS, SUPPORTED_LANGUAGES_LONGHAND, SUPPORTED_LANGUAGES_SHORTHAND, LONG_TO_SHORT


class Config:
    """Manages runtime-tunable settings with JSON persistence."""

    SETTINGS_FILE = "settings.json"

    def __init__(self):
        # Import static data from constants (never changes)
        self.models = MODELS
        self.supported_languages_longhand = SUPPORTED_LANGUAGES_LONGHAND
        self.supported_languages_shorthand = SUPPORTED_LANGUAGES_SHORTHAND
        self.long_to_short = LONG_TO_SHORT

        # Runtime-tunable defaults (can be overridden by settings.json)
        self.model_name = "large-v3-turbo"
        self.device = "cpu"
        self.compute_type = "float16"
        self.batch_size = 8
        self.device_index = "0"
        self.suppress_no_align_warning = False
        self.temperature = 0.0
        self.min_speakers = "None"
        self.max_speakers = "10"
        self.beam_size = 1

        # Load persisted settings if present
        self.load_settings()

    def load_settings(self, path: str = None):
        """Load runtime-tunable settings from JSON file."""
        path = path or self.SETTINGS_FILE
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return

        if not isinstance(data, dict):
            return

        # Apply only known runtime-tunable keys
        for key in ["model_name", "device", "compute_type", "batch_size", 
                    "device_index", "temperature", "suppress_no_align_warning",
                    "min_speakers", "max_speakers", "beam_size"]:
            if key in data:
                value = data[key]
                # Type coercion for known fields
                if key == "batch_size" or key == "beam_size":
                    value = int(value)
                elif key == "temperature":
                    value = float(value)
                elif key == "suppress_no_align_warning":
                    value = bool(value)
                setattr(self, key, value)

    def save_settings(self, path: str = None):
        """Save runtime-tunable settings to JSON file."""
        path = path or self.SETTINGS_FILE
        data = {
            "model_name": self.model_name,
            "device": self.device,
            "compute_type": self.compute_type,
            "batch_size": self.batch_size,
            "device_index": self.device_index,
            "temperature": self.temperature,
            "suppress_no_align_warning": self.suppress_no_align_warning,
            "min_speakers": self.min_speakers,
            "max_speakers": self.max_speakers,
            "beam_size": self.beam_size,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_hf_token(self):
        """Load Hugging Face token from project root hf_token.txt file."""
        try:
            with open("hf_token.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            print("HF token file not found. Please create 'hf_token.txt' with your Hugging Face token.")
            return None
