import pandas
import pytest

from mao.constants import NUMBER_OF_KANGXI_RADICALS
from mao.kangxi import retrieve_unicode_kangxi_table, add_is_kangxi_radical_column
from tests.conftest import SKIP_DOWNLOAD_TESTS


@pytest.mark.skipif(SKIP_DOWNLOAD_TESTS, reason="Skipping tests that require downloads")
def test_retrieve_unicode_kangxi_table():
    dataframe = retrieve_unicode_kangxi_table()
    assert len(dataframe) == NUMBER_OF_KANGXI_RADICALS
    assert dataframe.loc[1, "glyph"] == "⼀"
    assert dataframe.loc[1, "unicode"] == "2F00"
    assert dataframe.loc[1, "unified_glyph"] == "一"
    assert dataframe.loc[1, "unified_unicode"] == "4E00"
    assert dataframe.loc[214, "glyph"] != dataframe.loc[214, "unified_glyph"]
    assert dataframe.loc[7, "glyph"] == "⼆"
    assert dataframe.loc[13, "unified_glyph"] == "冂"


def test_add_is_kangxi_radical_column():
    kangxi_table = pandas.DataFrame(data=["⼀", "⼁"], columns=["unified_glyph"])
    dataframe = pandas.DataFrame(data=["𬂛", "⼀"], columns=["glyph"])
    add_is_kangxi_radical_column(dataframe, kangxi_table=kangxi_table)
    dataframe.set_index("glyph", inplace=True)
    assert dataframe.loc["⼀", "is_kangxi_radical"]
    assert not dataframe.loc["𬂛", "is_kangxi_radical"]
