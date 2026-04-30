import os
import json
from config import Config

# Tell PyTorch that OmegaConf objects are safe to unpickle
# this is safe because we control the code and data,
# but be cautious if loading from untrusted sources
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

configuration = Config()

class WhisperXWrapper:
    def __init__(self):
        self.model = None

    def load_model(self, model_name: str=None):
        if model_name is not None:
            self.model_name = model_name
        print(f"Loading Transcription model on {configuration.device}...")
        try:
            import whisperx
        except Exception as e:
            raise ImportError(
                "Failed to import whisperx. Ensure whisperx and its dependencies are installed: "
                f"{e}"
            )

        self.model = whisperx.load_model(
            self.model_name,
            device=configuration.device,
            compute_type=configuration.compute_type
        )

    def transcribe_and_align(self, audio_path, language="English", diarize=False):
        try:
            import whisperx
        except Exception as e:
            raise ImportError(
                "Failed to import whisperx for transcription. Ensure whisperx is installed: "
                f"{e}"
            )

        audio = whisperx.load_audio(audio_path)
        print("Loaded audio, starting transcription...")
        result = self.model.transcribe(audio, batch_size=16, language=language)
        print("Transcription complete, starting alignment...")

        print(f"Aligning on {configuration.device}...")
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=configuration.device
        )

        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            configuration.device,
            return_char_alignments=False
        )
        print("Alignment complete.")
        if diarize:
            hf_token = configuration.load_HF_token()
            if not hf_token:
                print("Cannot perform diarization without Hugging Face token. "
                      "Please provide a valid token in 'hf_token.txt'. Skipping diarization.")
                return result
            diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token,
                                                         device=configuration.device)
            diarize_segments = diarize_model(audio)
            result = whisperx.assign_word_speakers(diarize_segments, result)

        with open("transcription_output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result
