from downloader import Downloader
from urllib.parse import urljoin
from alexacallback import AlexaCallback
import datetime
import time
import threading

SLEEP_TIME = 1

def crawler(seed_url, delay=5, scrape_callback=None, cache=None, user_agent="wswp", num_retries=1, proxies=None, timeout=60, ignore_robots=True):
    '''Crawle the websit'''
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,cache=cache)
    alexa_callback = AlexaCallback(max_urls=100)
    crawl_queue = [seed_url]
    # 扩展爬虫网站队列
    crawl_queue.extend(alexa_callback())
    seen = set([seed_url])
    startTime = datetime.datetime.now()
    while crawl_queue:
        urlBegin = datetime.datetime.now()
        url = crawl_queue.pop()
        html = D(url)
        urlEnd = datetime.datetime.now()
        if(scrape_callback):
            scrape_callback(url, str((urlEnd - urlBegin).microseconds))
        else:
            print("Run Time: %d ms" % (urlEnd - urlBegin).microseconds)
    endTime = datetime.datetime.now()
    print("Total Run Time: %d s" % (endTime - startTime).seconds)
   
        
def thread_crawler(seed_url, delay=5, scrape_callback=None, cache=None, user_agent="wswp", num_retries=1, proxies=None, timeout=60, ignore_robots=True, max_threads=10):
    '''Crawle the websit'''
    # the queue of URL's that still need to be crawled
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,cache=cache)
    alexa_callback = AlexaCallback(max_urls=100)
    crawl_queue = [seed_url]
    # 扩展爬虫网站队列
    crawl_queue.extend(alexa_callback())
    seen = set([seed_url])
    
    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                # crawl queue is empty
                break
            else:
                urlBegin = datetime.datetime.now()
                html = D(url)
                urlEnd = datetime.datetime.now()
                if(scrape_callback):
                    scrape_callback(url, str((urlEnd - urlBegin).microseconds))
                else:
                    print("Run Time: %d ms" % (urlEnd - urlBegin).microseconds)
                    
    threads = []
    startTime = datetime.datetime.now()
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution elsewhere
        time.sleep(SLEEP_TIME)
    endTime = datetime.datetime.now()
    print("Total Run Time: %d s" % (endTime - startTime).seconds)        