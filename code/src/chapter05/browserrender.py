import time
import sys
from PyQt4.QtGui import * #QApplication
from PyQt4.QtWebKit import * #QWebView
from PyQt4.QtCore import * #QEventLoop

class BrowserRender(QWebView):
    def __init__(self, parent=None, show=True):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        if show:
            self.show() # show the browser
            
    def download(self, url, timeout=60):
        '''Wait for download to complete and return result'''
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)
        self.load(QUrl(url))
        timer.start(timeout * 1000)
        
        loop.exec_()    # delay here until download finished
        if timer.isActive():
            # downloaded successfully
            timer.stop()
            return self.html()
        else:
            # timed out
            print('Request timed out: ' + url)
            
    def html(self):
        '''Shortcut to return the current HTML'''
        return self.page().mainFrame().toHtml()
    
    def find(self, pattern):
        '''Find all elements that match the pattern'''
        return self.page().mainFrame().findAllElements(pattern)
    
    def attr(self, pattern, name, value):
        '''Set attribute for matching elements'''
        for e in self.find(pattern):
            e.setAttribute(name, value)
            
    def text(self, pattern, value):
        '''Set attribute for matching elements'''
        for e in self.find(pattern):
            e.setPlainText(value)
            
    def click(self, pattern):
        '''Click matching elements'''
        for e in self.find(pattern):
            e.evaluateJavaScript("this.click()")
            
    def wait_load(self, pattern, timeout=60):
        '''Wait untill pattern is found and return matches'''
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.app.processEvents()
            matches = self.find(pattern)
            if matches:
                return matches
        print('Wait load timed out')