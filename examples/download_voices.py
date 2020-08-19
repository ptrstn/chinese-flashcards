from han.data.kangxi import load_kangxi_radicals_table
from han.tts import ChineseTTSClient, save_speech_response, CHINESE_VOICE_NAMES

tts_client = ChineseTTSClient()
kangxi_table = load_kangxi_radicals_table()
glyphs = list(kangxi_table.unified_glyph)


for glyph in glyphs:
    voice_index = 3
    voice = tts_client.speak_chinese(text=glyph, voice_index=voice_index)
    voice_name = CHINESE_VOICE_NAMES[voice_index]
    save_speech_response(voice, f"data/voices/{voice_name}/{glyph}.mp3")
    save_speech_response(voice, f"data/voices/{glyph}.mp3")
