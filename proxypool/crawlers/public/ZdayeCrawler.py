from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from pyquery import PyQuery as pq
import requests


BASE_URL = 'https://www.zdaye.com'
INDEX_URL = 'https://www.zdaye.com/dayProxy/1.html'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

class ZdayeCrawler(BaseCrawler):



    def __init__(self):
        '''
        获取列表页最新的文章，即第一篇文章（包含了最新的代理ip信息）
        ip信息需要分页获取，构造urls
        '''
        response = requests.get(INDEX_URL, headers=headers)
        doc = pq(response.text)
        contents = doc('#J_posts_list .thread_item').items()
        for content in contents:
            lable = content.find('.thread_title a')
            suffix_origin = lable.attr('href')
            suffix = suffix_origin[:suffix_origin.find('.')]
            self.urls = [BASE_URL + suffix + '/' + str(i) +'.html' for i in range(1,4)]
            break

    def parse(self, html):
        doc = pq(html)
        contents = doc('#ipc tbody tr').items()
        for content in contents:
            # 以下取值中存在&nbsp;处理起来比较麻烦，因此从其他地方获取
            # ip = content.find('td:nth-child(1)').text().strip()
            # port = content.find('td:nth-child(2)').text().strip()
            check_link = content.find('td:nth-child(2) a').attr('href')
            ip, port = check_link[check_link.rfind('/') + 1:].split(':')
            yield Proxy(host=ip, port=port)


if __name__ == '__main__':
    zdaye = ZdayeCrawler()
    # syj 此处传参必须为key/value形式，不可以直接传入value
    for proxy in zdaye.crawl(headers=headers):
        print(proxy)