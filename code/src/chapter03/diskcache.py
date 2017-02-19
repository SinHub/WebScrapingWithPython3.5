import os
import re
import pickle
import zlib
from datetime import datetime, timedelta
from urllib.parse import urlsplit

class DiskCache:
    def __init__(self, cache_dir='cache', expires=timedelta(days=30)):
        self.cache_dir = cache_dir
        self.expires = expires
        
    def url_to_path(self, url):
        '''Create file system path for this URL
        '''
        components = urlsplit(url)
        # append index.html to empty paths
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)
        # restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)
    
    def __getitem__(self, url):
        '''Load data from disk for this URL
        '''
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                # zlib 解压缩 + pickle 装载(反序列化)
                result, timestamp = pickle.loads(zlib.decompress(fp.read()))
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')
            
    def __setitem__(self, url, result):
        '''Save data to disk for this url
        '''
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        timestamp = datetime.utcnow()
        data = pickle.dumps((result, timestamp))
        with open(path, 'wb') as fp:
            # pickle 序列化 + zlib 压缩
            fp.write(zlib.compress(data))
            
    def has_expired(self, timestamp):
        '''Return whether this timestamp has expired
        '''
        return datetime.utcnow() > timestamp + self.expires