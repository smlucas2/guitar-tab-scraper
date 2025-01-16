# Tab Scraper
A Python-based web scraper designed to extract guitar tabs and surrounding details of songs from Ultimate Guitar.

## Features
- Scrapes guitar tabs from Ultimate Guitar
- Implements respectful scraping practices with random delays
- Allows user to specify the number of pages to scrape

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
python tab_scraper.py -p <number_of_pages>
```
Replace `<number_of_pages>` with the number of pages you want to scrape. Defaults to 1 page.

To scrape a single song:
```
python tab_scraper.py -s <song_url>
```
Replace `<song_url>` with the URL of the song you want to scrape.

### Example
To scrape 5 pages:
```
python tab_scraper.py -p 5
```