from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from pyquery import PyQuery as pq


class YqIeCrawler(BaseCrawler):
    urls = ['http://ip.yqie.com/ipproxy.htm']

    def parse(self, html):
        doc = pq(html)
        # 根据id和标签确定dom节点，并且设置对应节点的位置>0
        trs = doc('#GridViewOrder tr:gt(0)').items()
        for tr in trs:
            ip = tr.find('td:nth-child(1)').text()
            port = int(tr.find('td:nth-child(2)').text())
            yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    yqiecrawler = YqIeCrawler()
    for proxy in yqiecrawler.crawl():
        print(proxy)