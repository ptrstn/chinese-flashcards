from mao.utils import validate_png_file_signature, validate_gif_file_signature


def test_validate_png_file_signature():
    assert not validate_png_file_signature("string")
    assert not validate_png_file_signature(b'GIF89a,\x01,\x01')
    assert validate_png_file_signature(b'\x89PNG\r\n\x1a\n\x00\x00')
    assert not validate_png_file_signature("b'<!DOCTYPE '")


def test_validate_gif_file_signature():
    assert not validate_gif_file_signature("string")
    assert validate_gif_file_signature(b'GIF89a,\x01,\x01')
    assert not validate_gif_file_signature(b'\x89PNG\r\n\x1a\n\x00\x00')
    assert not validate_gif_file_signature("b'<!DOCTYPE '")
