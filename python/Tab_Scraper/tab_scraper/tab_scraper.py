# -*- coding: utf-8 -*-
"""
Tab Scraper

This utility will scrapethe "Ultimate Guitar" website and obtain the tabulations.
"""

import requests
import argparse
import time
import random
import json
from bs4 import BeautifulSoup

class UltimateGuitarScraper:
    all_song_details = []
    
    def scrape_pages(self, pages):
        print("Beginning scraping of Ultimate Guitar for tabs.")
        start_time = time.time()
        for page in range(1, pages + 1):
            print("Scraping page " + str(page) + "...")
            self._scrape_tab_urls(page)
        end_time = time.time()
        
        elapsed_time = int(end_time - start_time)
        print(f"Scraping completed in {elapsed_time}s.")
        print(f"Extracted details of {str(len(self.all_song_details))} songs.")
        return self.all_song_details
    
    def scrape_song(self, song_url):
        print("Scraping song from Ultimate Guitar at URL [" + song_url + "].")
        self._scrape_song_details(song_url)
        print("Scraping completed.")
        return self.all_song_details
        
    def _scrape_tab_urls(self, page):
        response = self._request_tab_explorer_page(page)
            
        song_urls = self._parse_tab_urls(response)
        for song_url in song_urls:
            self._scrape_song_details(song_url)
            #delaying to be respectful to website resources
            time.sleep(random.uniform(1, 3))
        
    def _scrape_song_details(self, song_url):
        song_data = self._request_song_data_json(song_url)
        song_tab_data = song_data['tab']
        song_view_data = song_data['tab_view']
        
        song_details_map = {'URL': song_url}
        song_details_map['ID'] = song_tab_data['id']
        song_details_map['SONG_ID'] = song_tab_data['song_id']
        song_details_map['ARTIST_ID'] = song_tab_data['artist_id']
        song_details_map['BAND_NAME'] = song_tab_data['artist_name']
        song_details_map['SONG_NAME'] = song_tab_data['song_name']
        song_details_map['DIFFICULTY'] = song_tab_data['difficulty']
        song_details_map['TUNING'] = song_view_data['meta']['tuning']['value']
        song_details_map['KEY'] = song_view_data['meta']['tonality']
        song_details_map['RATING'] = "{:.2f}".format(float(song_tab_data['rating']))
        song_details_map['VOTES'] = song_tab_data['votes']
        song_details_map['VIEWS'] = song_view_data['stats']['view_total']
        song_details_map['FAVORITES'] = song_view_data['stats']['favorites_count']
        song_details_map['TABS'] = self._clean_tabs(song_view_data['wiki_tab']['content'])
        
        self.all_song_details.append(song_details_map)
        
    def _request_tab_explorer_page(self, page):
        if page == 1:
            return requests.get('https://www.ultimate-guitar.com/explore?type[]=Tabs')
        else:
            return requests.get('https://www.ultimate-guitar.com/explore?type[]=Tabs&page=' + str(page))
        
    def _parse_tab_urls(self, response):
        # TODO: turn this into json for cleaner use
        content = BeautifulSoup(response.content, 'html.parser')
        div_content = content.find('html').find('body').find('div', class_='js-store')
        div_content_str = str(div_content)
        song_urls = div_content_str.split('tab_url&quot;:&quot;')
            
        return self._clean_tab_urls(song_urls)
    
    def _clean_tab_urls(self, song_urls):
        # TODO: change this to utilize json, or remove if not needed
        cleaned_song_urls = []
        #first element is the div tag, will skip that
        for song_url in song_urls[1:]:
            cleaned_song_url = song_url.split('&')[0]
            cleaned_song_urls.append(cleaned_song_url)
            
        return cleaned_song_urls
    
    def _request_song_data_json(self, song_url):
        response = requests.get(song_url)
        content = BeautifulSoup(response.content, 'html.parser')
        
        #Obtaining content from necessary div and cleaning it up 
        div_content = str(content.find('html').find('body').find('div', class_='js-store'))
        div_content = div_content.replace("&quot;", "\"")
        div_content = div_content[36:-8]
        
        return json.loads(div_content)['store']['page']['data']
    
    def _clean_tabs(self, tab_content):
        tab_content = tab_content.replace('[tab]', '').replace('[/tab]', '')
            
        return tab_content
    
def main():
    parser = argparse.ArgumentParser(description="Web scraper for guitar tabs")
    parser.add_argument("-p", "--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("-s", "--song", type=str, help="Song URL to scrape")
    args = parser.parse_args()
    
    scraper = UltimateGuitarScraper()
    if args.song:
        scraper.scrape_song(args.song)
    else:
        scraper.scrape_pages(args.pages)

if __name__ == '__main__':
    main()