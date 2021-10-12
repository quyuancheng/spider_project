# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import base64
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11'
    ]
    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent

class ProxyDownloadMiddleware(object):
    def process_request(self, request, spider):
        proxy = 'http://115.28.107.149:16817'
        # user_password = "94251049:5rv6zk1h"
        request.meta['proxy'] = proxy
#         # b64_user_password = base64.b64encode(user_password.encode('utf-8'))
#         # request.headers['Proxy-Authorization'] = 'Basic ' +  b64_user_password.decode('utf-8')
# class PoolProxyDownloadMiddleware(object):
#     PROXYS = ['114.98.114.41:3256','106.45.105.132:3256','122.51.207.244:8888',
#               '121.232.148.63:3256','111.177.192.91:3256']
#     def process_request(self,request,spider):
#         proxy = random.choice(self.PROXYS)
#         request.meta['proxy'] = proxy