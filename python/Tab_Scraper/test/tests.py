# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:55:01 2025

@author: Sean
"""

import unittest
from unittest.mock import patch

import requests
import requests_mock

from util.mock_site_builder import create_mock_site
from tab_scraper.tab_scraper import UltimateGuitarScraper

# TODO: for each test, validate output, delete output, delete cache
# TODO: test cache and clearing cache
# TODO: test custom output path
# TODO: test CSV file exists
# TODO: test using command line flags
# TODO: Test failing when misusing command line flag
# TODO: Test using wrong data types when using flags
class TestScraper(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # intercepting requests to Ultimate Guitar to use mock site for testing
        cls.mock_adapter = requests_mock.Adapter()
        cls.session = requests.Session()
        cls.session.mount('https://', cls.mock_adapter)
        
        create_mock_site(cls.mock_adapter)
    
    def test_scrape_song(self):
        scraper = UltimateGuitarScraper()
        with patch('requests.get', self.session.get):
            scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/band1/song1')
    
    def test_scrape_songs(self):
        scraper = UltimateGuitarScraper()
        with patch('requests.get', self.session.get):
            scraper.scrape_songs()

if __name__ == '__main__':
    unittest.main()