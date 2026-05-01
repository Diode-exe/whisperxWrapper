import os
import warnings
from config import Config

# Tell PyTorch that OmegaConf objects are safe to unpickle
# this is safe because we control the code and data,
# but be cautious if loading from untrusted sources
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"


class WhisperXWrapper:
    def __init__(self):
        self.model = None
        self.model_name = None
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
            print("Failed to import whisperx. Ensure whisperx and its dependencies are installed: "
                f"{e}")

        self.model = whisperx.load_model(
            self.model_name,
            device=self.configuration.device,
            compute_type=self.configuration.compute_type
        )

    def transcribe_and_align(self, audio_path, language="English", diarize=False, output_formats=None):
        if output_formats is None:
            output_formats = []
        try:
            import whisperx
        except Exception as e:
            print("Failed to import whisperx for transcription. Ensure whisperx is installed: "
                f"{e}")

        audio = whisperx.load_audio(audio_path)
        print("Loaded audio, starting transcription...")
        language_short = self.configuration.long_to_short.get(language, "en")
        print(f"Transcription language code: {language_short}")
        try:
            result = self.model.transcribe(
                audio,
                batch_size=16,
                language=language_short,
                language_code=language_short,
            )
        except TypeError:
            # Older/newer whisperx versions may not accept `language_code` kwarg.
            result = self.model.transcribe(
                audio,
                batch_size=16,
                language=language_short,
            )
        # keep original transcription result (contains language metadata)
        trans_result = result
        print("Transcription complete, starting alignment...")

        print(f"Aligning on {self.configuration.device}...")
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=self.configuration.device
        )

        result = whisperx.align(
            trans_result["segments"],
            model_a,
            metadata,
            audio,
            self.configuration.device,
            return_char_alignments=False
        )
        # ensure language metadata is present for writers
        try:
            result["language"] = trans_result.get("language", language_short)
        except Exception:
            result = {**(result or {}), "language": trans_result.get("language", language_short)}
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
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore",
                        message=r"std\(\): degrees of freedom is <= 0.*",
                        category=UserWarning,
                    )
                    diarize_segments = diarize_model(audio)
                result = whisperx.assign_word_speakers(diarize_segments, result)
            except KeyboardInterrupt:
                print("Diarization interrupted by user.")
                return result
            except Exception as e:
                print(f"Failed to perform diarization: {e}")
                print("You may need to accept the terms of the diarization model on Hugging Face "
                      "and ensure your token has access.")
        print("Diarization complete.")
        # Normalize output_formats to a list of format strings
        options = {"max_line_width": 80, "max_line_count": None, "highlight_words": False}
        for fmt in output_formats:
            print(f"Writing output in {fmt} format...")
            writer = whisperx.utils.get_writer(fmt, output_dir=os.path.dirname(audio_path))
            writer(result, audio_path, options)
        return result
