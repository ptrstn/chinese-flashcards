from mao.data.kangxi import load_kangxi_radicals_table
from mao.data.strokes import download_glyph_strokes_to_disk

kangxi_table = load_kangxi_radicals_table()
glyphs = list(kangxi_table.unified_glyph)
download_glyph_strokes_to_disk(glyphs, "data/strokes")
