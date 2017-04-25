import re
from datetime import timedelta
from urllib.parse import urljoin,urlparse
from urllib.robotparser import RobotFileParser
from scrapecallback import ScrapeCallback
from downloader import Downloader
from diskcache import DiskCache

        
def link_crawler(seed_url, link_regex, max_depth=1, cache_callback = None, scrape_callback = None):
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
        if not is_robot_friendly(seed_url, url, user_agent='wswp'):
            print("Blocked by robots.txt: " + url)
            continue
        html = D(url)
        if scrape_callback:
            links.extend(scrape_callback(url, html) or [])
        if( depth == max_depth ):
            # print("Stop by the limit of depth " + str(max_depth) + ".")
            continue
        # filter for links matching our regular expression
        for link in get_links(html):
            # check if link matches expected regex
            if re.match(link_regex, link):
                # check if have already seen this link
                link = urljoin(seed_url, link)
                if link not in seen:
                    seen[link] = depth + 1
                    crawl_queue.append(link)
                
def get_links(html):
    '''Return a list of links from html
    '''
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

def is_robot_friendly(base_url, url, user_agent):
    rp = RobotFileParser()
    rp.set_url(urljoin(base_url, '/robots.txt'))
    rp.read()
    return rp.can_fetch(user_agent, url)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com','/(index|view)', max_depth=-1, cache_callback=DiskCache(), scrape_callback=ScrapeCallback())
