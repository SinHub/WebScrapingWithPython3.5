from crawler import crawler
from diskcache import DiskCache
from alexacallback import AlexaCallback
from scrapecallback import ScrapeCallback

def main():
    scrape_callback = ScrapeCallback()
    cache = DiskCache()
    #cache.clear()
    crawler('http://example.webscraping.com', scrape_callback=scrape_callback, cache=cache, timeout=10, ignore_robots=True)
    
    
if __name__ == '__main__':
        main()