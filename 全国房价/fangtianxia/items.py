# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区的名字
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 几居  列表
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 风格
    style = scrapy.Field()
    # 房天下详情页面url
    origin_url = scrapy.Field()

class esfHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区的名字
    name = scrapy.Field()
    #几居
    rooms = scrapy.Field()
    # 层数
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 年代
    years = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    # 其它说明
    other = scrapy.Field()