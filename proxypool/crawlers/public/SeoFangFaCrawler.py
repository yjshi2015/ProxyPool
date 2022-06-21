import re
from proxypool.crawlers import BaseCrawler
from proxypool.schemas.proxy import Proxy


class SeoFangFaCrawler(BaseCrawler):

    urls = ['https://proxy.seofangfa.com/']

    def parse(self, html):
        ip_address_re = re.compile('<tr><td>(.*?)</td><td>(.*?)</td>')
        ip_adresses = ip_address_re.findall(html)
        for ip, port in ip_adresses:
            yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    seoFangFa = SeoFangFaCrawler()
    proxies = seoFangFa.crawl()
    for proxy in proxies:
        print("proxy", proxy)