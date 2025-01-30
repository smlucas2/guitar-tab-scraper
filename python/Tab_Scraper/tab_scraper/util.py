# -*- coding: utf-8 -*-

import shelve
import csv
import sys
from typing import Dict, List
from pathlib import Path

class SongFileWriter:
    
    def resolve_directory_path(self, custom_dir: str, default_dir: str) -> Path:
        if custom_dir is None:
            current_script_dir = Path(__file__).resolve().parent
    
            target_dir = current_script_dir.parent / default_dir
            target_dir.mkdir(parents=True, exist_ok=True)
            return target_dir
        else:
            target_dir = Path(custom_dir)
            self._validate_directory(target_dir)
            
            target_dir.mkdir(parents=True, exist_ok=True)
            return target_dir
            
    def _validate_directory(self, directory: Path):
        if not directory.exists():
            parent_dir = directory.parent
            if not parent_dir.is_dir():
                print(f"Parent directory '{parent_dir}' does not exist.")
                sys.exit(1)
        
        if any(char in str(directory.name) for char in '<>:"/\\|?*'):
            print(f"Directory '{directory}' contains invalid characters.")
            sys.exit(1)
            
class SongDetailsOutputer(SongFileWriter):
    
    def __init__(self, out_dir: str) -> None:
        self.out_dir = self.resolve_directory_path(out_dir, "output") / "songdetails.csv"
        
    def output(self, song_details: List[Dict[str, str]]) -> None:
        with open(self.out_dir, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=song_details[0].keys())
            writer.writeheader()
            for details in song_details:
                writer.writerow(details)

class SongCacher(SongFileWriter):
    
    def __init__(self, cache_dir: str) -> None:
        self.cache_dir = self.resolve_directory_path(cache_dir, "songcache") / "songcache.db"
        
    def cache_song(self, url: str, song_details: Dict[str, str]) -> None:
        with shelve.open(self.cache_dir) as cache:
            cache[url] = song_details
            
    def get_cached_songs(self) -> Dict[str, Dict[str, str]]:
        with shelve.open(self.cache_dir) as cache:
            return dict(cache)
    
    def clear_cache(self) -> None:
        with shelve.open(self.cache_dir) as cache:
            cache.clear()