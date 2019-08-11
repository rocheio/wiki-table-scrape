# wiki-table-scrape

Scrape HTML tables from a Wikipedia page into CSV format.

Read more about the initial project in [the blog post][blog-post].

## Usage

```sh
# Create and activate a virtualenv for Python 3
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Download a page into a folder of CSV files
python -m wikitablescrape --output-folder="/tmp/scrape" --url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"

# Inspect the output
ls -l /tmp/scrape | awk '{print $5"\t"$9}'
# 10817	1000_metres.csv
# 17354	2000_metres.csv
# 18894	3000_metres.csv
# 16955	4000_metres.csv
# 5304	5000_metres.csv
# 6633	6000_metres.csv
# 7156	7000_metres.csv
# 1098	8000_metres.csv
# 7984	under_1000_metres.csv

head -5 /tmp/scrape/8000_metres.csv
# "Mountain","Metres","Feet","Range","Location and Notes"
# "Mount Everest","8,848","29,029","Himalayas","Nepal/China"
# "K2","8,611","28,251","Karakoram","Pakistan/China"
# "Kangchenjunga","8,586","28,169","Himalayas","Nepal/India – Highest in India"
# "Lhotse","8,516","27,940","Himalayas","Nepal/China – Climbers ascend Lhotse Face in climbing Everest"
```

## Local Development

This package depends on [Python 3](https://www.python.org/downloads/). Follow these steps if you want to develop and test the package locally.

```sh
# Create and activate a virtualenv for Python 3
python3 -m venv venv
. venv/bin/activate

# Install requirements from pip
pip install -r requirements.txt

# Run unit tests and code coverage checks
coverage run --source wikitablescrape -m unittest discover && coverage report --fail-under=80

# (Optionally) See coverage data
coverage html && open htmlcov/index.html
```

If on Windows, you may also need to download the  `.whl` for the [`lxml`](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) parser and install it locally.

### Where to Start?

- [Top 25 Articles this Month](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report)
- [Top 100 Articles of All Time](https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages#Top-100_list)

## Contributing

If you would like to contribute to this module, please open an issue or pull request.

If you'd like to read more about this module, please check out [my blog post][blog-post].

[blog-post]: https://roche.io/2016/05/08/scrape-wikipedia-with-python
