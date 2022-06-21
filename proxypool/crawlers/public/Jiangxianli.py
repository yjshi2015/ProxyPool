import json
from proxypool.schemas.proxy import Proxy
import requests
from loguru import logger
from proxypool.crawlers.base import BaseCrawler


BASE_URL = 'https://ip.jiangxianli.com/api/proxy_ips?page={page}'
class Jiangxianli(BaseCrawler):
    MAX_PAGE = 3
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE)]

    def parse(self, html):
        html_json = json.loads(html)
        ip_list = html_json.get('data')['data']
        if ip_list:
            for item in ip_list:
                # todo syj 筛选https代理
                # if item['protocol'] == 'https':
                yield Proxy(host=item['ip'], port=item['port'])


if __name__ == '__main__':
    jiangxianli = Jiangxianli()
    proxies = jiangxianli.crawl()
    for proxy in proxies:
        print('proxy : ' + proxy.string())
