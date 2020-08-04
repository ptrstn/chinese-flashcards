def validate_png_file_signature(byte_content):
    """
    Checks if the PNG file signature is valid.

    The first eight bytes of a PNG file always contain the following values:

    (decimal)              137  80  78  71  13  10  26  10
    (hexadecimal)           89  50  4e  47  0d  0a  1a  0a
    (ASCII C notation)    \211   P   N   G  \r  \n \032 \n

    see: http://www.libpng.org/pub/png/spec/1.2/PNG-Rationale.html#R.PNG-file-signature

    :param byte_content:
    :return:
    """
    return byte_content[:7] == b"\x89PNG\r\n\x1a"


def validate_gif_file_signature(byte_content):
    return byte_content[:6] == b"GIF89a"
