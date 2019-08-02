"""Test the scrape script on four articles."""

import csv
import os
import shutil
import unittest

from . import scrape

# Delete previous output folder if it exists, then create a new one
try:
    shutil.rmtree("output")
except FileNotFoundError:
    pass

scrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation",
    output_folder="mountains",
)

scrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_volcanoes_by_elevation",
    output_folder="volcanoes",
)

scrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_career_scoring_leaders",
    output_folder="nba",
)

scrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_highest-grossing_films",
    output_folder="films",
)

# Move all CSV folders into a single 'output' folder
os.makedirs("output")
shutil.move("./mountains", "./output")
shutil.move("./volcanoes", "./output")
shutil.move("./nba", "./output")
shutil.move("./films", "./output")


class TestHTMLFiles(unittest.TestCase):
    def test_mountains(self):
        with open("testdata/mountains/input.html", "r") as htmlfile:
            table = scrape.get_tables_from_html(htmlfile.read())[0]
            got = scrape.parse_rows_from_table(table)

        with open("testdata/mountains/output.csv", "r") as csvfile:
            want = list(csv.reader(csvfile))

        for g, w in zip(got, want):
            assert g == w, f"got '{g}' want '{w}'"
