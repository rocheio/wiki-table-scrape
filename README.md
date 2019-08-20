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

# Download a page into a folder of CSV files
python -m wikitablescrape --output-folder="/tmp/scrape" --url="https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"

# Inspect the output
head /tmp/scrape/8000_metres.csv
# "Mountain","Metres","Feet","Range","Location and Notes"
# "Mount Everest","8,848","29,029","Himalayas","Nepal/China"
# "K2","8,611","28,251","Karakoram","Pakistan/China"
# "Kangchenjunga","8,586","28,169","Himalayas","Nepal/India – Highest in India"
# "Lhotse","8,516","27,940","Himalayas","Nepal/China – Climbers ascend Lhotse Face in climbing Everest"
# "Makalu","8,485","27,838","Himalayas","Nepal/China"
# "Cho Oyu","8,201","26,906","Himalayas","Nepal/China – Considered ""easiest"" eight-thousander"
# "Dhaulagiri","8,167","26,795","Himalayas","Nepal – Presumed world's highest from 1808-1838"
# "Manaslu","8,163","26,781","Himalayas","Nepal"
# "Nanga Parbat","8,126","26,660","Himalayas","Pakistan"
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
