from pathlib import Path

import pandas
import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError

NAMESLIST_BASE_PATH = Path("data", "nameslist")


def request_html_table_soup(url) -> BeautifulSoup:
    try:
        response = requests.get(url)
    except SSLError:
        response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("table")


def entitize(elements, indices):
    """
    Turn coherent data in an elements list into single entity units.
    The entity units are described by the indicies.
    """
    entities = []
    for idx, entity_index in enumerate(indices):
        next_index = indices[idx + 1] if idx < len(indices) - 1 else None
        entity = elements[entity_index:next_index]
        entities.append(entity)
    return entities


def dismantle_to_entities(soup: BeautifulSoup) -> list:
    rows = soup.findAll("tr")
    entity_indices = [
        index for index, row in enumerate(rows) if row.find("td").find("code")
    ]
    entities = entitize(elements=rows, indices=entity_indices)
    return entities


def entities_to_dicts(entities: list) -> list:
    return [
        dict_element for entity in entities for dict_element in entity_to_dicts(entity)
    ]


def find_name_text(row):
    return row.find("span", {"class": "name"}).text


def find_code_point_text(row):
    return row.find("code").text


def find_glyph_text(row):
    return row.find("td", {"class": "c"}).text.strip()


def find_unified_glyph_text(row):
    return row.find_all("td")[-1].contents[1].strip()[0]


def entity_to_dicts(entity: list) -> list:
    name = find_name_text(entity[0])
    code_point = find_code_point_text(entity[0])
    glyph = find_glyph_text(entity[0])

    return (
        [
            {
                "name": name,
                "code_point": code_point,
                "glyph": glyph,
                "unified_code_point": find_code_point_text(row),
                "unified_glyph": find_unified_glyph_text(row),
            }
            for row in entity[1:]
            if row.find("code")
        ]
        if len(entity) > 1
        else [
            {
                "name": name,
                "code_point": code_point,
                "glyph": glyph,
                "unified_code_point": None,
                "unified_glyph": None,
            }
        ]
    )


def load_nameslist(url, base_path=NAMESLIST_BASE_PATH):
    stem = Path(url).stem
    feather_path = Path(base_path, f"{stem}.feather")
    try:
        return pandas.read_feather(feather_path)
    except FileNotFoundError:
        soup = request_html_table_soup(url)
        entities = dismantle_to_entities(soup)
        dicts = entities_to_dicts(entities)
        df = pandas.DataFrame(dicts)
        print(
            f"Saving {stem} nameslist DataFrame in Feather format to {feather_path}..."
        )
        feather_path.parent.mkdir(exist_ok=True, parents=True)
        df.to_feather(feather_path)
        return df


def load_kangxi_radicals_nameslist(base_path=NAMESLIST_BASE_PATH):
    url = "https://unicode.org/charts/nameslist/n_2F00.html"
    return load_nameslist(url=url, base_path=base_path)


def load_cjk_supplements_nameslist(base_path=NAMESLIST_BASE_PATH):
    url = "https://unicode.org/charts/nameslist/n_2E80.html"
    return load_nameslist(url=url, base_path=base_path)
