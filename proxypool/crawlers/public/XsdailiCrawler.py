from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import requests

BASE_URL = 'https://www.xsdaili.cn'


class XsdailiCrawler(BaseCrawler):

    urls = []

    def __init__(self):
        response = requests.get(BASE_URL)
        doc = pq(response.text)
        titles = doc(".title a").items()
        for title in titles:
            link = title.attr("href")
            self.urls.append(BASE_URL + link)
            # 只获取头2个链接
            if len(self.urls) == 2:
                break

    def parse(self, html):
        doc = pq(html)
        content = doc('.row .col-md-12 .cont').text()
        ip_addresses = content.split('\n')
        for ip_address in ip_addresses:
            proxy_str = ip_address[:ip_address.find('@')]
            ip, port = proxy_str.split(':')
            yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    xsdaili = XsdailiCrawler()
    for proxy in xsdaili.crawl():
        print(proxy)