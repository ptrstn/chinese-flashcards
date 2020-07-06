import pytest

from mao.unihan import download_unihan_zip
from tests.conftest import SKIP_DOWNLOAD_TESTS, clear_unihan_test_files, UNIHAN_TEST_PATH


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_download_unihan_zip():
    test_path = UNIHAN_TEST_PATH
    assert not test_path.exists()
    download_unihan_zip(test_path)
    assert test_path.exists()
    clear_unihan_test_files()
