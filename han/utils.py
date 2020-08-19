import re

import numpy

from han.decorators import non_null_call


def extract_unicode_notations(text, join_on=" "):
    return join_on.join(re.findall(r"U\+[0-9A-F]+", text))


def _match_encode_unicode_notation(match):
    return encode_unicode_notation(match.group())


def encode_unicode_notations_in_text(text):
    return re.sub(r"U\+[0-9a-fA-F]+", _match_encode_unicode_notation, text)


def encode_unicode_notation(unicode_notation):
    """
    Encodes a ASCII-fied unicode notation ("U+" convention)

    :param unicode_notation: string like "U+2F08"
    :return: encoded unicode character like "人"
    """
    return chr(int(unicode_notation.replace("U+", ""), 16))


@non_null_call
def extract_encode_glyphs(value):
    glyphs = encode_unicode_notations_in_text(extract_unicode_notations(value))
    return glyphs if glyphs else numpy.nan
