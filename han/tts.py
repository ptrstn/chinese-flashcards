import pathlib

from google.cloud import texttospeech

CHINESE_VOICE_NAMES = [
    "cmn-CN-Wavenet-A",
    "cmn-CN-Wavenet-B",
    "cmn-CN-Wavenet-C",
    "cmn-CN-Wavenet-D",
]

CHINESE_LANGUAGE_CODE = "cmn-CN"


class GoogleTTSClient:
    def __init__(self) -> None:
        super().__init__()
        self.client = texttospeech.TextToSpeechClient()
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def speak(self, text, language_code, voice_name):
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
        )

        synthesis_input = texttospeech.SynthesisInput(text=text)

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=self.audio_config
        )

        return response


class ChineseTTSClient(GoogleTTSClient):
    def speak_chinese(self, text, voice_index=2):
        voice_name = CHINESE_VOICE_NAMES[voice_index]
        return super().speak(text, CHINESE_LANGUAGE_CODE, voice_name)


def save_speech_response(response, filename):
    filepath = pathlib.Path(filename)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, "wb") as file:
        file.write(response.audio_content)
        print(f'Audio content written to file "{filename}"')
