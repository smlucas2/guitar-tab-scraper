# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:55:01 2025

@author: Seanly Bear
"""

from tab_scraper.tab_scraper import UltimateGuitarScraper
import unittest
         
class TestScraper(unittest.TestCase):
    scraper = UltimateGuitarScraper()
    
    def test_scrape_song(self):
        # TODO: use requests_mock library to make a mock site to scrape so this break if url is changed
        self.scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/metallica/nothing-else-matters-tabs-8519')
        # TODO: validate output
        # TODO: delete output
    
    def test_scrape_songs(self):
        # TODO: use requests_mock library to make a mock site to scrape so this doesnt take forever
        self.scraper.scrape_songs()
        # TODO: validate output
        # TODO: delete output
        
    # TODO: test cache and clearing cache
    # TODO: test custom output path
    # TODO: test CSV file exists
    # TODO: test using command line flags
    # TODO: Test failing when misusing command line flag
    # TODO: Test using wrong data types when using flags

if __name__ == '__main__':
    unittest.main()