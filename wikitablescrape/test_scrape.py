"""Test the wikitablescrape package."""

import csv
import os
import tempfile
import unittest

from . import scrape

from bs4 import BeautifulSoup


class TestParseTables(unittest.TestCase):
    """Test parsing HTML into CSV tables using saved files."""

    def assert_html_to_csv(self, testin, testout):
        """Assert that an HTML input file becomes an HTML output file."""
        with open(testin, "r") as htmlfile:
            table = scrape.get_tables_from_html(htmlfile.read())[0]
            got = scrape.parse_rows_from_table(table)

        with open(testout, "r") as csvfile:
            want = list(csv.reader(csvfile))

        for g, w in zip(got, want):
            self.assertEqual(g, w)

    def test_parse_colspans(self):
        """Confirm that a <th colspan> element becomes multiple CSV column cells."""
        self.assert_html_to_csv("testdata/colspan/input.html", "testdata/colspan/output.csv")

    def test_parse_rowspans(self):
        """Confirm that a <th rowspan> element becomes multiple CSV row cells."""
        self.assert_html_to_csv("testdata/rowspan/input.html", "testdata/rowspan/output.csv")

    def test_parse_linebreaks(self):
        """Confirm that <br /> elements are parsed out and replaced with spaces."""
        self.assert_html_to_csv("testdata/linebreaks/input.html", "testdata/linebreaks/output.csv")

    def test_quotes_and_smalls(self):
        """Confirm that <small> elements are included and `"` quotes are escaped."""
        self.assert_html_to_csv("testdata/mountains/input.html", "testdata/mountains/output.csv")

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

    def assert_header_from_table(self, header, html):
        """Assert that a given header is returned from a given HTML string."""
        table = BeautifulSoup(html, "lxml").find("table")
        got = scrape.parse_table_header(table)
        self.assertEqual(got, header)

    def test_caption(self):
        """A table with a <caption> will always use the caption."""
        self.assert_header_from_table("Caption", """
            <h2>Header</h2>
            <h3>Subheader</h3>
            <table id="id" class="class">
                <caption>Caption</caption>
            </table>
        """)

    def test_h2(self):
        """A table without a caption returns the preceeding <h2>."""
        self.assert_header_from_table("Header", """
            <h2>Header</h2>
            <table></table>
        """)

    def test_h2_and_h3(self):
        """A table with an <h2> header will also check for <h3> subheaders."""
        self.assert_header_from_table("Header - Subheader", """
            <h2>Header</h2>
            <h3>Subheader</h3>
            <table></table>
        """)

    def test_table_only(self):
        """A table with no other information will return a default value."""
        self.assert_header_from_table(None, """
            <table></table>
        """)
