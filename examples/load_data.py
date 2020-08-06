from mao.cedict import load_cedict
from mao.dedict import load_dedict
from mao.kangxi import load_kangxi_radicals_table
from mao.unihan import load_unihan

unihan_df = load_unihan()
cedict_df = load_cedict()
dedict_df = load_dedict()
kangxi_df = load_kangxi_radicals_table()
