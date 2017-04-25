import re
from downloader import Downloader
from urllib.parse import urljoin

def crawler(seed_url, delay=5, scrape_callback=None, cache=None, user_agent="wswp", num_retries=1, proxies=None, timeout=60, ignore_robots=True):
    '''Crawel this website
    '''
    crawl_queue = [seed_url]
    seen = { seed_url: 0 }
    links = []
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen.get(url) or 0
        html = D(url)
        if scrape_callback and depth == 0:
            links.extend(scrape_callback(url, html) or [])
        # filter for links matching our regular expression
        for link in get_links(html):
            # check if link matches expected regex
            if re.match('/(index|view)', link):
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