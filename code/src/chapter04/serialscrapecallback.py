import csv

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('alexa.csv','w', newline=''))
        self.writer.writerow(['url', 'time/ms'])

    def __call__(self, url, time):
        row = [url, time]
        self.writer.writerow(row)