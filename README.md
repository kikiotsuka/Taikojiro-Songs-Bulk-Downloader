# Taikojiro-Songs-Bulk-Downloader
Download songs for taikojiro in bulk

## Dependencies

requests, bs4

## Usage

Run `scrape.py` to produce csv file containing list of taikojiro songs

Run `bulk-download.py` to bulk download list from the given csv file

The data in the csv file is in the form of `song title|download url|song description|download count`

It is recommended to manually edit the generated csv file to only download files you want
