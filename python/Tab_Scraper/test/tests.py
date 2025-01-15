# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:55:01 2025

@author: Seanly Bear
"""

from tab_scraper.tab_scraper import UltimateGuitarScraper
import unittest
         
class TestScraper(unittest.TestCase):
    scraper = UltimateGuitarScraper()
    
    def test_scrape_single_page(self):
        song_details = []
        song_details = self.scraper.scrape_pages(1)
        
        self.assertTrue(len(song_details) == 31)
        
    def test_scrape_multiple_pages(self):
        song_details = []
        song_details = self.scraper.scrape_pages(3)
        
        self.assertTrue(len(song_details) == 107)

if __name__ == '__main__':
    unittest.main()