# wiki-table-scrape

Scrape HTML tables from a Wikipedia page into CSV format.

`wikitablescrape` can be used as a shell command or imported as a Python package.

## Why?

This tool makes it easy to download any Wikipedia table via CLI in a format ready for text processing.

This is especially useful when combined with a tool like [`xsv`](https://github.com/BurntSushi/xsv).

##### Year Distribution of Costliest Atlantic Hurricanes

```
wikitablescrape --url='https://en.wikipedia.org/wiki/List_of_costliest_Atlantic_hurricanes' --header='costliest' | xsv select "Season" | xsv stats --median | xsv select field,min,max,median,mean,stddev | xsv table
```
```
field   min   max   median  mean                stddev
Season  1965  2018  2002    1999.1228070175441  12.900523823770502
```

##### Country / Market Distribution of Best-selling Music Artists

```
wikitablescrape --url='https://en.wikipedia.org/wiki/List_of_best-selling_music_artists' --header='100 million' | xsv select 'Country / Market' | xsv frequency | xsv table
```
```
field             value                         count
Country / Market  United States                 26
Country / Market  United Kingdom                10
Country / Market  United Kingdom United States  1
Country / Market  Australia                     1
Country / Market  Spain                         1
Country / Market  Japan                         1
```

## Installation

You can download the package from [PyPI](https://pypi.org/project/wikitablescrape/) or build from source using [Python 3](https://www.python.org/downloads/).

### As a system-level Python package

```sh
python3 -m pip install wikitablescrape
wikitablescrape --help
```

### In a virtual environment

```sh
python3 -m venv venv
. venv/bin/activate
pip install wikitablescrape
wikitablescrape --help
```

### Build from source

```sh
git clone https://github.com/rocheio/wiki-table-scrape
cd ./wiki-table-scrape
python3 -m venv venv
. venv/bin/activate
python setup.py install
wikitablescrape --help
```

## Sample Commands

##### Write a single table to stdout

```sh
wikitablescrape --url="https://en.wikipedia.org/wiki/List_of_highest-grossing_films" --header="films by year" | tee >(head -1) >(tail -5) >/dev/null
```
```csv
"Year","Title","Worldwide gross","Budget","Reference(s)"
"2015","Star Wars: The Force Awakens","$2,068,223,624","$245,000,000",""
"2016","Captain America: Civil War","$1,153,304,495","$250,000,000",""
"2017","Star Wars: The Last Jedi","$1,332,539,889","$200,000,000",""
"2018","Avengers: Infinity War","$2,048,359,754","$316,000,000–400,000,000",""
"2019","Avengers: Endgame","$2,796,255,086","$356,000,000",""
```

##### Download all tables on a page into a folder of CSV files

```sh
wikitablescrape --url="https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages#Top-100_list" --output-folder="/tmp/scrape"
```
```
Parsing all tables from 'https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages#Top-100_list' into '/tmp/scrape'
Writing table 1 to /tmp/scrape/top_100_list.csv
Writing table 2 to /tmp/scrape/countries.csv
Writing table 3 to /tmp/scrape/cities.csv
Writing table 4 to /tmp/scrape/people.csv
Writing table 5 to /tmp/scrape/people_singers.csv
Writing table 6 to /tmp/scrape/people_actors.csv
Writing table 7 to /tmp/scrape/people_athletes.csv
Writing table 8 to /tmp/scrape/people_modern_political_leaders.csv
Writing table 9 to /tmp/scrape/people_pre_modern_people.csv
Writing table 10 to /tmp/scrape/people_3rd_millennium_people.csv
Writing table 11 to /tmp/scrape/progression_of_the_most_viewed_millennial_persons_on_wikipedia.csv
Writing table 12 to /tmp/scrape/music_bands_historical_most_viewed_3rd_millennium_persons.csv
Writing table 13 to /tmp/scrape/sport_teams_historical_most_viewed_3rd_millennium_persons.csv
Writing table 14 to /tmp/scrape/films_and_tv_series_historical_most_viewed_3rd_millennium_persons.csv
Writing table 15 to /tmp/scrape/albums_historical_most_viewed_3rd_millennium_persons.csv
Writing table 16 to /tmp/scrape/books_and_book_series_historical_most_viewed_3rd_millennium_persons.csv
Writing table 17 to /tmp/scrape/books_and_book_series_pre_modern_books_and_texts.csv
```

```sh
head -5 /tmp/scrape/cities.csv
```
```csv
"Rank","Page","Continent","Views in millions"
"1","New York City","North America","69"
"2","London","Europe","57"
"2","Singapore","Asia","57"
"*","Angelsberg","Europe","44"
```

## Testing

```sh
./scripts/test.sh

# Show coverage data in a browser
coverage html && open htmlcov/index.html
```

## Sample Articles for Scraping

- [Top 25 Articles this Month](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report)
- [Top 100 Articles of All Time](https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages#Top-100_list)

## Contributing

If you would like to contribute to this module, please open an issue or pull request.

## More Information

If you'd like to read more about this module, please check out [my blog post][blog-post] from the initial release.

[blog-post]: https://roche.io/2016/05/scrape-wikipedia-with-python
