import re
import lxml.html
import csv

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w', newline=''))
        self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld',
                       'currency_code','currency_name', 'phone', 'postal_code_format','postal_code_regex',
                       'languages','neighbours')
        self.writer.writerow(self.fields)
        
    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)
