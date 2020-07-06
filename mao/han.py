from pypinyin import pinyin


class HanCharacter:
    def __init__(self, character: str) -> None:
        super().__init__()
        self.glyph = character
        self.unicode = f"{ord(character):x}".upper()
        self.pinyin = pinyin(character)[0][0]


def analyse_chinese_character(character: str) -> dict:
    chinese_character = HanCharacter(character)

    return {
        "Character": chinese_character.glyph,
        "Unicode": chinese_character.unicode,
        "Pinyin": chinese_character.pinyin,
    }


def print_chinese_character_range(first_character: str, last_character: str) -> None:
    print(f"{'No.':3} {'Unicode':7} {'Hanzi':6} {'Pinyin':10}")

    for idx, unicode_value in enumerate(
        range(ord(first_character), ord(last_character) + 1)
    ):
        character = HanCharacter(chr(unicode_value))
        print(
            f"{idx + 1:3} {character.unicode:7x} {character.glyph:6} {character.pinyin:10}"
        )


def print_chinese_character_analysis(character: str) -> None:
    for key, value in analyse_chinese_character(character).items():
        print(f"{key:>10} {value}")
