import pytest

from mao.constants import NUMBER_OF_KANGXI_RADICALS
from mao.data import get_kangxi_radicals_table
from tests.conftest import SKIP_DOWNLOAD_TESTS


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_get_kangxi_radicals_table():
    dataframe = get_kangxi_radicals_table()
    assert len(dataframe) == NUMBER_OF_KANGXI_RADICALS
