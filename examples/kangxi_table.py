# Produces a similar table as:
# https://en.wikipedia.org/wiki/Kangxi_radical#Table_of_radicals
import subprocess

import pandas

from mao.data import get_kangxi_table

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

kangxi_table = get_kangxi_table()

kangxi_table.columns = kangxi_table.columns.str.replace("_glyph", "")

column_names = list(kangxi_table)
new_names = [name[1:] if name.startswith("k") else name for name in column_names]
kangxi_table.columns = new_names

kangxi_table.fillna("", inplace=True)

wiki_url = "https://en.wikipedia.org/wiki/Kangxi_radical#Table_of_radicals"
bootstrap = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"

with open("kangxi_table.html", "w") as file:
    file.write("<!DOCTYPE html><html><head>")
    file.write('<meta charset="utf-8"/>')
    file.write(f'<link rel="stylesheet" href="{bootstrap}">')
    file.write("</head><body>")
    file.write('<div class="container-fluid">')
    file.write('<h1 class="display-4">Unified Kangxi Radicals</h1>')
    file.write(f"<p class='lead'>Compare with: <a href='{wiki_url}'>{wiki_url}</a></p>")
    file.write(kangxi_table.to_html(index=False, index_names=False))
    file.write("</body></html>")

subprocess.call(["xdg-open", "kangxi_table.html"])
