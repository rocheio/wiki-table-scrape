import argparse
import logging

from . import scrape


def main():
    parser = argparse.ArgumentParser(description='Scrape tables from Wikipedia pages into CSV')
    parser.add_argument('--url', help='URL of the Wikipedia page to scrape', required=True)
    parser.add_argument('--output-folder', help='Folder where CSV files will be saved', required=True)
    parser.add_argument('--debug', help='Enable debug-level logging', default=False)
    args = parser.parse_args()

    if args.debug:
        scrape.LOGGER.setLevel(logging.DEBUG)

    scrape.scrape(
        url=args.url,
        output_folder=args.output_folder
    )


if __name__ == '__main__':
    scrape.LOGGER.setLevel(logging.INFO)
    scrape.LOGGER.addHandler(logging.StreamHandler())
    main()
