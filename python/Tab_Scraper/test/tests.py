# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:55:01 2025

@author: Sean
"""

from pathlib import Path
import unittest
from unittest.mock import patch

import logging
import requests
import requests_mock
import shutil
import csv

from util.mock_site_builder import create_mock_site
from tab_scraper.tab_scraper import UltimateGuitarScraper

# TODO: test default paths for output/cache/logs
# TODO: test custom logs path works
# TODO: Test bad custom log path
class TestScraper(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # intercepting requests to Ultimate Guitar to use mock site for testing
        cls.mock_adapter = requests_mock.Adapter()
        cls.session = requests.Session()
        cls.session.mount('https://', cls.mock_adapter)
        
        create_mock_site(cls.mock_adapter)
        
    def tearDown(self):
        logging.shutdown()
        self._delete_directory('output')
        self._delete_directory('cache')
        self._delete_directory('testcache')
        self._delete_directory('log')
        
    def test_scrape_songs(self):
        scraper = UltimateGuitarScraper()
        with patch('requests.get', self.session.get):
            scraper.scrape_songs()
                    
        row_to_data = {1: ['0001', '125000'], 4: ['0004', '8000']}
        self._validate_output_rows(row_to_data)
    
    def test_scrape_song(self):
        scraper = UltimateGuitarScraper()
        with patch('requests.get', self.session.get):
            scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/band1/song1')
            
        row_to_data = {1: ['0001', '125000']}
        self._validate_output_rows(row_to_data)

    def test_scrape_song_bad_url(self):
        scraper = UltimateGuitarScraper()
        with self.assertRaises(SystemExit) as cm:
            with patch('requests.get', self.session.get):
                scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/wrong/wrong')
            
        self.assertEqual(cm.exception.code, 1)
        
    def test_custom_output_path(self):
        out_path = './testoutput'
        scraper = UltimateGuitarScraper(out_dir=out_path)
        with patch('requests.get', self.session.get):
            scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/band1/song1')
            
        self._check_and_delete_file(out_path + '/songdetails.csv')

    # TODO: Fix, no longer throws error, goes to default
    # def test_bad_custom_output_path(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         out_path = './parent1/parent2/parent3'
    #         UltimateGuitarScraper(out_dir=out_path)
            
    #     self.assertEqual(cm.exception.code, 1)

    # TODO: Fix, no longer throws error, goes to default
    # def test_bad_custom_output_chars(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         out_path = 'sadsad??['
    #         UltimateGuitarScraper(out_dir=out_path)
            
    #     self.assertEqual(cm.exception.code, 1)
        
    def test_custom_cache_path(self):
        cache_path = './testcache'
        scraper = UltimateGuitarScraper(cache_dir=cache_path)
        with patch('requests.get', self.session.get):
            scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/band1/song1')
            
        self._check_and_delete_file(cache_path + '/songcache.db')

    # TODO: Fix, no longer throws error, goes to default
    # def test_bad_custom_cache_path(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         cache_path = './parent1/parent2/parent3'
    #         UltimateGuitarScraper(cache_dir=cache_path)
            
    #     self.assertEqual(cm.exception.code, 1)

    # TODO: Fix, no longer throws error, goes to default
    # def test_bad_custom_cache_chars(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         cache_path = '<>asdf44'
    #         UltimateGuitarScraper(cache_dir=cache_path)
            
    #     self.assertEqual(cm.exception.code, 1)
    
    # def test_custom_logs_path(self):
    #     logs_path = './testoutput'
    #     scraper = UltimateGuitarScraper(logs_path=logs_path)
    #     with patch('requests.get', self.session.get):
    #         scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/band1/song1')
            
    #     # TODO file name
    #     self._check_and_delete_file(logs_path + '/log')
    
    # def test_bad_custom_logs(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         logs_path = './parent1/parent2/parent3'
    #         UltimateGuitarScraper(logs_path=logs_path)
            
    #     self.assertEqual(cm.exception.code, 1)
    
    # def test_bad_custom_logs_chars(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         logs_path = 'sadsad??['
    #         UltimateGuitarScraper(logs_path=logs_path)
            
    #     self.assertEqual(cm.exception.code, 1)
        
    def test_clear_cache(self):
        scraper = UltimateGuitarScraper()
        with patch('requests.get', self.session.get):
            scraper.scrape_url('https://tabs.ultimate-guitar.com/tab/band1/song1')
            
        cached_songs = scraper.cacher.get_cached_songs()
        self.assertEqual(len(cached_songs), 1)
        scraper.clear_cache()
        cached_songs = scraper.cacher.get_cached_songs()
        self.assertEqual(len(cached_songs), 0)
        
    def _validate_output_rows(self, row_to_data):
        with open("./output/songdetails.csv", mode='r') as file:
            csv_reader = csv.reader(file)
            for index, row in enumerate(csv_reader):
                if index in row_to_data:
                    row_data = row_to_data[index]
                    self.assertEqual(row[0], row_data[0], f"Output row start does not match [{row_data[0]}]!")
                    self.assertEqual(row[-1], row_data[1], f"Output row end does not match [{row_data[1]}]!")

    def _delete_directory(self, directory: str) -> str:
        current_script_dir = Path(__file__).resolve().parent
        target_directory = current_script_dir.parent
        default_dir = target_directory / directory
        
        if default_dir.exists():
            shutil.rmtree(default_dir)
    
    def _check_and_delete_file(self, path):
        file_path = Path(path)
        self.assertTrue(file_path.exists(), f"File at [{path}] does not exist!")
        parent_dir = file_path.parent

        if parent_dir.exists() and parent_dir.is_dir():
            shutil.rmtree(parent_dir)

if __name__ == '__main__':
    unittest.main()