# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from tab_scraper.tab_scraper import UltimateGuitarScraper
   
def main() -> None:
    args = _build_arg_parser()
    _run_scraper(args)
        
def _build_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Web scraper for guitar tabs")
    parser.add_argument("-t", "--tab", type=str, help="Tab URL to scrape")
    parser.add_argument("-l", "--limit", type=int, default=None, help="Limit on the amount of pages to scrape")
    parser.add_argument("-o", "--offset", type=int, default=0, help="Offset on the amount of pages to scrape")
    parser.add_argument("--output", type=str, default=None, help="Output directory. Defaults to [Tab_Scraper/output] directory.")
    parser.add_argument("--cache", type=str, default=None, help="Cache directory. Defaults to [Tab_Scraper/cache] directory.")
    parser.add_argument("--logs", type=str, default=None, help="Log directory. Defaults to [Tab_Scraper/logs] directory.")
    parser.add_argument("-c", action='store_true', help="Clears the song cache.")
    return parser.parse_args()

def _run_scraper(args: ArgumentParser) -> None:
    scraper = UltimateGuitarScraper(args.output, args.cache, args.logs)
    if args.c:
        scraper.clear_cache()
    
    if args.tab:
        scraper.scrape_url(args.tab)
    else:
        scraper.scrape_songs(args.limit, args.offset)

if __name__ == '__main__':
    main()