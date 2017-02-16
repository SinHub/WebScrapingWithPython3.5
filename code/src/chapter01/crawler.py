import re
import requests
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from throttle import Throttle


def print_url(r, *args, ** kwargs):
    print(r.status_code)

def download(url, headers=None, num_retries=2):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    proxies = {
        "http" : "http://10.0.2.19:8888"
    }
    print('Downloading:', url)
    try:
        # req = requests.get(url, headers = headers, proxies=proxies, hooks = dict({"response":print_url})) # 使用代理的情况
        req = requests.get(url, headers = headers, hooks = dict({"response":print_url}))
        req.raise_for_status() # 遇到客户端错误4XX或服务端错误5XX会抛出 HTTPError 错误，否则输出 None
        html = req.text
    except requests.exceptions.ConnectionError as ce:
        print('Connection error:', str(ce))
        html = None
    except requests.exceptions.HTTPError as he:
        print('HTTP error:', str(he))
        if(num_retries > 0):
            if(500 <= he.response.status_code < 600):
                download(url, headers, num_retries-1)
        html = None
    return html

def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)
        
def link_crawler(seed_url, link_regex, max_depth=1):
    '''Crawl from given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = {}
    while crawl_queue:
        url = crawl_queue.pop()
        if not is_robot_friendly(seed_url, url, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'):
            print("Blocked by robots.txt: " + url)
            continue
        throttle = Throttle(1)
        throttle.wait(url)
        depth = seen.get(url) or 0
        html = download(url)
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
    #download("http://zhihu.com/")
    #crawl_sitemap('http://example.webscraping.com/sitemap.xml')
    #download("http://httpbin.org/status/502")
    link_crawler('http://example.webscraping.com','/(index|view)')
    
    
