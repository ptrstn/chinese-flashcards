from mao.strokes import download_glyph_strokes_to_disk


def test_download_glyph_strokes_to_disk():
    glyphs = ["一", "龜"]
    path = "test_data/strokes"
    download_glyph_strokes_to_disk(glyphs, path)