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
python -m wikitablescrape --url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation" --output-folder="/tmp/mountains"

# Inspect the output
ls /tmp/mountains
# mountains.csv   mountains_2.csv mountains_4.csv mountains_6.csv mountains_8.csv
# mountains_1.csv mountains_3.csv mountains_5.csv mountains_7.csv

head -5 /tmp/mountains/mountains.csv
# "Mountain","Metres","Feet","Range","Location and Notes"
# "Mount Everest","8,848","29,029","Himalayas","Nepal/China"
# "K2","8,611","28,251","Karakoram","Pakistan/China"
# "Kangchenjunga","8,586","28,169","Himalayas","Nepal/India – Highest in India"
# "Lhotse","8,516","27,940","Himalayas","Nepal/China – Climbers ascend Lhotse Face in climbing Everest"
```

## Local Development

This package depends on [Python 3][python]. Follow these steps if you want to develop and test the package locally.

```sh
# Create and activate a virtualenv for Python 3
python3 -m venv venv
. venv/bin/activate

# Install requirements from pip
pip install -r requirements.txt

# Run unit tests and code coverage checks
coverage run --source wikitablescrape -m unittest discover && coverage report --fail-under=50

# (Optionally) See coverage data
coverage html && open htmlcov/index.html
```

If on Windows, you may also need to download the  `.whl` for the [`lxml`][lxml] parser and install it locally.

## Disclaimers

The script won't give you 100% clean data for every page on Wikipedia, but it will get you most of the way there. You can see the output from the pages for [mountain height][wiki-mountains], [volcano height][wiki-volcano], [NBA scores][wiki-nba], and [the highest-grossing films][wiki-films] in the `output` folder of this repo.

I only plan to add features to this module as I need them, but if you would like to contribute, please open an issue or pull request.

If you'd like to read more about this module, please check out [my blog post][blog-post].

[beautiful-soup]: https://www.crummy.com/software/BeautifulSoup/
[blog-post]: https://roche.io/2016/05/08/scrape-wikipedia-with-python
[lxml]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
[python]: https://www.python.org/downloads/
[requests]: http://docs.python-requests.org/en/master/
[wiki-films]: https://en.wikipedia.org/wiki/List_of_highest-grossing_films
[wiki-mountains]: https://en.wikipedia.org/wiki/List_of_mountains_by_elevation
[wiki-nba]: https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_career_scoring_leaders
[wiki-volcano]: https://en.wikipedia.org/wiki/List_of_volcanoes_by_elevation
