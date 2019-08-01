import argparse

from . import scrape


def main():
    parser = argparse.ArgumentParser(description='Scrape tables from Wikipedia pages into CSV')
    parser.add_argument('--url', help='URL of the Wikipedia page to scrape', required=True)
    parser.add_argument('--output-folder', help='Folder where CSV files will be saved', required=True)
    args = parser.parse_args()

    print(f"Scraping data from {args.url} into {args.output_folder}")
    scrape.scrape(
        url=args.url,
        output_folder=args.output_folder
    )


if __name__ == '__main__':
    main()
