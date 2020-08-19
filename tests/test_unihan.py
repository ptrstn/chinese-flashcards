import pathlib

import pytest

from han.data.unihan import download_unihan_zip, read_unihan_field_values
from tests.conftest import (
    SKIP_DOWNLOAD_TESTS,
    clear_unihan_test_files,
    UNIHAN_TEST_PATH,
)


def setup_module():
    download_unihan_zip(UNIHAN_TEST_PATH)


def teardown_module():
    clear_unihan_test_files()


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_read_unihan_field_values():
    file_path = pathlib.Path(UNIHAN_TEST_PATH, "Unihan_Readings.txt")
    field_values = read_unihan_field_values(file_path)

    expected_field_values = [
        "kCantonese",
        "kDefinition",
        "kHangul",
        "kHanyuPinlu",
        "kHanyuPinyin",
        "kJapaneseKun",
        "kJapaneseOn",
        "kKorean",
        "kMandarin",
        "kTang",
        "kTGHZ2013",
        "kVietnamese",
        "kXHC1983",
    ]

    assert field_values == expected_field_values
