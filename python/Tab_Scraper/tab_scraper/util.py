# -*- coding: utf-8 -*-

import atexit
import shelve
import logging
import csv
from typing import Dict, List
from pathlib import Path

class SongFileWriter:
    _DEFAULT_DIR_NAME = None
    
    def resolve_directory_path(self, custom_dir: str) -> Path:
        if custom_dir is not None:
            target_dir = Path(custom_dir)
            if self._is_valid_directory(target_dir):
                target_dir.mkdir(parents=True, exist_ok=True)
                return target_dir.resolve()
        
        # Bad/No custom dir, using default dir
        current_script_dir = Path(__file__).resolve().parent
        target_dir = current_script_dir.parent / self._DEFAULT_DIR_NAME
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir
            
    def _is_valid_directory(self, directory: Path) -> bool:
        if not directory.exists():
            parent_dir = directory.parent
            if not parent_dir.is_dir():
                print(f"""Custom directory '{parent_dir}' for '{self._DEFAULT_DIR_NAME}' does not exist. Using default dir.""")
                return False
        
        if any(char in str(directory.name) for char in '<>:"/\\|?*'):
            print(f"Custom directory '{directory}' for '{self._DEFAULT_DIR_NAME}' contains invalid characters. Using default dir.")
            return False
            
        return True
            
class SongDetailsOutputer(SongFileWriter):
    _DEFAULT_DIR_NAME = 'output'
    
    def __init__(self, out_dir: str) -> None:
        self.out_dir = self.resolve_directory_path(out_dir) / 'songdetails.csv'
        
    def output(self, song_details: List[Dict[str, str]]) -> None:
        with open(self.out_dir, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=song_details[0].keys())
            writer.writeheader()
            for details in song_details:
                writer.writerow(details)

class SongCacher(SongFileWriter):
    _DEFAULT_DIR_NAME = 'cache'
    
    def __init__(self, cache_dir: str) -> None:
        self.cache_dir = self.resolve_directory_path(cache_dir) / 'songcache.db'
        
    def cache_song(self, url: str, song_details: Dict[str, str]) -> None:
        with shelve.open(self.cache_dir) as cache:
            cache[url] = song_details
            
    def get_cached_songs(self) -> Dict[str, Dict[str, str]]:
        with shelve.open(self.cache_dir) as cache:
            return dict(cache)
    
    def clear_cache(self) -> None:
        with shelve.open(self.cache_dir) as cache:
            cache.clear()

class SongLogger(SongFileWriter):
    _DEFAULT_DIR_NAME = 'log'
    
    def __init__(self, log_dir: str, module_name: str) -> None:
        self.log_dir = self.resolve_directory_path(log_dir) / 'tab_scraper.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=self.log_dir,
            filemode='w',
            force=True
        )
        
        self.logger = logging.getLogger(module_name)
        atexit.register(logging.shutdown)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warn(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)