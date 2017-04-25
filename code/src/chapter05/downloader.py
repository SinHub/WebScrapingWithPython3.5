import random
import requests
from throttle import Throttle

class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies = None, num_retries = 1, cache = None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache
        
    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
                print("Retrieve by cache. " + url)
            except KeyError as e:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and (500 <= result['code'] < 600 or result['code'] is None):
                    # server error so ignore result from cache and re-download
                    result = None
        if result is None:
            # result was not loaded from cache
            # so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {
                'User-Agent' : self.user_agent,
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']
            
    def download(self, url, headers, proxy, num_retries, data = None):
        print('Downloading:', url)
        try:
            req = requests.get(url, headers = headers, proxies = proxy, hooks = dict({"response":self.print_url}))
            req.raise_for_status() # 遇到客户端错误4XX或服务端错误5XX会抛出 HTTPError 错误，否则输出 None
            html = req.text
            code = req.status_code
        except requests.exceptions.ConnectionError as ce:
            print('Connection error:', str(ce))
            html = None
            code = None
        except requests.exceptions.HTTPError as he:
            print('HTTP error:', str(he))
            if(num_retries > 0):
                if(500 <= he.response.status_code < 600):
                    download(url, headers, num_retries-1)
            html = None
            code = he.response.status_code
        except:
            return {'html': '', "code": ""}
        return {'html': html, "code": code}

    def print_url(self, r, *args, ** kwargs):
        print(r.status_code)    