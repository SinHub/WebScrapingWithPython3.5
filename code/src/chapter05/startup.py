import lxml.html
from downloader import Downloader
from scrapecallback import ScrapeCallback
from browserrender import BrowserRender
import json
import csv
import string
import re

D = Downloader()
'''init()代码'''
# html = D("http://example.webscraping.com/search")
# tree = lxml.html.fromstring(html)
# tree.cssselect('div#results a')

def first():
    '''循环串行读取'''
    template_url = 'http://example.webscraping.com/ajax/search.json?page={}&page_size=10&search_term={}'
    countries = set()
    
    for letter in string.ascii_lowercase:
        page = 0
        while True:
            html = D(template_url.format(page, letter))
            try:
                ajax = json.loads(html)
            except ValueError as e:
                print(e)
                ajax = None
            else:
                for record in ajax['records']:
                    countries.add(record['country'])
            page += 1
            if ajax is None or page >= ajax['num_pages']:
                break
        open('countries.txt', 'w').write('\n'.join(sorted(countries)))
        
def second():
    '''优化边界'''
    FIELDS = ('country', 'id', 'pretty_link', 'country', 'capital', 'continent', 'tld', 'currency_code',
              'currency_name','phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
    # FIELDS = ('country', 'id', 'pretty_link')
    writer = csv.writer(open('countries.csv', 'w'))
    writer.writerow(FIELDS)
    seed_url = "http://example.webscraping.com/ajax/search.json?page=0&page_size=1000&search_term=."
    html = D(seed_url)
    scrape_callback = ScrapeCallback()
    href_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    ajax = json.loads(html)
    for record in ajax['records']:
        url = "http://example.webscraping.com" + href_regex.findall(record['pretty_link'])[0]
        html = D(url)
        scrape_callback(url, html)
    
            
def third():
    '''使用Qt WebKit内核'''
    br = BrowserRender()
    br.download('http://example.webscraping.com/search')
    br.attr('#search_term', 'value', '.')
    br.text('#page_size option[selected]', '1000')
    br.click('#search')
    elements = br.wait_load('#results a')
    countries = [e.toPlainText().strip() for e in elements]
    print(countries)
        
        
def fourth():
    '''使用Selenium'''
    from selenium import webdriver
    # IE 浏览器需要关闭保护模式，有两种方法：
    # 1.修改注册表 HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones 的 1~4 文件的 2500 的属性值为非零值
    # 2.加入下面两行代码
    # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
    # DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True      
    driver = webdriver.Ie()
    driver.get('http://example.webscraping.com/search')
    driver.find_element_by_id('search_term').send_keys('.')
    js = "document.getElementById('page_size').options[1].text='1000'"
    driver.execute_script(js)
    driver.find_element_by_id('search').click()
    # 等待ajax返回，设置30秒延时
    driver.implicitly_wait(10)
    links = driver.find_elements_by_css_selector('#results a')
    countries = [link.text for link in links]
    print(countries)
    driver.close()
    
    
if __name__ == '__main__':
    fourth()