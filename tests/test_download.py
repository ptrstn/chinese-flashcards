import pytest

from han.data.unihan import download_unihan_zip, read_all_unihan_files
from tests.conftest import (
    SKIP_DOWNLOAD_TESTS,
    clear_unihan_test_files,
    UNIHAN_TEST_PATH,
)


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_download_unihan_zip():
    test_path = UNIHAN_TEST_PATH
    clear_unihan_test_files(test_path)
    assert not test_path.exists()
    download_unihan_zip(test_path)
    dataframe = read_all_unihan_files(test_path)
    assert set(dataframe) == {"unicode", "field", "description"}
    assert len(dataframe) > 1_000_000
    assert test_path.exists()
    clear_unihan_test_files()
