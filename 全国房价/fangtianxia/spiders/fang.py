import scrapy
import re
from fangtianxia.items import NewHouseItem,esfHouseItem
from scrapy_redis.spiders import RedisSpider
class FangSpider(RedisSpider):
    name = 'fang'
    redis_key = 'citylist_start_url'
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(FangSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        trs = response.xpath('//*[@id="c02"]//tr')
        # 定义省份名字保存，如果解析出来没名字的就用上次的省份
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            # 提取省份名字
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            # 正则去掉文本空白
            province_text = re.sub(r"\s","", province_text)
            # 判断是否没省份
            if province_text:
                province = province_text
                # 过滤国外的城市
            if province == '其它':
                continue
            else:
                city_td = tds[1]
                city_links = city_td.xpath('.//a')
                for city_link in city_links:
                    city = city_link.xpath('.//text()').get()
                    city_url = city_link.xpath('.//@href').get()

                    # 构建url连接 模板：https://hf.newhouse.fang.com/house/s/
                    url_module = city_url.split('.')  # ['http://zz', 'fang', 'com/']
                    str1 = url_module[0]
                    str2 = url_module[1]
                    str3 = url_module[2]
                    # 获取新房和二手房url
                    # 北京做特殊处理
                    if 'bj' in str1:
                        newhouse_url = 'https://newhouse.fang.com/house/s/'
                        esfhouse_url = 'https://esf.fang.com/'
                    else:
                        if str3 == 'com/':
                            newhouse_url = str1 +'.newhouse.'+str2 + '.' + str3 + 'house/s/'
                            esfhouse_url = str1 + '.esf.' + str2 + '.' + str3 + 'house/s/'
                        else:
                            newhouse_url = str1 + '.newhouse.' + str2 + './' + str3 + 'house/s/'
                            esfhouse_url = str1 + '.esf.' + str2 + './' + str3 + 'house/s/'
                        # 对新房url发请求：
                    yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,
                                         meta={'info':(province,city)})
                    # 对二手房url请求
                    yield scrapy.Request(url=esfhouse_url,callback=self.parse_esfhouse,
                                         meta={'info': (province, city)})


    # 新房数据解析
    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath('//*[@id="newhouse_loupan_list"]/ul/li')
        try:
            for li in lis:
                name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get().strip()
                origin_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
                house_type_list = li.xpath('.//div[@class="house_type clearfix"]//text()').getall()
                house_type_list = [i.strip() for i in house_type_list]
                house_type_list = ''.join(house_type_list)
                if house_type_list:
                    rooms = house_type_list.split('—')[0]
                    area = house_type_list.split('—')[1]
                else:
                    rooms = '暂无'
                    area = '暂无'
                adrs = li.xpath('.//div[@class="address"]/a/text()').get().strip()
                address = adrs.split(']')[1]
                district = adrs.split(']')[0] + ']'
                sale = li.xpath('.//div[@class="fangyuan"]/span/text()').get().strip()
                styles = li.xpath('.//div[@class="fangyuan"]/a/text()').extract()
                style = ','.join(styles)
                prices = li.xpath('.//div[@class="nhouse_price"]//text()').extract()
                price = ''.join(prices).strip()
                item = NewHouseItem()
                item['province'] = province
                item['city'] = city
                item['name'] = name
                item['area'] = area
                item['rooms'] = rooms
                item['address'] = address
                item['district'] = district
                item['sale'] = sale
                item['style'] = style
                item['sale'] = sale
                item['price'] = price
                item['origin_url'] = origin_url
                yield item
        except:
            pass
        next_url = response.xpath('.//div[@class="page"]//a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin('next_url'),
                                     callback=self.parse_newhouse,meta={'info':(province,city)})

    def parse_esfhouse(self,response):
        province, city = response.meta.get('info')
        dls = response.xpath('/html/body/div[4]/div[4]/div[4]/dl')
        for dl in dls:
            item = esfHouseItem(province=province, city=city)
            name = dl.xpath('.//p[@class="add_shop"]/a/text()').get()
            address = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
            item['address'] = address
            prices = dl.xpath('.//dd[@class="price_right"]//text()').getall()
            prices = [i.strip() for i in prices]
            if prices != []:
                item['price'] = prices[2]+prices[3]
                item['unit'] = prices[5]
            else:
                item['price'] = '暂无价格'
                item['unit'] = '暂无价格'
            if name == None:
                item['name'] = '暂无名字'
            else:
                item['name'] = name.strip()
            house_info_list = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
            house_info_list = [i.strip() for i in house_info_list]
            for house_info in house_info_list:
                if "厅" in house_info:
                    item['rooms'] = house_info
                elif ("层" or "栋") in house_info:
                    item['floor'] = house_info
                elif "向" in house_info:
                    item['toward'] = house_info
                elif "建" in house_info:
                    item['years'] = house_info
                elif "㎡" in house_info:
                    item['area'] = house_info
                else:
                    item['other'] = '暂无信息'
            yield item
        next_url = response.xpath('.//div[@class="page_al"]/p[1]/a/@href').get()
        if next_url:
            next_url = 'https://esf.fang.com' + next_url
            yield scrapy.Request(url=next_url,
                                callback=self.parse_esfhouse,meta={'info':(province,city)})


















