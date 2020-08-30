import pandas
from bs4 import BeautifulSoup

from han.data.nameslist import (
    request_html_table_soup,
    dismantle_to_entities,
    entitize,
    entity_to_dicts,
    entities_to_dicts, load_kangxi_radicals_nameslist, load_cjk_supplements_nameslist,
)


def test_request_html_table_soup():
    assert request_html_table_soup("https://unicode.org/charts/nameslist/n_2F00.html")
    assert request_html_table_soup("https://unicode.org/charts/nameslist/n_2E80.html")


def test_dismantle_to_entities():
    kangxi_soup = request_html_table_soup(
        "https://unicode.org/charts/nameslist/n_2F00.html"
    )
    kangxi_entities = dismantle_to_entities(kangxi_soup)
    assert len(kangxi_entities) == 214, "Should be 214 Kangxi radicals"

    supplements_soup = request_html_table_soup(
        "https://unicode.org/charts/nameslist/n_2E80.html"
    )
    supplement_entities = dismantle_to_entities(supplements_soup)
    assert len(supplement_entities) == 115, "Should be 115 code points"


def test_entitize():
    elements = ["a1", "a2", "b", "c1", "c2", "c3"]
    entity_indices = [0, 2, 3]
    entities = entitize(elements=elements, indices=entity_indices)
    assert entities == [
        ["a1", "a2"],
        ["b"],
        ["c1", "c2", "c3"],
    ]

    elements = ["unrelevant", "a1", "a2", "b", "c1", "c2", "c3"]
    entity_indices = [1, 3, 4]
    entities = entitize(elements=elements, indices=entity_indices)
    assert entities == [
        ["a1", "a2"],
        ["b"],
        ["c1", "c2", "c3"],
    ]


def test_entity_to_dicts_two_rows():
    html = """
    <tr><td><code><a name="2E81">2E81</a></code></td><td class="c">&nbsp;⺁&nbsp;</td><td colspan="2"><span class="name">Cjk Radical Cliff</span></td></tr>
    <tr><td>&nbsp;</td><td class="char">&nbsp;</td><td class="c">→</td><td><code>5382</code>&nbsp;厂</td></tr>
    <tr><td>&nbsp;</td><td class="char">&nbsp;</td><td class="c">→</td><td><code>20086</code>&nbsp;𠂆</td></tr>
    """
    soup = BeautifulSoup(html, "html.parser")
    entity = dismantle_to_entities(soup)[0]
    entity_dicts = entity_to_dicts(entity)

    assert len(entity_dicts) == 2

    assert entity_dicts[0]["name"] == "Cjk Radical Cliff"
    assert entity_dicts[0]["code_point"] == "2E81"
    assert entity_dicts[0]["glyph"] == "⺁"
    assert entity_dicts[0]["unified_code_point"] == "5382"
    assert entity_dicts[0]["unified_glyph"] == "厂"

    assert entity_dicts[1]["name"] == "Cjk Radical Cliff"
    assert entity_dicts[1]["code_point"] == "2E81"
    assert entity_dicts[1]["glyph"] == "⺁"
    assert entity_dicts[1]["unified_code_point"] == "20086"
    assert entity_dicts[1]["unified_glyph"] == "𠂆"


def test_entity_to_dicts_no_rows():
    html = """
    <tr><td width="1pt"><code><a name="2E80">2E80</a></code></td><td class="c">&nbsp;⺀&nbsp;</td><td colspan="2"><span class="name">Cjk Radical Repeat</span></td></tr>
    """
    soup = BeautifulSoup(html, "html.parser")
    entity = dismantle_to_entities(soup)[0]
    entity_dicts = entity_to_dicts(entity)

    assert len(entity_dicts) == 1

    assert entity_dicts[0]["name"] == "Cjk Radical Repeat"
    assert entity_dicts[0]["code_point"] == "2E80"
    assert entity_dicts[0]["glyph"] == "⺀"
    assert entity_dicts[0]["unified_code_point"] is None
    assert entity_dicts[0]["unified_glyph"] is None


def test_entity_to_dicts_mixed_rows():
    html = """
    <tr><td><code><a name="2EAB">2EAB</a></code></td><td class="c">&nbsp;⺫&nbsp;</td><td colspan="2"><span class="name">Cjk Radical Eye</span></td></tr>
    <tr><td>&nbsp;</td><td class="char">&nbsp;</td><td class="c">•</td><td>form used at top</td></tr>
    <tr><td>&nbsp;</td><td class="char">&nbsp;</td><td class="c">→</td><td><code>2EB2</code>&nbsp;⺲ cjk radical net two</td></tr>
    <tr><td>&nbsp;</td><td class="char">&nbsp;</td><td class="c">→</td><td><code>76EE</code>&nbsp;目</td></tr>
    <tr><td>&nbsp;</td><td class="char">&nbsp;</td><td class="c">→</td><td><code>7F52</code>&nbsp;罒</td></tr>
    """
    soup = BeautifulSoup(html, "html.parser")
    entity = dismantle_to_entities(soup)[0]
    entity_dicts = entity_to_dicts(entity)

    assert len(entity_dicts) == 3

    assert entity_dicts[0]["name"] == "Cjk Radical Eye"
    assert entity_dicts[0]["code_point"] == "2EAB"
    assert entity_dicts[0]["glyph"] == "⺫"
    assert entity_dicts[0]["unified_code_point"] == "2EB2"
    assert entity_dicts[0]["unified_glyph"] == "⺲"

    assert entity_dicts[1]["name"] == "Cjk Radical Eye"
    assert entity_dicts[1]["code_point"] == "2EAB"
    assert entity_dicts[1]["glyph"] == "⺫"
    assert entity_dicts[1]["unified_code_point"] == "76EE"
    assert entity_dicts[1]["unified_glyph"] == "目"


def test_entity_to_dicts_kangxi_nameslist():
    url = "https://unicode.org/charts/nameslist/n_2F00.html"
    soup = request_html_table_soup(url)

    entities = dismantle_to_entities(soup)
    assert len(entities) == 214, "Should be 214 Kangxi radicals"

    kangxi_dicts = entities_to_dicts(entities)
    assert len(kangxi_dicts) > 214, "Should be more than 214 unified radical mappings"


def test_entity_to_dicts_kangxi_nameslist():
    url = "https://unicode.org/charts/nameslist/n_2E80.html"
    soup = request_html_table_soup(url)

    entities = dismantle_to_entities(soup)
    assert len(entities) == 115

    supplements_dicts = entities_to_dicts(entities)
    assert len(supplements_dicts) > 115
    assert supplements_dicts[0]["name"] == "Cjk Radical Repeat"
    assert supplements_dicts[115]["name"] == "Cjk Radical Eat Two"


def test_load_nameslists():
    radicals_df = load_kangxi_radicals_nameslist(base_path="test_data/nameslist")
    assert len(radicals_df) > 214
    supplements_df = load_cjk_supplements_nameslist(base_path="test_data/nameslist")
    assert len(supplements_df) > 115
