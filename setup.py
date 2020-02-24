import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="wikitablescrape",
    version="1.0.4",
    author="Andy Roche",
    author_email="andy@roche.io",
    description="Scrape HTML tables from a Wikipedia page into CSV format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rocheio/wiki-table-scrape",
    packages=setuptools.find_packages(),
    scripts=["scripts/wikitablescrape"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
