import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wiki-table-scrape-rocheio",
    version="1.0.0",
    author="Andy Roche",
    author_email="andy@roche.io",
    description="Scrape HTML tables from a Wikipedia page into CSV format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rocheio/wiki-table-scrape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
