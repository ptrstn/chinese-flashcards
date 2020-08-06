import collections

from mao.tts import ChineseTTSClient, save_speech_response


def test_tts():
    client = ChineseTTSClient()
    response = client.speak_chinese("女")
    assert response


def test_save_speech_response():
    response = collections.namedtuple("Response", "audio_content")
    response.audio_content = b"abc"
    save_speech_response(response, "test_data/voices/test.mp3")
