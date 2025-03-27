# -*- coding: utf-8 -*-

"""
Tab Scraper

This utility will scrape the "Ultimate Guitar" website and obtain the tabulations.
"""

import json
import random
import time
import sys
from typing import Optional, List, Dict, Union

import requests
from bs4 import BeautifulSoup

from tab_scraper.util import SongCacher, SongDetailsOutputer, SongLogger

NestedDict = Dict[str, Union[str, "NestedDict"]]

class UltimateGuitarScraper:

    def __init__(
            self,
            out_dir: Optional[str] = None,
            cache_dir: Optional[str] = None,
            log_dir: Optional[str] = None
        ) -> None:
        """
        Initialize the UltimateGuitarScraper with optional custom directories.
        
        Args:
            out_dir: Optional custom directory for output files. If None, uses default directory.
            cache_dir: Optional custom directory for cache files. If None, uses default directory.
            log_dir: Optional custom directory for log files. If None, uses default directory.
        """
        self.outputer = SongDetailsOutputer(out_dir)
        self.cacher = SongCacher(cache_dir)
        self.logger = SongLogger(log_dir, __name__)

    def scrape_songs(self, limit: Optional[int] = None, offset: Optional[int] = 0) -> None:
        """
        Scrape songs from Ultimate Guitar website.
        
        Args:
            limit: Optional maximum number of pages to scrape. If None, scrape until the end.
            offset: Optional starting page number (0-based index). Default is 0 (start from page 1).
        """
        self._print_and_log_info("Beginning scraping of Ultimate Guitar for tabs.")
        start_time = time.time()

        if limit is not None:
            limit = self._normalize_limit(limit)
        offset = self._normalize_offset(offset)
            
        song_details = []
        try:
            page = offset + 1
            pages_scraped = 0
            
            while True:
                if limit is not None and pages_scraped >= limit:
                    self.logger.info(f"Reached limit of {limit} pages. Stopping scrape.")
                    break
                
                urls = self._scrape_urls(page)
                song_details.extend(self._scrape_page_details(urls))
                
                page += 1
                pages_scraped += 1
        except:
            self.logger.info("End of song pages reached.")

        end_time = time.time()
        elapsed_time = int(end_time - start_time)
        self._print_and_log_info(f"Scraping completed in {elapsed_time}s.")
        self._print_and_log_info(f"{str(len(song_details))} songs extracted.")

        self.outputer.output(song_details)

    def scrape_url(self, url: str) -> None:
        """
        Scrape a single song from the specified Ultimate Guitar URL.
        
        Args:
            url: The URL of the song tab to scrape.
        """
        self._print_and_log_info(f"Scraping song at URL [{url}].")
        song_details = [self._scrape_song_details(url)]
        self._print_and_log_info("Scraping completed.")

        self.outputer.output(song_details)

    def clear_cache(self) -> None:
        """
        Clear the song cache to force re-scraping of all songs.
        """
        self.cacher.clear_cache()

    def _scrape_urls(self, page: int) -> List[str]:
        explorer_url = self._build_explorer_page_url(page)
        explorer_data = self._request_url_data_json(explorer_url)['data']['tabs']

        tab_urls = [explorer_datum['tab_url'] for explorer_datum in explorer_data]
        return tab_urls

    def _scrape_page_details(self, urls: List[str]) -> List[Dict[str, str]]:
        cached_songs = self.cacher.get_cached_songs()

        page_details = []
        for url in urls:
            if url in cached_songs:
                self.logger.info(f"Using cached values for song details with URL [{url}].")
                page_details.append(cached_songs.get(url))
            else:
                song_details = self._scrape_song_details(url)
                page_details.append(song_details)
                self.logger.info(f"Song details obtained for URL [{url}].")

                # Delaying to be respectful to website resources
                time.sleep(random.uniform(1, 3))

        return page_details

    def _scrape_song_details(self, url: str) -> Dict[str, str]:
        song_data = self._request_url_data_json(url)
        song_tab_data = song_data['tab']
        song_view_data = song_data['tab_view']

        song_details_map = {
            'ID': self._get_nested_value(url, song_tab_data, 'id'),
            'SONG_ID': self._get_nested_value(url, song_tab_data, 'song_id'),
            'ARTIST_ID': self._get_nested_value(url, song_tab_data, 'artist_id'),
            'TABS': self._get_nested_value(url, song_view_data, 'wiki_tab', 'content').replace('[tab]', '').replace('[/tab]', ''),
            'SONG_NAME': self._get_nested_value(url, song_tab_data, 'song_name'),
            'ARTIST_NAME': self._get_nested_value(url, song_tab_data, 'artist_name'),
            'URL': url,
            'DIFFICULTY': self._get_nested_value(url, song_tab_data, 'difficulty'),
            'TUNING': self._get_nested_value(url, song_view_data, 'meta', 'tuning', 'value'),
            'KEY': self._get_nested_value(url, song_view_data, 'meta', 'tonality'),
            'RATING': "{:.2f}".format(float(self._get_nested_value(url, song_tab_data, 'rating'))),
            'VOTES': self._get_nested_value(url, song_tab_data, 'votes'),
            'VIEWS': self._get_nested_value(url, song_view_data, 'stats', 'view_total'),
            'FAVORITES': self._get_nested_value(url, song_view_data, 'stats', 'favorites_count')
        }

        self.cacher.cache_song(url, song_details_map)

        return song_details_map
    
    def _normalize_limit(self, limit: int) -> int:
        limit = max(0, limit)
        if limit == 0:
            self.logger.warn("Limit set to 0, no songs will be scraped. Closing scraper.")
            sys.exit(1)

        self._print_and_log_info(f"Will scrape a maximum of {limit} pages.")
        return limit
    
    def _normalize_offset(self, offset: int) -> int:
        offset = max(0, offset)
        if offset > 0:
            self._print_and_log_info(f"Starting from page {offset + 1}.")

        return offset

    def _build_explorer_page_url(self, page: int) -> str:
        return f'https://www.ultimate-guitar.com/explore?type[]=Tabs&page={page}' if page != 1 else 'https://www.ultimate-guitar.com/explore?type[]=Tabs'
    
    def _request_url_data_json(self, url: str) -> NestedDict:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except:
            self.logger.error(f"Bad URL [{url}].")
            print(f"Bad URL [{url}].")
            sys.exit(1)

        content = BeautifulSoup(response.content, 'html.parser')
        clean_content = self._clean_content(content)
        json_content = json.loads(clean_content)['store']['page']['data']

        return json_content

    def _clean_content(self, content: BeautifulSoup) -> str:
        div_content = str(content.find('html').find('body').find('div', class_='js-store'))
        # Removes starting and ending HTML tags to convert to JSON
        div_content = div_content[36:-8]
        # Cleans encoded characters and deactivates new line characters
        div_content = div_content.replace('&quot;', '\"').replace('\\r\\n', '\\\\n')

        return div_content

    def _get_nested_value(self, song_url: str, json: NestedDict, *keys: str) -> str:
        try:
            for key in keys:
                json = json[key]
            return json
        except:
            self.logger.warn(f"Failed to find [{key}] value for song at URL [{song_url}].")
            return ''

    def _print_and_log_info(self, msg):
        self.logger.info(msg)
        print(msg)
