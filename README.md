# wiki-table-scrape

Scrape all the tables from a Wikipedia article into a folder of CSV files.

You can read more about it in [the blog post][blog-post]

## Installation

This is a [Python 3][python] module that depends on the [Beautiful Soup][beautiful-soup] and [requests][requests] packages.

```sh
# Create and activate a virtualenv for Python 3
python3 -m venv venv
. venv/bin/activate

# Install requirements from pip
pip install -r requirements.txt

# Test the program by downloading sample tables
python test_wikitablescrape.py
```

If on Windows, you also need to download the  `.whl` for the [`lxml`][lxml] parser and install it locally.

## Usage

Just import the module and call the `scrape` function. Pass it the full URL of a Wikipedia article, and a simple string (no special characters or filetypes) for the output name. The output will all be written to the `output_name` folder, with files named `output_name.csv`, `output_name_1.csv`, etc.

```python
import wikitablescrape

wikitablescrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_highest-grossing_films",
    output_name="films"
)
```

Inspecting the output with Bash gives the following results:

```text
$ ls films/
films.csv  films_1.csv  films_2.csv  films_3.csv

$ cat films/films_1.csv
"Rank","Title","Worldwide gross (2014 $)","Year"
"1","Gone with the Wind","$3,440,000,000","1939"
"2","Avatar","$3,020,000,000","2009"
"3","Star Wars","$2,825,000,000","1977"
"4","Titanic","$2,516,000,000","1997"
"5","The Sound of Music","$2,366,000,000","1965"
"6","E.T. the Extra-Terrestrial","$2,310,000,000","1982"
"7","The Ten Commandments","$2,187,000,000","1956"
"8","Doctor Zhivago","$2,073,000,000","1965"
"9","Jaws","$2,027,000,000","1975"
"10","Snow White and the Seven Dwarfs","$1,819,000,000","1937"
```

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
