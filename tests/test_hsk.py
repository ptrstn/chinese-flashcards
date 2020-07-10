import pandas

from mao.hsk import read_all_hsk_files, add_hsk_level_column


def test_read_all_hsk_files():
    dataframe = read_all_hsk_files()
    assert len(dataframe[dataframe.hsk_level == 1]) == 174
    assert len(dataframe[dataframe.hsk_level == 2]) == 173
    assert len(dataframe[dataframe.hsk_level == 3]) == 270
    assert len(dataframe[dataframe.hsk_level == 4]) == 447
    assert len(dataframe[dataframe.hsk_level == 5]) == 621
    assert len(dataframe[dataframe.hsk_level == 6]) == 978
    assert len(dataframe) == 2663


def test_add_hsk_level_column():
    dataframe = pandas.DataFrame({"glyph": ["一", "㐂", "衬"]})
    hsk_table = pandas.DataFrame({"glyph": ["衬"], "hsk_level": [3]})
    dataframe = add_hsk_level_column(dataframe, hsk_table=hsk_table)
    dataframe.set_index("glyph", inplace=True)
    assert dataframe.loc["衬", "hsk_level"] == 3
    assert pandas.isna(dataframe.loc["㐂", "hsk_level"])
