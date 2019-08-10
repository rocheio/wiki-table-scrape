"""Test the wikitablescrape package."""

import csv
import unittest

from . import scrape


class TestFiles(unittest.TestCase):
    """Test parsing HTML into CSV using saved files."""

    def test_parse_rows_from_table(self):
        cases = [
            ("testdata/mountains/input.html", "testdata/mountains/output.csv"),
            ("testdata/rowspan/input.html", "testdata/rowspan/output.csv"),
        ]
        for testin, testout in cases:
            with open(testin, "r") as htmlfile:
                table = scrape.get_tables_from_html(htmlfile.read())[0]
                got = scrape.parse_rows_from_table(table)

            with open(testout, "r") as csvfile:
                want = list(csv.reader(csvfile))

            for g, w in zip(got, want):
                assert g == w, f"got '{g}' want '{w}'"
