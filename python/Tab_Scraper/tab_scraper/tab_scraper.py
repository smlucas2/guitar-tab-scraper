# -*- coding: utf-8 -*-
"""
Tab Scraper

This utility will scrapethe "Ultimate Guitar" website and obtain the tabulations.
"""

import json
import random
import time
from typing import Optional, List, Dict, Union

import requests
from bs4 import BeautifulSoup

from tab_scraper.util import SongCacher, SongDetailsOutputer

NestedDict = Dict[str, Union[str, "NestedDict"]]

# TODO: add logger class with logging
# TODO: update README
# TODO: update pyproject
# TODO: update tests
# TODO: add docs to all public methods
class UltimateGuitarScraper:
    
    def __init__(
            self, 
            out_path: Optional[str] = None, 
            cache_path: Optional[str] = None, 
            log_path: Optional[str] = None
        ) -> None:
        
        self.song_cache = SongCacher(cache_path)
        self.outputer = SongDetailsOutputer(out_path)
        # TODO: create logger
        
    def scrape_songs(self) -> None:
        start_time = time.time()
        print("Beginning scraping of Ultimate Guitar for tabs.")
        
        song_details = []
        
        try:
            page = 1
            while True:
                urls = self._scrape_urls(page)
                song_details.extend(self._scrape_page_details(urls))
                page += 1
        except:
            print("End of song list reached.")
                
        end_time = time.time()
        elapsed_time = int(end_time - start_time)
        print(f"Scraping completed in {elapsed_time}s.")
        print(f"Extracted details of {str(len(song_details))} songs.")
        
        self.outputer.output(song_details)
    
    def scrape_url(self, url: str) -> None:
        print("Scraping song from Ultimate Guitar at URL [" + url + "].")
        song_details = [self._scrape_song_details(url)]
        print("Scraping completed.")
        
        self.outputer.output(song_details)
    
    def clear_cache(self) -> None:
        self.song_cache.clear_cache()
        
    def _scrape_urls(self, page: int) -> None:
        page_url = self._build_explorer_page_url(page)
        explorer_dict = self._request_site_data_json(page_url)['data']['tabs']
        
        tab_urls = []
        for explorer_data in explorer_dict:
            tab_urls.append(explorer_data['tab_url'])
            
        return tab_urls
    
    def _scrape_page_details(self, urls: List[str]) -> List[Dict[str, str]]:
        cached_songs = self.song_cache.get_cached_songs()
        
        page_details = []
        for url in urls:
            if url in cached_songs:
                print("Using cached values for song details with URL [" + url + "].")
                page_details.append(cached_songs.get(url))
            else:
                song_details = self._scrape_song_details(url)
                page_details.append(song_details)
                print("Song details obtained for URL [" + url + "].")
            
                # Delaying to be respectful to website resources
                time.sleep(random.uniform(1, 3))
            
        return page_details
        
    def _scrape_song_details(self, url: str) -> Dict[str, str]:
        song_data = self._request_site_data_json(url)
        song_tab_data = song_data['tab']
        song_view_data = song_data['tab_view']
        
        song_details_map = {'ID': self._get_value(song_tab_data, url, 'id')}
        song_details_map['SONG_ID'] = self._get_value(song_tab_data, url, 'song_id')
        song_details_map['ARTIST_ID'] = self._get_value(song_tab_data, url, 'artist_id')
        tab_data = self._get_value(song_view_data, url, 'wiki_tab', 'content')
        song_details_map['TABS'] = tab_data.replace('[tab]', '').replace('[/tab]', '')
        song_details_map['SONG_NAME'] = self._get_value(song_tab_data, url, 'song_name')
        song_details_map['ARTIST_NAME'] = self._get_value(song_tab_data, url, 'artist_name')
        song_details_map['URL'] = url
        song_details_map['DIFFICULTY'] = self._get_value(song_tab_data, url, 'difficulty')
        song_details_map['TUNING'] = self._get_value(song_view_data, url, 'meta', 'tuning', 'value')
        song_details_map['KEY'] = self._get_value(song_view_data, url, 'meta', 'tonality')
        rating_data = self._get_value(song_tab_data, url, 'rating')
        song_details_map['RATING'] = "{:.2f}".format(float(rating_data))
        song_details_map['VOTES'] = self._get_value(song_tab_data, url, 'votes')
        song_details_map['VIEWS'] = self._get_value(song_view_data, url, 'stats', 'view_total')
        song_details_map['FAVORITES'] = self._get_value(song_view_data, url, 'stats', 'favorites_count')
        
        self.song_cache.cache_song(url, song_details_map)
        
        return song_details_map
        
    def _build_explorer_page_url(self, page: int) -> str:
        if page == 1:
            return 'https://www.ultimate-guitar.com/explore?type[]=Tabs'
        return 'https://www.ultimate-guitar.com/explore?type[]=Tabs&page=' + str(page)
    
    def _request_site_data_json(self, song_url: str) -> NestedDict:
        response = requests.get(song_url)
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
    
    def _get_value(self, json: NestedDict, song_url: str, *keys: str) -> str:
        try:
            for key in keys:
                json = json[key]
            return json
        except:
            print("Failed to find [" + key + "] value for song at URL [" + song_url + "].")
            return ''