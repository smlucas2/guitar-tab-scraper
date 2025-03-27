# Tab Scraper
A Python-based web scraper designed to extract guitar tabs and surrounding details of songs from Ultimate Guitar.

## Features
- Scrapes guitar tabs from Ultimate Guitar
- Implements respectful scraping practices with random delays
- Allows user to specify the number of pages to scrape with offset

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tab-scraper.git
   ```
2. Navigate to the project directory:
   ```
   cd tab-scraper
   ```

## Usage
Run the scraper from the command line.
To bulk scrape multiple pages from Ultimate Guitar:
```
python tab_scraper.py --limit <page_limit> --offset <page_offset>
```
Replace `<page_limit>` with the number of pages you want to scrape.
Replace `<page_offset>` with the offset of pages you want to scrape.

To scrape a single song:
```
python tab_scraper.py --tab <tab_url>
```
Replace `<tab_url>` with the URL of the song you want to scrape.
