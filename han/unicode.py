import unicodedata


def get_unicode_name(character):
    return unicodedata.name(character)


def encode_unicode_character(hex_code):
    return chr(int(hex_code.replace("U+", ""), 16))


def encode_unicode_characters(text):
    words = text.split()
    return " ".join(
        [
            encode_unicode_character(word)
            if word.startswith("U+") or word.startswith("0x")
            else word
            for word in words
        ]
    )
