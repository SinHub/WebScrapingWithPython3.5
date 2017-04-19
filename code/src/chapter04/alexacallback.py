import os
import csv
from io import StringIO
from zipfile import ZipFile

class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        # self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
        
    def __call__(self):
        # 获取 zip 压缩文件，这里因为连接外网容易被墙
        # get the .zip file because of GFW
        zipped_file = os.path.join(os.getcwd(), 'top-1m.csv.zip')
        urls = []
        with ZipFile(zipped_file) as zf:
            # 获取 zip 压缩文件中的第一个文件
            # get the first file from the .zip compressed file
            zipped_file = zf.namelist()[0]
            # 通过 StringIO 将 zip 的内容转变为 file 类型
            # use StringIO to change file from .zip into type file
            zipped_data = StringIO(zf.read(zipped_file).decode('utf-8'))
            for _, website in csv.reader(zipped_data):
                urls.append("http://" + website)
                if len(urls) == self.max_urls:
                    break;                    
        return urls        