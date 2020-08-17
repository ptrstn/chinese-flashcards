import numpy
import pandas

from mao.utils import (
    validate_png_file_signature,
    validate_gif_file_signature,
    extract_unicode_notations,
    encode_unicode_notations_in_text,
    extract_encode_glyphs,
)


def test_validate_png_file_signature():
    assert not validate_png_file_signature("string")
    assert not validate_png_file_signature(b"GIF89a,\x01,\x01")
    assert validate_png_file_signature(b"\x89PNG\r\n\x1a\n\x00\x00")
    assert not validate_png_file_signature("b'<!DOCTYPE '")


def test_validate_gif_file_signature():
    assert not validate_gif_file_signature("string")
    assert validate_gif_file_signature(b"GIF89a,\x01,\x01")
    assert not validate_gif_file_signature(b"\x89PNG\r\n\x1a\n\x00\x00")
    assert not validate_gif_file_signature("b'<!DOCTYPE '")


def test_extract_unicode_notations():
    assert extract_unicode_notations("U+91D2<kMatthews") == "U+91D2"
    text = (
        "U+9B2D<kLau,kMatthews,kMeyerWempe "
        "U+9B2C<kMatthews "
        "U+9B26<kLau,kMeyerWempe "
        "U+9B2A<kLau,kMatthews"
    )
    assert extract_unicode_notations(text) == "U+9B2D U+9B2C U+9B26 U+9B2A"
    assert extract_unicode_notations("Some random text") == ""
    assert extract_unicode_notations("") == ""
    text = "U+8349<kMatthews U+8279<kMatthews"
    assert extract_unicode_notations(text, join_on=", ") == "U+8349, U+8279"


def test_encode_unicode_notations_in_text():
    text = "U+8349<kMatthews U+8279<kMatthews"
    assert encode_unicode_notations_in_text(text) == "草<kMatthews 艹<kMatthews"


def test_extract_encode_glyphs():
    text = (
        "U+9B2D<kLau,kMatthews,kMeyerWempe "
        "U+9B2C<kMatthews "
        "U+9B26<kLau,kMeyerWempe "
        "U+9B2A<kLau,kMatthews"
    )
    assert extract_encode_glyphs(text) == "鬭 鬬 鬦 鬪"
    assert pandas.isnull(extract_encode_glyphs("random text"))
    assert pandas.isnull(extract_encode_glyphs(numpy.nan))
