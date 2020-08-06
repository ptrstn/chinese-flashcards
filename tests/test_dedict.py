import pathlib
import pytest

from mao.dedict import load_dedict
from tests.conftest import SKIP_DOWNLOAD_TESTS

DEDICT_TEST_PATH = pathlib.Path("test_data", "dedict", "handedict.u8")


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_load_dedict():
    dedict_df = load_dedict(DEDICT_TEST_PATH)
    assert "traditional" in dedict_df
    assert "simplified" in dedict_df
    assert "pinyin" in dedict_df
    assert "german" in dedict_df
