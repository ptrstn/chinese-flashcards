import pathlib

import pandas
import requests
from bs4 import BeautifulSoup

UNICODE_KANGXI_URL = "https://unicode.org/charts/nameslist/n_2F00.html"
KANGXI_RADICALS_PATH = pathlib.Path("data", "kangxi", "radicals.csv")


def _get_kangxi_html_table_soup(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("table")


def _extract_kangxi_radical_name(row):
    name = row.find("span", {"class": "name"}).text
    return name.replace("Kangxi Radical ", "")


def _extract_kangxi_radical_unicode(row):
    return row.find("a").text.strip()


def _extract_kangxi_radical_glyph(row):
    return row.find("td", {"class": "c"}).text.strip()


def _find_column_containing_code(row):
    for column in row.findAll("td"):
        if column.find("code"):
            return column


def _extract_unified_unicode(column):
    unihan_code, _ = column.text.split()
    return unihan_code.strip()


def _extract_unified_glyph(column):
    _, unified_glyph = column.text.split()
    return unified_glyph.strip()


def _create_kangxi_dataframe(table):
    column_names = ["name", "unicode", "glyph", "unified_unicode", "unified_glyph"]
    dataframe = pandas.DataFrame(columns=column_names)
    dataframe.index.name = "number"
    rows = table.findAll("tr")
    counter = 1

    for row in rows:
        if row.find("a"):
            dataframe.loc[counter, "name"] = _extract_kangxi_radical_name(row)
            dataframe.loc[counter, "unicode"] = _extract_kangxi_radical_unicode(row)
            dataframe.loc[counter, "glyph"] = _extract_kangxi_radical_glyph(row)
        elif row.find(text="≈"):
            column = _find_column_containing_code(row)
            dataframe.loc[counter, "unified_unicode"] = _extract_unified_unicode(column)
            dataframe.loc[counter, "unified_glyph"] = _extract_unified_glyph(column)
            counter = counter + 1
    return dataframe


def retrieve_unicode_kangxi_table(url=UNICODE_KANGXI_URL):
    print(f"Downloading Kangxi radicals table from {url}...")
    kangxi_table = _get_kangxi_html_table_soup(url)
    dataframe = _create_kangxi_dataframe(kangxi_table)
    return dataframe


def add_is_kangxi_radical_column(dataframe, kangxi_table):
    dataframe.loc[:, "is_kangxi_radical"] = dataframe.glyph.isin(
        list(kangxi_table.unified_glyph)
    )
    return dataframe


def save_kangxi_radicals_table(kangxi_table, path=KANGXI_RADICALS_PATH):
    print(f"Saving Kangxi radicals table to {path}...")
    path.parent.mkdir(exist_ok=True, parents=True)
    kangxi_table.to_csv(path)


def load_kangxi_radicals_table(path=KANGXI_RADICALS_PATH):
    if not pathlib.Path(path).exists():
        kangxi_table = retrieve_unicode_kangxi_table()
        save_kangxi_radicals_table(kangxi_table)
        return kangxi_table
    else:
        return pandas.read_csv(path, index_col=0)


def load_kangxi_radicals_list(path=KANGXI_RADICALS_PATH):
    kangxi_table = load_kangxi_radicals_table(path)
    return list(kangxi_table.unified_glyph)


def unihanify_radical(radical):
    kangxi_table = load_kangxi_radicals_table()
    kangxi_table.set_index("glyph", inplace=True)
    try:
        return kangxi_table.loc[radical, "unified_glyph"]
    except KeyError:
        raise KeyError(f"Ununified radical {radical} does not exist.")


def deunihanify_radical(radical):
    kangxi_table = load_kangxi_radicals_table()
    kangxi_table.set_index("unified_glyph", inplace=True)
    try:
        return kangxi_table.loc[radical, "glyph"]
    except KeyError:
        raise KeyError(f"Unified radical {radical} does not exist.")
