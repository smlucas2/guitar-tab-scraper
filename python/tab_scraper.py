# -*- coding: utf-8 -*-
"""
Tab Scraper

This utility will scrapethe "Ultimate Guitar" website and obtain the tabulations.
"""

import requests
from bs4 import BeautifulSoup

class Scraper:
    all_song_details = []
    
    def scrape_pages(self, pages):
        for page in range(0, pages):
            self._scrape_tab_urls(page + 1)
        
    def _scrape_tab_urls(self, page):
        response = self._request_tab_explorer_page(page)
            
        song_urls = self._parse_tab_urls(response)
        for song_url in song_urls:
            self._scrape_song_details(song_url)
        
    def _scrape_song_details(self, song_url):
        song_details = [song_url]
        
        song_content = self._parse_song_content(song_url)
        tab_complete = self._parse_tab_sections(song_content)
        song_details.append(tab_complete)
        
        self.all_song_details.append(song_details)
        
    def _request_tab_explorer_page(self, page):
        if page == 1:
            return requests.get('https://www.ultimate-guitar.com/explore?type[]=Tabs')
        else:
            return requests.get('https://www.ultimate-guitar.com/explore?type[]=Tabs&page=' + str(page))
        
    def _parse_tab_urls(self, response):
        content = BeautifulSoup(response.content, 'html.parser')
        div_content = content.find('html').find('body').find('div', class_='js-store')
        div_content_str = str(div_content)
        song_urls = div_content_str.split('tab_url&quot;:&quot;')
            
        return self._clean_tab_urls(song_urls)
    
    def _clean_tab_urls(self, song_urls):
        cleaned_song_urls = []
        #first element is the div tag, will skip that
        for song_url in song_urls[1:]:
            cleaned_song_url = song_url.split('&')[0]
            cleaned_song_urls.append(cleaned_song_url)
            
        return cleaned_song_urls
    
    def _parse_song_content(self, song_url):
        response = requests.get(song_url)
        content = BeautifulSoup(response.content, 'html.parser')
        div_content = content.find('html').find('body').find('div', class_='js-store')
        return str(div_content)
    
    def _parse_tab_sections(self, song_content):
        tab_sections_dirty = song_content.split('[/tab]')
        tab_complete = []
        #we don't want the last item in the list, its just html content
        for index, tab_section_dirty in enumerate(tab_sections_dirty[:-1]):
            tab_strings = tab_section_dirty.split('[tab]')[1]
            tab_strings = tab_strings.split('\\r\\n')
            
            tab_section_cleaned = ''
            for tab_string in tab_strings:
                #removes special characters
                tab_string = tab_string.encode().decode('unicode_escape')
                tab_section_cleaned = tab_section_cleaned + tab_string + '\n'
            #removes final trailing newline char
            tab_section_cleaned = tab_section_cleaned[:-1]
            tab_complete.append(tab_section_cleaned)
            
        return tab_complete
                
scraper = Scraper()
scraper.scrape_pages(1)