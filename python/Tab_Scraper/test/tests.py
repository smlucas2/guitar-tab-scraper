# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:55:01 2025

@author: Sean
"""

from pathlib import Path
import unittest
from unittest.mock import patch

import requests
import requests_mock
import shutil
import csv

from util.mock_site_builder import create_mock_site
from tab_scraper.tab_scraper import UltimateGuitarScraper

# TODO: for each test, run as script with appropriate flag and validate output
# TODO: test caching works
# TODO: test clearing cache with flag
# TODO: test custom output path with flag
# TODO: test custom cache path with flag
# TODO: test custom logs path with flag
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
            
        row_to_data = {1: ['0001', '125000']}
        self._validate_output_rows(row_to_data)
        self._clean_up()
    
    def test_scrape_songs(self):
        scraper = UltimateGuitarScraper()
        with patch('requests.get', self.session.get):
            scraper.scrape_songs()
                    
        row_to_data = {1: ['0001', '125000'], 4: ['0004', '8000']}
        self._validate_output_rows(row_to_data)
        self._clean_up()
        
    def _validate_output_rows(self, row_to_data):
        with open("../output/songdetails.csv", mode='r') as file:
            csv_reader = csv.reader(file)
            for index, row in enumerate(csv_reader):
                if index in row_to_data:
                    row_data = row_to_data[index]
                    self.assertEqual(row[0], row_data[0])
                    self.assertEqual(row[-1], row_data[1])
        
    def _clean_up(self):
        self._delete_directory('output')
        self._delete_directory('songcache')

    def _delete_directory(self, directory: str) -> str:
        current_script_dir = Path(__file__).resolve().parent
        target_directory = current_script_dir.parent
        default_dir = target_directory / directory
        
        shutil.rmtree(default_dir)

if __name__ == '__main__':
    unittest.main()