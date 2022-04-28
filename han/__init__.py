__version__ = "0.0.1"

from .data.cedict import load_cedict  # noqa: F401
from .data.dedict import load_dedict  # noqa: F401
from .data.hsk import load_hsk  # noqa: F401
from .data.kangxi import load_kangxi_radicals  # noqa: F401
from .data.unihan import load_unihan  # noqa: F401
