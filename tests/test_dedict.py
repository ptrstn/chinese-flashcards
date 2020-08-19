import pytest

from mao.dedict import load_dedict
from tests.conftest import SKIP_DOWNLOAD_TESTS


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_load_dedict():
    dedict_df = load_dedict("test_data/dedict")
    assert "traditional" in dedict_df
    assert "simplified" in dedict_df
    assert "pinyin" in dedict_df
    assert "german" in dedict_df
