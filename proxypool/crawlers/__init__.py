import pkgutil
from .base import BaseCrawler
import inspect

'''
多个crawler子类从不同的网站爬取代理，在这里统一将所有子类汇总起来，添加到classes中返回。
最后只要遍历classes里面的类，并以此实例化，调用各自的crawl方法即可完成代理的爬取跟提取
'''
classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    for name, value in inspect.getmembers(module):
        globals()[name] = value
        if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler:
            classes.append(value)
__all__ = __ALL__ = classes