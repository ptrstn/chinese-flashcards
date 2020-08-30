import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError


def request_html_table_soup(url) -> BeautifulSoup:
    try:
        response = requests.get(url)
    except SSLError:
        response = requests.get(url, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("table")


def entitize(elements, indices):
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
