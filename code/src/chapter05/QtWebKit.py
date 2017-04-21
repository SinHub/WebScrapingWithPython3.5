import lxml.html
from PyQt4.QtGui import * #QApplication
from PyQt4.QtWebKit import * #QWebView
from PyQt4.QtCore import * #QEventLoop

def first():
    url = 'http://example.webscraping.com/dynamic'
    # Qt其他对象初始化前必须先创建 Application 对象
    app = QApplication([])
    webview = QWebView()
    #1 创建本地事件循环
    loop = QEventLoop()
    #2 webview 的 loadFinished 回调连接了 QEventLoop 的 quit 方法，从而在 网页加载完成后停止事件循环
    webview.loadFinished.connect(loop.quit)
    #3 将要加载的URL传给 webview
    webview.load(QUrl(url))
    #4 由于 webview 的 load 方法是异步的，会直接运行下一行，所以我们使用了 loop.exec_ 来启动事件循环
    loop.exec_()
    # 加载完成后，事件循环退出（#2），抽取HTML数据
    html = webview.page().mainFrame().toHtml()
    tree = lxml.html.fromstring(html)
    print(tree.cssselect('#result')[0].text_content())    

def second():
    app = QApplication([])
    webview = QWebView()
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl('http://example.webscraping.com/search'))
    loop.exec_()
    webview.show()
    frame = webview.page().mainFrame()
    frame.findFirstElement('#search_term').setAttribute('value', '.')
    # frame.findFirstElement('#page_size option[selected]').setAttribute('value','1000')
    # 原书中的选择器例子不能奏效，这里是更改了选择器
    frame.findFirstElement('#page_size option[selected]').setPlainText('1000')
    # 使用evaluateJavaScript进行提交，模拟点击事件，除此之外还允许我们插入任何想要的 JS 代码
    frame.findFirstElement('#search').evaluateJavaScript('this.click()')
    # 1. 不使用该方法脚本将直接结束
    # app.exec_()
    # 2. 等待结束部分：
    elements = None
    while not elements:
        app.processEvents()
        # 不停循环，直到国家连接出现在 results 这个 div 元素中，
        # 每次执行都会调用 app.processEvents()，用于给QT事件执行任务的时间
        elements = frame.findAllElements('#results a')
    countries = [e.toPlainText().strip() for e in elements]
    print(countries)

if __name__ == "__main__":
    second()