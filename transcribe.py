import os
import json
from config import Config

# Tell PyTorch that OmegaConf objects are safe to unpickle
# this is safe because we control the code and data,
# but be cautious if loading from untrusted sources
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"


class WhisperXWrapper:
    def __init__(self):
        self.model = None
        self.configuration = Config()

    def load_model(self, model_name: str=None):
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = self.configuration.model_name
        print(f"Loading Transcription model on {self.configuration.device}...")
        try:
            import whisperx
        except Exception as e:
            raise ImportError(
                "Failed to import whisperx. Ensure whisperx and its dependencies are installed: "
                f"{e}"
            )

        self.model = whisperx.load_model(
            self.model_name,
            device=self.configuration.device,
            compute_type=self.configuration.compute_type
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
        result = self.model.transcribe(audio, batch_size=16,
                                       language=self.configuration.long_to_short.get(language, "en"))
        print("Transcription complete, starting alignment...")

        print(f"Aligning on {self.configuration.device}...")
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=self.configuration.device
        )

        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            self.configuration.device,
            return_char_alignments=False
        )
        print("Alignment complete.")
        if diarize:
            hf_token = self.configuration.load_HF_token()
            if not hf_token:
                print("Cannot perform diarization without Hugging Face token. "
                      "Please provide a valid token in 'hf_token.txt'. Skipping diarization.")
                return result
            try:
                diarize_model = whisperx.diarize.DiarizationPipeline(token=hf_token,
                                                            device=self.configuration.device)
                diarize_segments = diarize_model(audio)
                result = whisperx.assign_word_speakers(diarize_segments, result)
            except Exception as e:
                print(f"Failed to perform diarization: {e}")
                print("You may need to accept the terms of the diarization model on Hugging Face "
                      "and ensure your token has access.")

        with open("transcription_output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result
