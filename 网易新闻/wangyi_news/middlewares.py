# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from time import sleep

from scrapy.http import HtmlResponse


class WangyiNewsDownloaderMiddleware:


    def process_request(self, request, spider):

        return None

    def process_response(self, request, response, spider):
        if request.url in spider.model_url_list:
            bro = spider.bro
            bro.get(request.url)
            sleep(2)
            # 捕获到页面加载出来的全部数据(包含了动态加载的数据)
            page_text = bro.page_source
            # response.text = page_text
            return HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
        else:
            return response


    def process_exception(self, request, exception, spider):

        pass


