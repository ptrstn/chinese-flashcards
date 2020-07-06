from mao.han import HanCharacter


def test_analyse_chinese_character():
    character = "一"
    expected_unicode = "4E00"
    expected_pinyin = "yī"

    han_character = HanCharacter(character)
    assert han_character.glyph == character
    assert han_character.unicode == expected_unicode
    assert han_character.pinyin == expected_pinyin

    character = "⼀"
    expected_unicode = "2F00"
    expected_pinyin = "⼀"

    han_character = HanCharacter(character)
    assert han_character.glyph == character
    assert han_character.unicode == expected_unicode
    assert han_character.pinyin == expected_pinyin
