"""Test the wikitablescrape package."""

import csv
import os
import tempfile
import unittest

from . import scrape


class TestFiles(unittest.TestCase):
    """Test parsing HTML into CSV using saved files."""

    def test_parse_rows_from_table(self):
        cases = [
            ("testdata/colspan/input.html", "testdata/colspan/output.csv"),
            ("testdata/linebreaks/input.html", "testdata/linebreaks/output.csv"),
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
                self.assertEqual(g, w)


class TestDownload(unittest.TestCase):
    """Test that a request downloads files to a temp folder."""

    def test_scrape_text(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open("testdata/wholepage/volcanoes.html") as htmlfile:
                scrape.scrape_text(
                    text=htmlfile.read(),
                    output_folder=tmpdir,
                )
            want = [
                '1000_metres.csv',
                '2000_metres.csv',
                '3000_metres.csv',
                '4000_metres.csv',
                '5000_metres.csv',
                '6000_metres.csv',
                'from_its_base_on_the_ocean_floor.csv'
            ]
            got = sorted(os.listdir(tmpdir))
            self.assertEqual(got, want)
