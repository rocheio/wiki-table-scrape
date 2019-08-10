"""Create CSVs from all tables on a Wikipedia article."""

import csv
import os

from bs4 import BeautifulSoup
import requests


def scrape(url, output_folder):
    """Create CSVs from all tables in a Wikipedia article.

    ARGS:
        url (str): The full URL of the Wikipedia article to scrape tables from.
        output_folder (str): The directory to write output to.
    """

    # Read tables from Wikipedia article into list of HTML strings
    resp = requests.get(url)
    wikitables = get_tables_from_html(resp.content)

    # Create folder for output if it doesn't exist
    output_name = os.path.basename(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    for index, table in enumerate(wikitables):
        # Make a unique file name for each CSV
        if index == 0:
            filename = output_name
        else:
            filename = output_name + "_" + str(index)

        filepath = os.path.join(output_folder, filename) + ".csv"

        print(f"Writing table {index+1} to {filepath}")
        with open(filepath, mode="w", newline="", encoding="utf-8") as output:
            csv_writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\n")
            for row in parse_rows_from_table(table):
                csv_writer.writerow(row)


def get_tables_from_html(text):
    """Return all HTML tables from Wikipedia page text."""
    soup = BeautifulSoup(text, "lxml")
    table_classes = {"class": ["sortable", "plainrowheaders"]}
    return soup.findAll("table", table_classes)


def parse_rows_from_table(table):
    """Yield CSV rows from a bs4.Tag Wikipedia HTML table."""

    # Hold elements that span multiple rows in a list of
    # dictionaries that track 'rows_left' and 'value'
    saved_rowspans = []
    for row in table.findAll("tr"):
        cells = row.findAll(["th", "td"])

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

    # Strip references from the cell (tooltips on mouse-over)
    references = cell.findAll("sup", {"class": "reference"})
    if references:
        for ref in references:
            ref.extract()

    # Strip sortkeys from the cell
    sortkeys = cell.findAll("span", {"class": "sortkey"})
    if sortkeys:
        for sortkey in sortkeys:
            sortkey.extract()

    # Replace line breaks with spaces
    linebreaks = cell.findAll("br")
    if linebreaks:
        for linebreak in linebreaks:
            linebreak.replace_with(new_span(" "))

    # Strip footnotes from text (`[# 1] links`)
    text_items = cell.findAll(text=True)
    no_footnotes = [text for text in text_items if text[0] != "["]

    cleaned = (
        "".join(no_footnotes)  # Combine remaining elements into single string
        .replace("\xa0", " ")  # Replace non-breaking spaces
        .replace("\n", " ")  # Replace newlines
        .strip()
    )

    return cleaned


def new_span(text):
    """Return a new bs4.Tag <span> element with the given value."""
    return BeautifulSoup(f"<span>{text}</span>", "lxml").html.body.span
