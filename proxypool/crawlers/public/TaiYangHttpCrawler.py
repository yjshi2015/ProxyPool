from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from pyquery import PyQuery as pq

BASE_URL = 'http://www.taiyanghttp.com/free/page{num}/'


class TaiYangHttpScrawler(BaseCrawler):
    MAX_NUM = 30
    urls = [BASE_URL.format(num=num) for num in range(1, MAX_NUM)]

    def parse(self, html):
        doc = pq(html)
        trs = doc('#ip_list .tr.ip_tr').items()
        for tr in trs:
            host = tr.find('div:nth-child(1)').text()
            port = tr.find('div:nth-child(2)').text()
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    taiYangCrawler = TaiYangHttpScrawler()
    for proxy in taiYangCrawler.crawl():
        print(proxy)
