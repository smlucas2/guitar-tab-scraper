# -*- coding: utf-8 -*-

import argparse

from tab_scraper.tab_scraper import UltimateGuitarScraper
   
def main():
    args = _build_arg_parser()
    _run_scraper(args)
        
def _build_arg_parser():
    parser = argparse.ArgumentParser(description="Web scraper for guitar tabs")
    parser.add_argument("-u", "--url", type=str, help="URL to scrape")
    parser.add_argument("--output", type=str, default=None, help="Output path. Defaults to tab_scraper directory output folder.")
    parser.add_argument("--cache", type=str, default=None, help="Cache path. Defaults to tab_scraper directory songcache folder.")
    parser.add_argument("--logs", type=str, default=None, help="Log path. Defaults to tab_scraper directory logs folder.")
    parser.add_argument("-c", action='store_true', help="Clears the song cache.")
    return parser.parse_args()

def _run_scraper(args):
    scraper = UltimateGuitarScraper(args.out)
    if args.clear:
        scraper.clear_cache()
    
    if args.tab:
        scraper.scrape_url(args.url)
    else:
        scraper.scrape_songs()

if __name__ == '__main__':
    main()