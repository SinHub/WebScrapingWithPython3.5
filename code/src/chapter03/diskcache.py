import os
import re
import pickle
from urllib.parse import urlsplit

class DiskCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        
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
                return pickle.load(fp)
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
        with open(path, 'wb') as fp:
            fp.write(pickle.dumps(result))