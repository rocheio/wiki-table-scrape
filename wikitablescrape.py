"""Create CSVs from all tables on a Wikipedia article."""

import os
import requests
from bs4 import BeautifulSoup

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"
OUTPUT_NAME = "mountains"


def scrape(url, output_name):
    """Create CSVs from all tables in a Wikipedia article."""

    # Read tables from Wikipedia article into list of HTML strings
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    table_classes = {"class": ["sortable", "plainrowheaders"]}
    wikitables = soup.findAll("table", table_classes)

    # Create folder for output if it doesn't exist
    try:
        os.mkdir(output_name)
    except Exception:
        # Generic OS Error
        pass

    for index, table in enumerate(wikitables):
        # Make a unique file name for each CSV
        if index == 0:
            filename = output_name
        else:
            filename = output_name + '_' + str(index)

        filepath = os.path.join(output_name, filename) + '.csv'

        with open(filepath, 'w') as output:
            write_html_table_to_csv(table, output)


def write_html_table_to_csv(table, output):
    """Write HTML table from Wikipedia to a CSV file."""

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
                    value = rowspan_data['value']
                    cells.insert(index, value)

                    if saved_rowspans[index]['rows_left'] == 1:
                        saved_rowspans[index] = None
                    else:
                        saved_rowspans[index]['rows_left'] -= 1

        # If an element with rowspan, save it for future cells
        for index, cell in enumerate(cells):
            if cell.has_key("rowspan"):
                rowspan_data = {
                    'rows_left': int(cell["rowspan"]),
                    'value': cell,
                }
                saved_rowspans[index] = rowspan_data

        if cells:
            cleaned = clean_data(cells)
            output.write(cleaned)


def clean_data(row):
    """Clean table row list from Wikipedia into a string for CSV."""

    cleaned_cells = []

    for cell in row:
        # Strip references from the cell
        references = cell.findAll("sup", {"class": "reference"})
        if references:
            for ref in references:
                ref.extract()

        # Strip sortkeys from the cell
        sortkeys = cell.findAll("span", {"class": "sortkey"})
        if sortkeys:
            for ref in sortkeys:
                ref.extract()

        # Strip footnotes from text and join into a single string
        text_items = cell.findAll(text=True)
        no_footnotes = [text for text in text_items if text[0] != '[']
        puretext = ''.join(no_footnotes)

        # Replace non-breaking spaces with regular spaces
        puretext = puretext.replace('\xa0', ' ')
        # Escape double quotes for CSV, then surround with double quotes
        puretext = puretext.replace('"', '""')
        quoted = '"' + puretext + '"'

        cleaned_cells += [quoted]

    string = ', '.join(cleaned_cells) + '\n'
    print(string)
    return string


if __name__ == '__main__':
    scrape(WIKI_URL, OUTPUT_NAME)
