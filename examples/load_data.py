from han.data.cedict import load_cedict
from han.data.dedict import load_dedict
from han.data.kangxi import load_kangxi_radicals_table
from han.data.unihan import load_unihan

unihan_df = load_unihan()
cedict_df = load_cedict()
dedict_df = load_dedict()
kangxi_df = load_kangxi_radicals_table()
