import pandas
import pytest

from mao.constants import NUMBER_OF_KANGXI_RADICALS
from mao.data.kangxi import (
    retrieve_unicode_kangxi_table,
    add_is_kangxi_radical_column,
    unihanify_radical,
    deunihanify_radical,
)
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


def test_unihanify_radical():
    radical = "⾾"
    unified_radical = unihanify_radical(radical)
    assert unified_radical == "鬥"
    assert ord(radical) == 12222
    assert ord(unified_radical) == 39717

    with pytest.raises(KeyError):
        unihanify_radical("鬥")


def test_deunihanify_radical():
    unified_radical = "鬥"
    deunified_radical = deunihanify_radical(unified_radical)
    assert deunified_radical == "⾾"
    assert ord(unified_radical) == 39717
    assert ord(deunified_radical) == 12222

    with pytest.raises(KeyError):
        deunihanify_radical("⾾")
