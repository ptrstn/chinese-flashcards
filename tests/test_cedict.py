import pytest

from mao.cedict import load_cedict
from tests.conftest import SKIP_DOWNLOAD_TESTS


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_load_cedict():
    cedict_df = load_cedict("test_data/cedict")
    assert "traditional" in cedict_df
    assert "simplified" in cedict_df
    assert "pinyin" in cedict_df
    assert "english" in cedict_df
