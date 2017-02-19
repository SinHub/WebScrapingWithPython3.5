from crawler import Crawler
from diskcache import DiskCache
from alexacallback import AlexaCallback

def main():
    scrape_callback = AlexaCallback()
    cache = DiskCache()
    #cache.clear()
    Crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, timeout=10, ignore_robots=True)
    
    
    if __name__ == '__main__':
        main()    