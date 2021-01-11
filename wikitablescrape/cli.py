import argparse
import logging

import requests

from .parse import Parser, LOGGER, DEFAULT_NEWLINE_REPLACE


def main():
    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(logging.StreamHandler())

    cli = argparse.ArgumentParser(
        description="Scrape tables from Wikipedia pages into CSV"
    )
    cli.add_argument("--debug", help="Enable debug-level logging", default=False)
    cli.add_argument("--url", help="URL of the Wikipedia page to scrape", required=True)
    cli.add_argument("--output-folder", help="Folder to write all tables from a url")
    cli.add_argument("--header", help="Write a single HTML table by header to stdout")
    cli.add_argument(
        "--newline-replace",
        help="Value to replace HTML breaklines (<br>)",
        default=DEFAULT_NEWLINE_REPLACE,
    )

    args = cli.parse_args()

    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    resp = requests.get(args.url)
    resp.raise_for_status()

    parser = Parser(resp.text, args.newline_replace)

    if args.output_folder:
        LOGGER.info(f"Parsing all tables from '{args.url}' into '{args.output_folder}'")
        parser.write_to_dir(args.output_folder)
        return

    if args.header:
        LOGGER.debug(f"Parsing table '{args.header}' from '{args.url}'")
        table = parser.find_table_by_header(args.header)
        table.write()
        return

    LOGGER.error("Must provide either an `--output-folder` or `--header`")
