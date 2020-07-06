from mao.unicode import (
    get_unicode_name,
    encode_unicode_character,
    encode_unicode_characters,
)


def test_get_unicode_name():
    assert get_unicode_name("⼀") == "KANGXI RADICAL ONE"
    assert get_unicode_name("一") == "CJK UNIFIED IDEOGRAPH-4E00"
    assert get_unicode_name("鼖") == "CJK COMPATIBILITY IDEOGRAPH-2FA1B"
    assert get_unicode_name("水") == "CJK UNIFIED IDEOGRAPH-6C34"


def test_hex_code_to_unicode_character():
    assert encode_unicode_character("U+4EBA") == "人"
    assert encode_unicode_character("0x2f2a") == "⼪"
    assert encode_unicode_character("2fa1c") == "鼻"
    assert encode_unicode_character("00028D71") == "𨵱"
    assert encode_unicode_character("6C34") == "水"


def test_hex_codes_to_unicode_character():
    text = "U+4EBA 0x2f2a bamboocha 00028D71 U+6C34"
    expected_text = "人 ⼪ bamboocha 00028D71 水"
    assert encode_unicode_characters(text) == expected_text
