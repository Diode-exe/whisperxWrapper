## WhisperX GUI Wrapper

A lightweight Tkinter desktop wrapper around [WhisperX](https://github.com/m-bain/whisperX) for transcription, translation, alignment, and optional speaker diarization.

This project is intended for users who prefer a simple GUI over command-line flags.

## Features

- GUI-based audio/video file selection
- Transcription mode selection:
	- `transcribe` (same-language transcription)
	- `translate` (translate speech to English)
- Optional speaker diarization (requires Hugging Face token)
- Optional language auto-detection or manual language selection
- Model selection from common Whisper model variants
- Multiple output formats from the GUI (`srt`, `vtt`, `txt`, `json`, `tsv`, `aud`)
- Advanced settings window for compute options

## Project Layout

- `main.py`: Tkinter GUI application entry point
- `transcribe.py`: WhisperX wrapper class (model load, transcribe, align, diarize, output writing)
- `config.py`: App defaults and language mappings
- `advanced_settings.py`: Advanced settings popup window
- `hf_token.txt`: Place your Hugging Face token here for diarization
- `pyproject.toml`: Project metadata and Python dependency declaration

## Requirements

- Python `3.11.9` (exact match as declared in `pyproject.toml`)
- `whisperx>=3.8.5`
- System dependencies required by WhisperX (for many environments this includes FFmpeg and PyTorch-compatible runtime)

## Quick Start (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

2. Install project dependencies:

```powershell
python -m pip install --upgrade pip
pip install .
```

3. (Optional, only for diarization) add your Hugging Face token to `hf_token.txt`:

```text
hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. Launch the GUI:

```powershell
python main.py
```

## How To Use

1. Click **Select Audio/Video File** and choose an input file.
2. Pick mode:
	 - **Transcribe (Same Language)**
	 - **Translate (To English)**
3. Toggle **Auto-Detect Language** or select a language manually.
4. Choose a model.
5. Choose output formats (or keep **Save in All Formats** enabled).
6. Optionally enable **Speaker Diarization**.
7. Click **Start Processing**.

Output files are written next to the input media file.

## Configuration Notes

Defaults live in `config.py`:

- `model_name`: default model (`large-v3-turbo`)
- `device`: default inference device (`cpu`)
- `compute_type`: default compute type (`float16`)
- `batch_size`, `temperature`, and language mapping tables
- `suppress_no_align_warning`: warning preference for disabled alignment in GUI

Advanced settings can be changed in the **Advanced Settings** window at runtime.

## Diarization Setup

If diarization is enabled:

- A valid token must be available in `hf_token.txt`
- Your token may need access to required Hugging Face diarization models
- If access is missing, transcription still completes and diarization is skipped/fails gracefully

## Troubleshooting

- `HF token file not found`: create `hf_token.txt` in the project root and paste your token.
- Import/setup errors for WhisperX: verify your Python version and that `pip install .` completed successfully.
- FFmpeg-related errors: install FFmpeg and ensure it is available on your system PATH.
- Diarization warnings about short segments: non-fatal warnings may appear for edge-case clips.

## Current Known Issues

- The GUI alignment checkbox currently does not change backend behavior because alignment is always executed in `transcribe.py`.

If you want, I can also patch these issues so the GUI controls map cleanly to backend behavior.

## License

No license file is currently included in this repository. Add one (for example, MIT) if you plan to distribute the project.
