# Wikitablescrape

#### Scrape all tables from a Wikipedia article into CSV files on your computer.

To run the script, you must have [Python3][python] and the [Beautiful Soup][beautiful-soup] package installed. You can install Beautiful Soup from pip using `pip install bs4`.

Replace the values of `OUTPUT_NAME` and `WIKI_URL` at the top of the script with the values you want. All large tables from the article at `WIKI_URL` will be downloaded to multiple CSV files in a folder named `OUTPUT_NAME` in the same directory as your script.

The script won't give you 100% clean data for every page on Wikipedia, but it will get you most of the way there and handle the three topics I mention in [my blog post][blog-post]. You can see the output from the pages for [mountain height][wiki-mountains], [volcano height][wiki-volcano], [NBA scores][wiki-nba], and [the highest-grossing films][wiki-films] in the `output` folder.

Please open an Issue or Pull Request if you find a bug or have suggestions for improvement.

[beautiful-soup]: https://www.crummy.com/software/BeautifulSoup/
[blog-post]: https://roche.io/data/2016/05/08/scrape-wikipedia-into-csv.html
[python]: https://www.python.org/downloads/
[wiki-films]: https://en.wikipedia.org/wiki/List_of_highest-grossing_films
[wiki-mountains]: https://en.wikipedia.org/wiki/List_of_mountains_by_elevation
[wiki-nba]: https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_career_scoring_leaders
[wiki-volcano]: https://en.wikipedia.org/wiki/List_of_volcanoes_by_elevation
