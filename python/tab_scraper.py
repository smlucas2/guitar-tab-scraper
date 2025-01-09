# -*- coding: utf-8 -*-
"""
Tab Scraper

This utility will scrap the "Ultimate Guitar" website and obtain the tabulations.
"""

import requests
from bs4 import BeautifulSoup

class Scraper:
    def scrape_pages(self, pages):
        for page in range(0, pages):
            self.scrape_for_song_urls(page + 1)
        
    def scrape_for_song_urls(self, page):
        if page == 1:
            response = requests.get('https://www.ultimate-guitar.com/explore?type[]=Tabs')
        else:
            response = requests.get('https://www.ultimate-guitar.com/explore?page=' + str(page) + '&type[]=Tabs')
            
        content = BeautifulSoup(response.content, 'html.parser')
        div_content = content.find('html').find('body').find('div', class_='js-store')
        div_content_str = str(div_content)
        
        song_urls = div_content_str.split('tab_url&quot;:&quot;')
        #first element is the div tag, will skip that
        for song_url in song_urls[1:]:
            cleaned_song_url = song_url.split('&')[0]
            self.scrape_song(cleaned_song_url)
        
    def scrape_song(self, song_url):
        print(song_url)
        response = requests.get(song_url)
        content = BeautifulSoup(response.content, 'html.parser')
        div_content = content.find('html').find('body').find('div', class_='js-store')
        div_content_str = str(div_content)
        
        tab_sections_raw = div_content_str.split('[/tab]')
        for index, tab_section in enumerate(tab_sections_raw):
            #we don't care want the last item in the list, its just html content
            if index == len(tab_sections_raw) - 1:
                break
            tab_lines = tab_section.split('[tab]')[1]
            tab_lines_cleaned = tab_lines.split('\\r\\n')
            for tab_line in tab_lines_cleaned:
                #removes special characters
                tab_line = tab_line.encode().decode('unicode_escape')
                print(tab_line)
            print('\n')
        print('\n')
        
scraper = Scraper()
scraper.scrape_pages(1)