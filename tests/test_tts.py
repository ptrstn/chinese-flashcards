import collections

from google.api_core.exceptions import ServiceUnavailable
from google.auth.exceptions import DefaultCredentialsError, RefreshError

from han.tts import ChineseTTSClient, save_speech_response


def test_tts():
    try:
        client = ChineseTTSClient()
        response = client.speak_chinese("女")
        assert response
    except (DefaultCredentialsError, RefreshError, ServiceUnavailable):
        pass


def test_save_speech_response():
    response = collections.namedtuple("Response", "audio_content")
    response.audio_content = b"abc"
    save_speech_response(response, "test_data/voices/test.mp3")
