"""Parse HTML tables into 2d arrays for writing to CSV."""

import csv
import logging
import os
import re
import sys

from bs4 import BeautifulSoup


LOGGER = logging.getLogger(__name__)


class Error(Exception):
    """Base class for all errors emitted by the parse package."""

    pass


class HtmlTable:
    """A <table> element parsed from HTML as a bs4.Tag."""

    def __init__(self, tag):
        self.tag = tag

    def parse_header(self):
        """Return the best title for an HTML table, or None if not found."""
        caption = self.tag.find("caption")
        if caption:
            return clean_cell(caption)

        h2 = self.tag.findPrevious("h2")
        if h2:
            header = clean_cell(h2)
            # Try to find a subheader as well
            h3 = self.tag.findPrevious("h3")
            if h3:
                header += f" - {clean_cell(h3)}"
            return header

        return None

    def parse_rows(self):
        """Yield CSV rows from a bs4.Tag Wikipedia HTML table."""

        # Hold elements that span many rows in a list of
        # dictionaries that track 'rows_left' and 'value'
        saved_rowspans = []
        for row in self.tag.findAll("tr"):
            cells = row.findAll(["th", "td"])

            # Duplicate column values with a `colspan`
            for index, cell in reverse_enum(cells):
                if cell.has_attr("colspan"):
                    for _ in range(int(cell["colspan"]) - 1):
                        cells.insert(index, cell)

            # If the first row, use it to define width of table
            if len(saved_rowspans) == 0:
                saved_rowspans = [None for _ in cells]
            # Insert values from cells that span into this row
            elif len(cells) != len(saved_rowspans):
                for index, rowspan_data in enumerate(saved_rowspans):
                    if rowspan_data is not None:
                        # Insert the data from previous row; decrement rows left
                        value = rowspan_data["value"]
                        cells.insert(index, value)

                        if saved_rowspans[index]["rows_left"] == 1:
                            saved_rowspans[index] = None
                        else:
                            saved_rowspans[index]["rows_left"] -= 1

            # If an element with rowspan, save it for future cells
            for index, cell in enumerate(cells):
                if cell.has_attr("rowspan"):
                    rowspan_data = {"rows_left": int(cell["rowspan"]), "value": cell}
                    saved_rowspans[index] = rowspan_data

            if cells:
                # Clean the table data of references and unusual whitespace
                cleaned = [clean_cell(cell) for cell in cells]

                # Fill the row with empty columns if some are missing
                # (Some HTML tables leave final empty cells without a <td> tag)
                columns_missing = len(saved_rowspans) - len(cleaned)
                if columns_missing:
                    cleaned += [None] * columns_missing

            yield cleaned

    def write_to_file(self, path):
        """Write the table as CSV to a filepath."""
        with open(path, mode="w", newline="", encoding="utf-8") as output:
            self.write(output)

    def write(self, output=sys.stdout):
        """Write the table as CSV to stdout."""
        writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\n")
        for row in self.parse_rows():
            writer.writerow(row)


class Parser:
    """Parses HtmlTables from text for writing output as CSV."""

    def __init__(self, text):
        self.tables = [HtmlTable(tag) for tag in get_tables_from_html(text)]

    def write_to_dir(self, dir):
        """Write HtmlTables into a directory of CSV files."""
        os.makedirs(dir, exist_ok=True)

        for index, table in enumerate(self.tables):
            header = table.parse_header() or f"table_{index+1}"
            filepath = os.path.join(dir, csv_filename(header))

            LOGGER.info(f"Writing table {index+1} to {filepath}")
            table.write_to_file(filepath)

    def find_table_by_header(self, search):
        """Write a single HtmlTable to stdout from a header."""
        all_headers = []
        matches = []

        for table in self.tables:
            header = table.parse_header()
            if not header:
                continue

            # collect all valid headers for error logging later
            all_headers += [header]

            # search for tables using lowercase characters only
            needle = re.sub(r"[^a-z0-9]", "", search.lower())
            haystack = re.sub(r"[^a-z0-9]", "", header.lower())

            # return early on exact match to account for "table 1" and "table 1b"
            if needle == haystack:
                return table

            # otherwise collect other potential matches for potential error logging
            # e.g. "table 1a" and "table 1b" both matching on "table 1"
            if needle in haystack:
                matches += [table]

        if len(matches) == 1:
            return matches[0]

        if len(matches) > 1:
            raise Error(
                f"{len(matches)} matches for '{search}', specify further from: {all_headers}"
            )

        raise Error(
            f"no matches found for '{search}', specify further from: {all_headers}"
        )


def get_tables_from_html(text):
    """Return all HTML tables from Wikipedia page text."""
    soup = BeautifulSoup(text, "lxml")
    tables = soup.findAll("table")
    # Exclude tables with only one row (need at least header + data)
    tables = [tbl for tbl in tables if len(tbl.findAll("tr")) > 1]
    return tables


def clean_cell(cell):
    """Yield clean string value from a bs4.Tag from Wikipedia."""

    to_remove = (
        # Tooltip references with mouse-over effects
        {"name": "sup", "class": "reference"},
        # Keys for special sorting effects on the table
        {"name": "sup", "class": "sortkey"},
        # Wikipedia `[edit]` buttons
        {"name": "span", "class": "mw-editsection"},
    )

    # Remove extra tags not essential to the table
    for definition in to_remove:
        for tag in cell.findAll(**definition):
            tag.extract()

    # Replace line breaks with spaces
    linebreaks = cell.findAll("br")
    if linebreaks:
        for linebreak in linebreaks:
            linebreak.replace_with(new_span(" "))

    # If cell is only a single image, use its alt-text
    tags = cell.findAll()
    if len(tags) == 1 and tags[0].name == "img":
        return spaces_only(tags[0]["alt"])

    # Reduce remaining cell to text, minus footnotes and other bracketed sections
    tags = [tag for tag in cell.findAll(text=True) if not tag.startswith("[")]
    return spaces_only("".join(tags))


def spaces_only(text):
    """Return text with all whitespace reduced to single spaces (trimmed)."""
    return re.sub(r"\s+", " ", text).strip()


def new_span(text):
    """Return a new bs4.Tag <span> element with the given value."""
    return BeautifulSoup(f"<span>{text}</span>", "lxml").html.body.span


def reverse_enum(iterable):
    """Return a reversed iterable with its reversed index."""
    return zip(range(len(iterable) - 1, -1, -1), reversed(iterable))


def csv_filename(text):
    """Return a normalized filename from a table header for outputting CSV."""
    text = text.replace(",", "")
    text = re.sub(r"[\(|\)]", " ", text.lower())
    text = text.replace(" - ", "-")  # Avoid `a_-_b` formatting in final output
    return "_".join(text.split()) + ".csv"
