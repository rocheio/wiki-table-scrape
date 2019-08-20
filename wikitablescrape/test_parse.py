"""Test the parse package."""

import csv
import os
import tempfile
import unittest

from bs4 import BeautifulSoup

from . import parse


class TestParseTables(unittest.TestCase):
    def assert_html_to_csv(self, testin, testout):
        """Assert that an HTML input file becomes a CSV output file."""
        with open(testin, "r") as htmlfile:
            tag = parse.get_tables_from_html(htmlfile.read())[0]
            got = parse.HtmlTable(tag).parse_rows()

        with open(testout, "r") as csvfile:
            want = list(csv.reader(csvfile))

        for g, w in zip(got, want):
            self.assertEqual(g, w)

    def test_parse_colspans(self):
        """An HTML `<th colspan>` element becomes many CSV column cells."""
        self.assert_html_to_csv(
            "testdata/colspan/input.html", "testdata/colspan/output.csv"
        )

    def test_parse_rowspans(self):
        """An HTML `<th rowspan>` element becomes many CSV row cells."""
        self.assert_html_to_csv(
            "testdata/rowspan/input.html", "testdata/rowspan/output.csv"
        )

    def test_parse_linebreaks(self):
        """HTML `<br />` elements are parsed out and replaced with spaces."""
        self.assert_html_to_csv(
            "testdata/linebreaks/input.html", "testdata/linebreaks/output.csv"
        )

    def test_quotes_and_smalls(self):
        """HTML `<small>` elements are included and `"` quotes are escaped."""
        self.assert_html_to_csv(
            "testdata/mountains/input.html", "testdata/mountains/output.csv"
        )

    def test_single_img_cells(self):
        """HTML `<img>` elements within cells become alt-text."""
        self.assert_html_to_csv(
            "testdata/imgcells/input.html", "testdata/imgcells/output.csv"
        )

    def test_write_to_dir(self):
        """An HTML page with many `<table>` elements is written to many CSV files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with open("testdata/wholepage/volcanoes.html") as htmlfile:
                parser = parse.Parser(htmlfile.read())
            parser.write_to_dir(tmpdir)
            want = [
                "1000_metres.csv",
                "2000_metres.csv",
                "3000_metres.csv",
                "4000_metres.csv",
                "5000_metres.csv",
                "6000_metres.csv",
                "from_its_base_on_the_ocean_floor.csv",
            ]
            got = sorted(os.listdir(tmpdir))
            self.assertEqual(got, want)


class TestParseTableHeader(unittest.TestCase):
    def assert_header_from_table(self, header, html):
        """Assert that a given header is returned from a given HTML string."""
        tag = BeautifulSoup(html, "lxml").find("table")
        got = parse.HtmlTable(tag).parse_header()
        self.assertEqual(got, header)

    def test_caption(self):
        """A table with a `<caption>` will always use the caption."""
        self.assert_header_from_table(
            "Caption",
            """
            <h2>Header</h2>
            <h3>Subheader</h3>
            <table id="id" class="class">
                <caption>Caption</caption>
            </table>
            """,
        )

    def test_h2(self):
        """A table without a caption returns the preceeding `<h2>`."""
        self.assert_header_from_table(
            "Header",
            """
            <h2>Header</h2>
            <table></table>
            """,
        )

    def test_h2_and_h3(self):
        """A table with an `<h2>` header will also check for `<h3>` subheaders."""
        self.assert_header_from_table(
            "Header - Subheader",
            """
            <h2>Header</h2>
            <h3>Subheader</h3>
            <table></table>
            """,
        )

    def test_table_only(self):
        """A table with no other information will return a default value."""
        self.assert_header_from_table(None, "<table></table>")


class TestFindTablesByHeader(unittest.TestCase):
    def assert_table_found(self, search, want, html):
        """Assert that an HtmlTable can be identified by its header."""
        parser = parse.Parser(html)
        table = parser.find_table_by_header(search)
        self.assertEqual(table.parse_header(), want)

    def test_formatting(self):
        """A match can be made with one table despite formatting differences."""
        pairs = (
            ("caption", "CaptiON!"),
            ("CaptiON!", "caption"),
            ("underscores-hyphens", "UNDERSCORES_HYPHENS"),
        )
        for p1, p2 in pairs:
            html = text_html_table(caption=p2)
            self.assert_table_found(p1, p2, html)

    def test_single_match(self):
        """A single table can be loosely matched from many tables"""
        html = text_html_table(caption="1,000 Metres")
        html += text_html_table(caption="2,000 Metres")
        self.assert_table_found("1000", "1,000 Metres", html)

    def test_no_header_table(self):
        """A match can be made against many tables when one has no header."""
        html = text_html_table()
        html += text_html_table(caption="Table 2")
        self.assert_table_found("table", "Table 2", html)

    def test_no_matches(self):
        """An error is raised when no matches are found."""
        html = text_html_table(caption="table 1")
        html += text_html_table(caption="table 2")
        with self.assertRaises(parse.Error):
            self.assert_table_found("n/a", "", html)

    def test_many_matches(self):
        """An error is raised when more than one match is found."""
        html = text_html_table(caption="table 1")
        html += text_html_table(caption="table 2")
        with self.assertRaises(parse.Error):
            self.assert_table_found("table", "", html)


def text_html_table(caption=None):
    """Return a text HtmlTable with a given caption for testing."""
    if caption:
        caption = f"<caption>{caption}</caption>"

    return f"""
        <table>
            {caption}
            <tr></tr>
            <tr></tr>
        </table>
        """
