# wiki-table-scrape

Scrape HTML tables from a Wikipedia page into CSV format.

Read more about the initial project in [the blog post][blog-post].

## Usage

This package depends on [Python 3](https://www.python.org/downloads/).

```sh
# Create and activate a virtualenv for Python 3
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Find a single HTML table and write as CSV to stdout
python -m wikitablescrape --url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation" --header="8000 metres" | head -5
# "Mountain","Metres","Feet","Range","Location and Notes"
# "Mount Everest","8,848","29,029","Himalayas","Nepal/China"
# "K2","8,611","28,251","Karakoram","Pakistan/China"
# "Kangchenjunga","8,586","28,169","Himalayas","Nepal/India – Highest in India"
# "Lhotse","8,516","27,940","Himalayas","Nepal/China – Climbers ascend Lhotse Face in climbing Everest"

# Download an entire page of CSV files into a folder
python -m wikitablescrape --url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation" --output-folder="/tmp/scrape"
```

## Testing

```sh
# Run unit tests and code coverage checks
coverage run --source wikitablescrape -m unittest discover && coverage report --fail-under=80

# (Optionally) See coverage data
coverage html && open htmlcov/index.html
```

## Sample Articles for Scraping

- [Top 25 Articles this Month](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report)
- [Top 100 Articles of All Time](https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages#Top-100_list)

## Contributing

If you would like to contribute to this module, please open an issue or pull request.

## More Information

If you'd like to read more about this module, please check out [my blog post][blog-post].

[blog-post]: https://roche.io/2016/05/scrape-wikipedia-with-python
