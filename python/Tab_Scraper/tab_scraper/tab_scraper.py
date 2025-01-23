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
import csv
import shelve
from pathlib import Path
from bs4 import BeautifulSoup

# TODO: add ouput folder and cache files to .gitignore, also remove them from git
# TODO: add logging
class UltimateGuitarScraper:
    CACHE = 'songcache.db'
    
    def scrape_pages(self, pages, output_path):
        start_time = time.time()
        print("Beginning scraping of Ultimate Guitar for tabs.")
        
        all_song_details = []
        for page in range(1, pages + 1):
            print("Scraping page " + str(page) + "...")
            
            tab_urls = self._scrape_tab_urls(page)
            all_song_details.append(self._scrape_page_details(tab_urls))
                
        end_time = time.time()
        elapsed_time = int(end_time - start_time)
        print(f"Scraping completed in {elapsed_time}s.")
        print(f"Extracted details of {str(len(all_song_details))} songs.")
        
        self._output_to_csv(all_song_details, output_path)
    
    def scrape_tab(self, tab_url, output_path):
        print("Scraping song from Ultimate Guitar at URL [" + tab_url + "].")
        all_song_details = [self._scrape_song_details(tab_url)]
        print("Scraping completed.")
        
        self._output_to_csv(all_song_details, output_path)
    
    def clear_cache(self):
        with shelve.open(self.CACHE) as db:
            db.clear()
    
    def _output_to_csv(self, all_song_details, output_path):
        output_path = self._retrieve_output_path(output_path)
        with open(output_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=all_song_details[0][0].keys())
            writer.writeheader()
            for page_details in all_song_details:
                for song_details in page_details:
                    writer.writerow(song_details)
                
    def _retrieve_output_path(self, output_path):
        if output_path is None:
            current_file = Path(__file__)
            parent_directory = current_file.parent.parent
            output_path = parent_directory / "output/output.csv"
        return output_path
        
    def _scrape_tab_urls(self, page):
        page_url = self._build_explorer_page_url(page)
        explorer_dict = self._request_site_data_json(page_url)['data']['tabs']
        
        tab_urls = []
        for explorer_data in explorer_dict:
            tab_urls.append(explorer_data['tab_url'])
            
        return tab_urls
    
    def _scrape_page_details(self, tab_urls):
        page_details = []
        with shelve.open(self.CACHE) as cached_songs:
            for tab_url in tab_urls:
                if tab_url in cached_songs:
                    print("Using cached values for song details with URL [" + tab_url + "].")
                    page_details.append(cached_songs.get(tab_url))
                else:
                    song_details = self._scrape_song_details(tab_url)
                    page_details.append(song_details)
                    print("Song details obtained for URL [" + tab_url + "].")
                
                    #delaying to be respectful to website resources
                    time.sleep(random.uniform(1, 3))
            
        return page_details
        
    def _scrape_song_details(self, song_url):
        song_data = self._request_site_data_json(song_url)
        song_tab_data = song_data['tab']
        song_view_data = song_data['tab_view']
        
        song_details_map = {'ID': self._get_data(song_tab_data, song_url, 'id')}
        song_details_map['SONG_ID'] = self._get_data(song_tab_data, song_url, 'song_id')
        song_details_map['ARTIST_ID'] = self._get_data(song_tab_data, song_url, 'artist_id')
        tab_data = self._get_data(song_view_data, song_url, 'wiki_tab', 'content')
        song_details_map['TABS'] = tab_data.replace('[tab]', '').replace('[/tab]', '')
        song_details_map['SONG_NAME'] = self._get_data(song_tab_data, song_url, 'song_name')
        song_details_map['ARTIST_NAME'] = self._get_data(song_tab_data, song_url, 'artist_name')
        song_details_map['URL'] = song_url
        song_details_map['DIFFICULTY'] = self._get_data(song_tab_data, song_url, 'difficulty')
        song_details_map['TUNING'] = self._get_data(song_view_data, song_url, 'meta', 'tuning', 'value')
        song_details_map['KEY'] = self._get_data(song_view_data, song_url, 'meta', 'tonality')
        rating_data = self._get_data(song_tab_data, song_url, 'rating')
        song_details_map['RATING'] = "{:.2f}".format(float(rating_data))
        song_details_map['VOTES'] = self._get_data(song_tab_data, song_url, 'votes')
        song_details_map['VIEWS'] = self._get_data(song_view_data, song_url, 'stats', 'view_total')
        song_details_map['FAVORITES'] = self._get_data(song_view_data, song_url, 'stats', 'favorites_count')
        
        with shelve.open(self.CACHE) as db:
            db[song_url] = song_details_map
        
        return song_details_map
        
    def _build_explorer_page_url(self, page):
        if page == 1:
            return 'https://www.ultimate-guitar.com/explore?type[]=Tabs'
        return 'https://www.ultimate-guitar.com/explore?type[]=Tabs&page=' + str(page)
    
    def _request_site_data_json(self, song_url):
        response = requests.get(song_url)
        content = BeautifulSoup(response.content, 'html.parser')
        clean_content = self._clean_content(content)
        
        return json.loads(clean_content)['store']['page']['data']
    
    def _clean_content(self, content):
        div_content = str(content.find('html').find('body').find('div', class_='js-store'))
        #Removes starting and ending HTML tags to convert to JSON
        div_content = div_content[36:-8]
        #Cleans encoded characters and deactivates new line characters
        div_content = div_content.replace('&quot;', '\"').replace('\\r\\n', '\\\\n')
        
        return div_content
    
    def _get_data(self, json, song_url, *keys):
        try:
            for key in keys:
                json = json[key]
            return json
        except:
            print("Failed to find [" + key + "] value for song at URL [" + song_url + "].")
            return ''
    
def main():
    parser = argparse.ArgumentParser(description="Web scraper for guitar tabs")
    parser.add_argument("-p", "--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("-t", "--tab", type=str, help="Tab URL to scrape")
    parser.add_argument("-o", "--out", type=str, default=None, help="Output path. Defalts to parent directory output folder.")
    parser.add_argument("-c", "--clear", action='store_true', help="Clears the song cache.")
    args = parser.parse_args()
    
    scraper = UltimateGuitarScraper()
    if args.clear:
        scraper.clear_cache()
    
    if args.tab:
        scraper.scrape_tab(args.tab, args.out)
    else:
        scraper.scrape_pages(args.pages, args.out)

if __name__ == '__main__':
    main()