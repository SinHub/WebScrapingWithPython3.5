import crawler_1
import re
from bs4 import BeautifulSoup
import lxml.html


if __name__ == "__main__":
    url = 'http://example.webscraping.com/view/United-Kingdom-239'
    html = crawl.download(url)
    print(re.findall('<td class="w2p_fw">(.*?)</td>', html)[1])
    print(re.findall('<tr id="places_area__row"><td class="w2p_fl"><label for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html))
    print(re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html))
    soup = BeautifulSoup(html,"html.parser")
    tr = soup.find(attrs={'id':'places_area__row'})
    td = tr.find(attrs={'class':'w2p_fw'})
    area = td.text
    print(area)
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
    area = td.text_content()
    print(area)