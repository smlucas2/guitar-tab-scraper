# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:55:01 2025

@author: Seanly Bear
"""

from tab_scraper.tab_scraper import UltimateGuitarScraper
import unittest
         
class TestScraper(unittest.TestCase):
    scraper = UltimateGuitarScraper()
    
    # def test_scrape_song(self):
    #     song_details = self.scraper.scrape_tab('https://tabs.ultimate-guitar.com/tab/metallica/nothing-else-matters-tabs-8519', None)
    
    #     self.assertTrue(len(song_details) == 1)    
    
    def test_scrape_single_page(self):
        song_details = []
        song_details = self.scraper.scrape_pages(1, None)
        
        self.assertTrue(len(song_details) == 31)
        
    # def test_scrape_multiple_pages(self):
    #     song_details = []
    #     song_details = self.scraper.scrape_pages(3, None)
        
    #     self.assertTrue(len(song_details) == 107)
        
    # TODO: change tests to check output.csv (and delete)
    # TODO: test cache and clearing cache
    # TODO: test CSV file exists
    # TODO: Test scraping a single song URL
    # TODO: test using command line flags
    # TODO: Test failing when misusing command line flag
    # TODO: Test using wrong data types when using flags

if __name__ == '__main__':
    unittest.main()