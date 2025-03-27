# Tab Scraper
A Python-based web scraper designed to extract guitar tabs and surrounding details of songs from Ultimate Guitar.

## Features
- Scrapes guitar tabs from Ultimate Guitar
- Implements respectful scraping practices with random delays
- Allows user to specify the number of pages to scrape with offset

## Installation
Clone this repository:
```
git clone https://github.com/smlucas2/guitar-tab-scraper.git
```

## Usage
Navigate to the project directory:
```
cd tab-scraper
```

To bulk scrape multiple pages from Ultimate Guitar, run:
```
python tab_scraper.py --limit <page_limit> --offset <page_offset>
```
Replace `<page_limit>` with the number of pages you want to scrape.  
Replace `<page_offset>` with the offset of pages you want to scrape.

To scrape a single song:
```
python tab_scraper.py --tab <tab_url>
```
Replace `<tab_url>` with the URL from Ultimate Guitar of the tab you want to scrape.
