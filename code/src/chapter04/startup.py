# from crawler import crawler
# from diskcache import DiskCache
# from scrapecallback import ScrapeCallback
from crawler_fromzip import crawler, thread_crawler
from serialscrapecallback import ScrapeCallback

def main():
    scrape_callback = ScrapeCallback()
    # cache = DiskCache()
    # cache.clear()
    # crawler('http://example.webscraping.com', scrape_callback=scrape_callback, cache=None, timeout=10, ignore_robots=True)
    thread_crawler('http://example.webscraping.com', scrape_callback=scrape_callback, cache=None, timeout=10, ignore_robots=True, max_threads=1)
    
    
if __name__ == '__main__':
    main()