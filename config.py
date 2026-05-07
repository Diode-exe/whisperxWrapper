"""Handles configuration settings for the WhisperXWrapper application, including model selection,
device settings, and supported languages. This class provides a centralized location for managing
these settings, making it easier to maintain and update the application as needed."""

class Config:
    """Configuration class for the WhisperXWrapper application. This class holds settings related to
    model selection, device configuration, and supported languages. It also includes a method for
    loading the Hugging Face token from a file."""
    def __init__(self):
        # default model name
        # can be changed in the GUI
        # or by setting the `model_name` attribute of the `WhisperXWrapper` instance
        self.model_name = "large-v3-turbo"
        self.models = [
            "tiny", "tiny.en",
            "base", "base.en",
            "small", "small.en",
            "medium", "medium.en",
            "large-v1", "large-v2", "large-v3",
            "large-v3-turbo" # The newest high-speed variant
        ]
        # inference platform
        # cannot be changed because you would need
        # to install the appropriate dependencies for each platform
        self.device = "cpu"
        # compute type for model inference
        # can be changed in the advanced settings window of the GUI
        self.compute_type = "float16"
        self.batch_size = 8
        # this isn't used in the code but is here for reference/documentation purposes
        self.supported_languages_shorthand = [
            "af", "am", "ar", "as", "az", "ba", "be", "bg", "bn", "bo",
            "br", "bs", "ca", "cs", "cy", "da", "de", "el", "en", "es",
            "et", "eu", "fa", "fi", "fo", "fr", "gl", "gu", "ha", "haw",
            "he", "hi", "hr", "hu", "hy", "id", "is", "it", "ja", "jw",
            "ka", "kk", "km", "kn", "ko", "la", "lb", "ln", "lo", "lt",
            "lv", "mg", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my",
            "ne", "nl", "nn", "no", "oc", "pa", "pl", "ps", "pt", "ro",
            "ru", "sa", "sd", "si", "sk", "sl", "sn", "so", "sq", "sr",
            "su", "sv", "sw", "ta", "te", "tg", "th", "tk", "tl", "tr",
            "tt", "uk", "ur", "uz", "vi", "yo", "zh"
        ]
        # This list is used to populate the dropdown menu in the GUI for language selection
        # these are sorted in alphabetical order by the shorthand language code
        # to ensure the longhand names are always in the same order
        self.supported_languages_longhand = [
            "Afrikaans", "Amharic", "Arabic",
            "Assamese", "Azerbaijani", "Bashkir",
            "Belarusian", "Bulgarian", "Bengali",
            "Tibetan", "Breton", "Bosnian",
            "Catalan", "Czech", "Welsh",
            "Danish", "German", "Greek",
            "English", "Spanish", "Estonian",
            "Basque", "Persian", "Finnish",
            "Faroese", "French", "Galician",
            "Gujarati", "Hausa", "Hawaiian",
            "Hebrew", "Hindi", "Croatian",
            "Hungarian", "Armenian", "Indonesian",
            "Icelandic", "Italian", "Japanese",
            "Javanese", "Georgian", "Kazakh",
            "Khmer", "Kannada", "Korean",
            "Latin", "Luxembourgish", "Lingala",
            "Lao", "Lithuanian", "Latvian",
            "Malagasy", "Maori", "Macedonian",
            "Malayalam", "Mongolian", "Marathi",
            "Malay", "Maltese", "Myanmar",
            "Nepali", "Dutch", "Nynorsk",
            "Norwegian", "Occitan", "Punjabi",
            "Polish", "Pashto", "Portuguese",
            "Romanian", "Russian", "Sanskrit",
            "Sindhi", "Sinhala", "Slovak",
            "Slovenian", "Shona", "Somali",
            "Albanian", "Serbian", "Sundanese",
            "Swedish", "Swahili", "Tamil",
            "Telugu", "Tajik", "Thai",
            "Turkmen", "Tagalog", "Turkish",
            "Tatar", "Ukrainian", "Urdu",
            "Uzbek", "Vietnamese", "Yoruba",
            "Chinese"
        ]

        self.long_to_short = {'Afrikaans': 'af', 'Amharic': 'am',
                              'Arabic': 'ar', 'Assamese': 'as',
                              'Azerbaijani': 'az', 'Bashkir': 'ba',
                              'Belarusian': 'be', 'Bulgarian': 'bg',
                              'Bengali': 'bn', 'Tibetan': 'bo',
                              'Breton': 'br', 'Bosnian': 'bs',
                              'Catalan': 'ca', 'Czech': 'cs',
                              'Welsh': 'cy', 'Danish': 'da',
                              'German': 'de', 'Greek': 'el',
                              'English': 'en', 'Spanish': 'es',
                              'Estonian': 'et', 'Basque': 'eu',
                              'Persian': 'fa', 'Finnish': 'fi',
                              'Faroese': 'fo', 'French': 'fr',
                              'Galician': 'gl', 'Gujarati': 'gu',
                              'Hausa': 'ha', 'Hawaiian': 'haw',
                              'Hebrew': 'he', 'Hindi': 'hi',
                              'Croatian': 'hr', 'Hungarian': 'hu',
                              'Armenian': 'hy', 'Indonesian': 'id',
                              'Icelandic': 'is', 'Italian': 'it',
                              'Japanese': 'ja', 'Javanese': 'jw',
                              'Georgian': 'ka', 'Kazakh': 'kk',
                              'Khmer': 'km', 'Kannada': 'kn',
                              'Korean': 'ko', 'Latin': 'la',
                              'Luxembourgish': 'lb', 'Lingala': 'ln',
                              'Lao': 'lo', 'Lithuanian': 'lt',
                              'Latvian': 'lv', 'Malagasy': 'mg',
                              'Maori': 'mi', 'Macedonian': 'mk',
                              'Malayalam': 'ml', 'Mongolian': 'mn',
                              'Marathi': 'mr', 'Malay': 'ms',
                              'Maltese': 'mt', 'Myanmar': 'my',
                              'Nepali': 'ne', 'Dutch': 'nl',
                              'Nynorsk': 'nn', 'Norwegian': 'no',
                              'Occitan': 'oc', 'Punjabi': 'pa',
                              'Polish': 'pl', 'Pashto': 'ps',
                              'Portuguese': 'pt', 'Romanian': 'ro',
                              'Russian': 'ru', 'Sanskrit': 'sa',
                              'Sindhi': 'sd', 'Sinhala': 'si',
                              'Slovak': 'sk', 'Slovenian': 'sl',
                              'Shona': 'sn', 'Somali': 'so',
                              'Albanian': 'sq', 'Serbian': 'sr',
                              'Sundanese': 'su', 'Swedish': 'sv',
                              'Swahili': 'sw', 'Tamil': 'ta',
                              'Telugu': 'te', 'Tajik': 'tg',
                              'Thai': 'th', 'Turkmen': 'tk',
                              'Tagalog': 'tl', 'Turkish': 'tr',
                              'Tatar': 'tt', 'Ukrainian': 'uk',
                              'Urdu': 'ur', 'Uzbek': 'uz',
                              'Vietnamese': 'vi', 'Yoruba': 'yo',
                              'Chinese': 'zh'}

    def load_hf_token(self):
        """Loads the Hugging Face token from a file."""
        try:
            with open("hf_token.txt", "r", encoding="utf-8") as f:
                token = f.read().strip()
                return token
        except FileNotFoundError:
            print("HF token file not found. "
                  "Please create a 'hf_token.txt' file with your Hugging Face token.")
            return None
