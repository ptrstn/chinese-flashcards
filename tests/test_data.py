import pytest

from mao.constants import NUMBER_OF_KANGXI_RADICALS
from mao.data import get_kangxi_radicals_table
from mao.unihan import download_unihan_zip
from tests.conftest import (
    SKIP_DOWNLOAD_TESTS,
    UNIHAN_TEST_PATH,
    clear_unihan_test_files,
)


def setup_module():
    download_unihan_zip(UNIHAN_TEST_PATH)


def teardown_module():
    clear_unihan_test_files()


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_get_kangxi_radicals_table():
    dataframe = get_kangxi_radicals_table(unihan_base_path=UNIHAN_TEST_PATH)
    assert len(dataframe) == NUMBER_OF_KANGXI_RADICALS
