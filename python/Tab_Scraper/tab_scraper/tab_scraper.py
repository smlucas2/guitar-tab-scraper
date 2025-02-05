# -*- coding: utf-8 -*-
"""
Tab Scraper

This utility will scrapethe "Ultimate Guitar" website and obtain the tabulations.
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

# TODO: fix existing tests
# TODO: test logging
# TODO: add limit/offset to song scraping to do it in batches if wanted
# TODO: test limit/offset
# TODO: test command line usage! might need some kind of limit so it doesnt take all day
# TODO: reorder imports and methods
# TODO: add docs to all public methods
# TODO: update README
# TODO: update pyproject
class UltimateGuitarScraper:
    
    def __init__(
            self, 
            out_dir: Optional[str] = None, 
            cache_dir: Optional[str] = None, 
            log_dir: Optional[str] = None
        ) -> None:
        
        self.outputer = SongDetailsOutputer(out_dir)
        self.cacher = SongCacher(cache_dir)
        self.logger = SongLogger(log_dir, __name__)
        
    def scrape_songs(self) -> None:
        self._print_and_log_info("Beginning scraping of Ultimate Guitar for tabs.")
        start_time = time.time()
        
        song_details = []
        try:
            page = 1
            while True:
                urls = self._scrape_urls(page)
                song_details.extend(self._scrape_page_details(urls))
                page += 1
        except:
            self.logger.info("End of song pages reached.")
                
        end_time = time.time()
        elapsed_time = int(end_time - start_time)
        self._print_and_log_info(f"Scraping completed in {elapsed_time}s.")
        self._print_and_log_info(f"{str(len(song_details))} songs extracted.")
        
        self.outputer.output(song_details)
    
    def scrape_url(self, url: str) -> None:
        self._print_and_log_info("Scraping song at URL [{url}].")
        song_details = [self._scrape_song_details(url)]
        self._print_and_log_info("Scraping completed.")
        
        self.outputer.output(song_details)
    
    def clear_cache(self) -> None:
        self.cacher.clear_cache()
        
    def _scrape_urls(self, page: int) -> None:
        explorer_url = self._build_explorer_page_url(page)
        explorer_data = self._request_url_data_json(explorer_url)['data']['tabs']
        
        tab_urls = []
        for explorer_datum in explorer_data:
            tab_urls.append(explorer_datum['tab_url'])
            
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
        
        song_details_map = {}
        song_details_map['ID'] = self._get_nested_value(url, song_tab_data, 'id')
        song_details_map['SONG_ID'] = self._get_nested_value(url, song_tab_data, 'song_id')
        song_details_map['ARTIST_ID'] = self._get_nested_value(url, song_tab_data, 'artist_id')
        tab_data = self._get_nested_value(url, song_view_data, 'wiki_tab', 'content')
        song_details_map['TABS'] = tab_data.replace('[tab]', '').replace('[/tab]', '')
        song_details_map['SONG_NAME'] = self._get_nested_value(url, song_tab_data, 'song_name')
        song_details_map['ARTIST_NAME'] = self._get_nested_value(url, song_tab_data, 'artist_name')
        song_details_map['URL'] = url
        song_details_map['DIFFICULTY'] = self._get_nested_value(url, song_tab_data, 'difficulty')
        song_details_map['TUNING'] = self._get_nested_value(url, song_view_data, 'meta', 'tuning', 'value')
        song_details_map['KEY'] = self._get_nested_value(url, song_view_data, 'meta', 'tonality')
        rating_data = self._get_nested_value(url, song_tab_data, 'rating')
        song_details_map['RATING'] = "{:.2f}".format(float(rating_data))
        song_details_map['VOTES'] = self._get_nested_value(url, song_tab_data, 'votes')
        song_details_map['VIEWS'] = self._get_nested_value(url, song_view_data, 'stats', 'view_total')
        song_details_map['FAVORITES'] = self._get_nested_value(url, song_view_data, 'stats', 'favorites_count')
        
        self.cacher.cache_song(url, song_details_map)
        
        return song_details_map
        
    def _build_explorer_page_url(self, page: int) -> str:
        if page == 1:
            return 'https://www.ultimate-guitar.com/explore?type[]=Tabs'
        return 'https://www.ultimate-guitar.com/explore?type[]=Tabs&page=' + str(page)
    
    def _request_url_data_json(self, url: str) -> NestedDict:
        try:
            response = requests.get(url)
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
        #Removes starting and ending HTML tags to convert to JSON
        div_content = div_content[36:-8]
        #Cleans encoded characters and deactivates new line characters
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