# -*- coding: utf-8 -*-

import os
import shelve

class SongCache:
    
    def __init__(self, cache_path):
        if cache_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            default_cache_dir = os.path.join(base_dir, "..", "..", "songcache")
            os.makedirs(default_cache_dir, exist_ok=True)
            self.cache_path = os.path.join(default_cache_dir, "songcache.db")
        else:
            self.cache_path = cache_path
        
    def cache_song(self, url, song_details):
        with shelve.open(self.cache_path) as cache:
            cache[url] = song_details
            
    def get_cached_songs(self):
        with shelve.open(self.cache_path) as cache:
            return dict(cache)
    
    def clear_cache(self):
        with shelve.open(self.cache_path) as cache:
            cache.clear()
        