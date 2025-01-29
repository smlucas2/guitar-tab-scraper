# -*- coding: utf-8 -*-

import os
import shelve
from typing import Dict

class SongCache:
    
    def __init__(self, cache_path: str) -> None:
        if cache_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            default_cache_dir = os.path.join(base_dir, "..", "..", "songcache")
            os.makedirs(default_cache_dir, exist_ok=True)
            self.cache_path = os.path.join(default_cache_dir, "songcache.db")
        else:
            self.cache_path = cache_path
        
    def cache_song(self, url: str, song_details: Dict[str, str]) -> None:
        with shelve.open(self.cache_path) as cache:
            cache[url] = song_details
            
    def get_cached_songs(self) -> Dict[str, Dict[str, str]]:
        with shelve.open(self.cache_path) as cache:
            return dict(cache)
    
    def clear_cache(self) -> None:
        with shelve.open(self.cache_path) as cache:
            cache.clear()
        