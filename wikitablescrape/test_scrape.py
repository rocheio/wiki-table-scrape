"""Test the wikitablescrape package."""

import csv
import os
import tempfile
import unittest

from . import scrape


class TestFiles(unittest.TestCase):
    """Test parsing HTML into CSVs using saved files."""

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

    def test_scrape_tables_from_text(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open("testdata/wholepage/volcanoes.html") as htmlfile:
                scrape.scrape_tables_from_text(
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


class TestParseTableHeader(unittest.TestCase):

    def test_caption(self):
        """A table with a <caption> will always choose that."""
        html = """
            <h2>Header</h2>
            <table>
                <caption>Caption</caption>
            </table>
        """
        table = scrape.get_tables_from_html(html)[0]
        got = scrape.parse_table_header(table)
        want = "Caption"
        self.assertEqual(got, want)

    def test_h2(self):
        """A table without a caption returns the preceeding <h2>."""
        html = """
            <h2>Header</h2>
            <table></table>
        """
        table = scrape.get_tables_from_html(html)[0]
        got = scrape.parse_table_header(table)
        want = "Header"
        self.assertEqual(got, want)

    def test_h2_and_h3(self):
        """A table with an <h2> header will also check for <h3> subheaders."""
        html = """
            <h2>Header</h2>
            <h3>Subheader</h3>
            <table></table>
        """
        table = scrape.get_tables_from_html(html)[0]
        got = scrape.parse_table_header(table)
        want = "Header - Subheader"
        self.assertEqual(got, want)
