"""Create CSVs from all tables on a Wikipedia article."""

import csv
import logging
import os
import re

from bs4 import BeautifulSoup
import requests


LOGGER = logging.getLogger(__name__)


def scrape(url, output_folder):
    """Scrape the text of a Wikipedia page, parsed from the URL of that page."""
    LOGGER.info(f"Scraping data from {url} into {output_folder}")
    resp = requests.get(url)
    resp.raise_for_status()
    scrape_tables_from_text(resp.text, output_folder)


def scrape_tables_from_text(text, output_folder):
    """Scrape the text from a Wikipedia page into a directory of CSV files."""
    wikitables = get_tables_from_html(text)

    # Create folder for output if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for index, table in enumerate(wikitables):
        header = parse_table_header(table) or f"table_{index+1}"
        filepath = os.path.join(output_folder, csv_filename(header))

        LOGGER.info(f"Writing table {index+1} to {filepath}")
        with open(filepath, mode="w", newline="", encoding="utf-8") as output:
            csv_writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\n")
            for row in parse_rows_from_table(table):
                csv_writer.writerow(row)


def get_tables_from_html(text):
    """Return all HTML tables from Wikipedia page text."""
    soup = BeautifulSoup(text, "lxml")
    return soup.findAll("table")


def parse_rows_from_table(table):
    """Yield CSV rows from a bs4.Tag Wikipedia HTML table."""

    # Hold elements that span multiple rows in a list of
    # dictionaries that track 'rows_left' and 'value'
    saved_rowspans = []
    for row in table.findAll("tr"):
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

    # Strip footnotes and other bracketed sections
    no_brackets = [tag for tag in cell.findAll(text=True) if not tag.startswith("[")]

    cleaned = (
        "".join(no_brackets)  # Combine remaining elements into single string
        .replace("\xa0", " ")  # Replace non-breaking spaces
        .replace("\n", " ")  # Replace newlines
        .strip()
    )

    # Replace all remaining whitespace with single spaces
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def new_span(text):
    """Return a new bs4.Tag <span> element with the given value."""
    return BeautifulSoup(f"<span>{text}</span>", "lxml").html.body.span


def reverse_enum(iterable):
    """Return a reversed iterable with its reversed index."""
    return zip(range(len(iterable)-1, -1, -1), reversed(iterable))


def parse_table_header(table):
    """Return the best title for a bs4.Tag Wikitable, or None if not found."""
    caption = table.find("caption")
    if caption:
        return clean_cell(caption)

    h2 = table.findPrevious("h2")
    if h2:
        header = clean_cell(h2)
        # Try to find a subheader as well
        h3 = table.findPrevious("h3")
        if h3:
            header += f" - {clean_cell(h3)}"
        return header

    return None


def csv_filename(text):
    """Return a normalized filename from a table header for outputting CSV."""
    text = text.replace(",", "")
    text = re.sub(r"[\(|\)]", " ", text.lower())
    text = text.replace(" - ", "-")  # Avoid `a_-_b` formatting in final output
    return "_".join(text.split()) + ".csv"
