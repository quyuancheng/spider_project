import scrapy
from selenium import webdriver
from wangyi_news.items import WangyiNewsItem

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']

    model_url_list = []
    bro = webdriver.Chrome(executable_path='/home/ubuntu/PycharmProjects/Scrapy/selenium/chromedriver')
    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        li_index = [2,3,5,6]
        for i in li_index:
            title1 = li_list[i].xpath('./a/text()').extract_first()
            model_url = li_list[i].xpath('./a/@href').extract_first()
            self.model_url_list.append(model_url)
        for url in self.model_url_list:
            yield scrapy.Request(url=url,callback=self.parse_model)
    def parse_model(self,response):
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            content_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item = WangyiNewsItem()
            item['title'] = title
            if content_url:
                yield scrapy.Request(url=content_url,callback=self.parse_del,meta={'item':item})
    def parse_del(self,response):
        cont = response.xpath('//*[@id="content"]/div[2]/p/text()').extract()
        content = ''.join(cont).strip()
        item = response.meta['item']
        item['content'] = content
        print(item)
        yield item
    def closed(self,spider):
        self.bro.quit()







