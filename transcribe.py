import os
import whisperx

# Tell PyTorch that OmegaConf objects are safe to unpickle
# this is safe because we control the code and data,
# but be cautious if loading from untrusted sources
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

class WhisperXWrapper:
    def __init__(self, model_name: str = "base"):
        self.device = "cpu"       # Transcription engine (CTranslate2)
        self.compute_type = "int8"
        self.model_name = model_name
        self.model = None

    def load_model(self, model_name: str=None):
        if model_name is not None:
            self.model_name = model_name
        print(f"Loading Transcription model on {self.device}...")
        self.model = whisperx.load_model(
            model_name,
            device=self.device,
            compute_type=self.compute_type
        )

    def transcribe_and_align(self, audio_path):
        audio = whisperx.load_audio(audio_path)
        result = self.model.transcribe(audio, batch_size=16)

        print(f"Aligning on {self.device}...")
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=self.device
        )

        result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            self.device,
            return_char_alignments=False
        )
        return result
