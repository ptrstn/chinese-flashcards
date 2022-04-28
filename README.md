[![Actions Status](https://github.com/ptrstn/chinese-flashcards/workflows/Python%20package/badge.svg)](https://github.com/ptrstn/chinese-flashcards/actions)
[![codecov](https://codecov.io/gh/ptrstn/chinese-flashcards/branch/master/graph/badge.svg)](https://codecov.io/gh/ptrstn/chinese-flashcards)

# Chinese Flashcards

A Python package for generating Chinese [Anki](https://apps.ankiweb.net/) flashcards from the [Unihan Unicode](https://en.wikipedia.org/wiki/Han_unification) standard.

## Installation

```bash
pip install --user git+https://github.com/ptrstn/chinese-flashcards
```

## Usage

Check the ```examples``` folder for various usage examples.

### Generate Kangxi Table of Radicals

Generate a HTML table similar to the one as in the [Wikipedia article](https://en.wikipedia.org/wiki/Kangxi_radical#Table_of_radicals) containing the [214 Kangxi radicals](https://en.wikipedia.org/wiki/Kangxi_radical) by using the [Unihan Database](https://unicode.org/charts/unihan.html):

```bash
python examples/kangxi_table.py 
```

## References 

- https://en.wikipedia.org/wiki/Chinese_character_encoding
- https://en.wikipedia.org/wiki/Han_unification
- https://en.wikipedia.org/wiki/Radical_(Chinese_characters)
- https://en.wikipedia.org/wiki/Kangxi_radical
- https://en.wikipedia.org/wiki/List_of_radicals_in_Unicode
- https://en.wikipedia.org/wiki/Variant_Chinese_character
- https://en.wikipedia.org/wiki/Suzhou_numerals
- https://www.unicode.org/reports/tr38/
- https://unicode.org/charts/unihan.html
- https://unicode.org/charts/nameslist/n_2F00.html
- https://www.unicode.org/versions/Unicode13.0.0/ch18.pdf
