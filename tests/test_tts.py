import collections

import pytest
from google.auth.exceptions import DefaultCredentialsError

from mao.tts import ChineseTTSClient, save_speech_response


def test_tts():
    with pytest.raises(DefaultCredentialsError):
        ChineseTTSClient()


def test_save_speech_response():
    response = collections.namedtuple("Response", "audio_content")
    response.audio_content = b"abc"
    save_speech_response(response, "test_data/voices/test.mp3")
