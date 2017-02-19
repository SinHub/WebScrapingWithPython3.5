import re
from datetime import timedelta
from urllib.parse import urljoin,urlparse
from urllib.robotparser import RobotFileParser
from alexacallback import AlexaCallback
from downloader import Downloader
from diskcache import DiskCache

        
def link_crawler(seed_url, cache_callback = None, scrape_callback = None):
    '''Crawl from given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = { seed_url: 0 }
    links = []
    D = Downloader(delay=1, user_agent='wswp', proxies=None, num_retries=1, cache = cache_callback)
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen.get(url) or 0
        html = D(url)
        if scrape_callback and depth == 0:
            links.extend(scrape_callback(url, html) or [])
        # filter for links matching our regular expression
        for link in get_links(html):
            # check if link matches expected regex
            if re.match(link_regex, link):
                # check if have already seen this link
                link = urljoin(seed_url, link)
                if link not in seen:
                    seen[link] = depth + 1
                    crawl_queue.append(link)
                


if __name__ == '__main__':
    scrape_callback = AlexaCallback()
    link_crawler('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', cache_callback=None, scrape_callback=scrape_callback)
