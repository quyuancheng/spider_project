# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from redis import Redis
import pymongo
# class MongodbPipeline():
#     conn = None
#     def open_spider(self,spider):
#         self.conn = pymongo.MongoClient(host='127.0.0.1',port=27017)
#         print(self.conn)
#     def process_item(self,item,spider):
#         # 指定数据库
#         db = self.conn['spider']
#         # 指定制定集合
#         db_set = db['wangyinews']
#         # 插入数据
#         db_set.insert(dict(item))
#         return item

# class RedisPipeline:
#     conn = None
#     def open_spider(self,spider):
#         self.conn = Redis(host='127.0.0.1',port='6379')
#         print(self.conn)
#     def process_item(self, item, spider):
#         self.conn.lpush('wangyinews',item)
#         return item


# class MysqlPipeline(object):
#     conn = None
#     cur = None
#     def open_spider(self,spider):
#         self.conn = pymysql.connect(host='127.0.0.1',user='root',password='mysql',
#                                database='spider',charset='utf8')
#         print(self.conn)
#
#     def process_item(self, item, spider):
#         self.cur = self.conn.cursor()
#         insert_data_sql = 'insert into wangyi_news(title,content) values (%s,%s)'
#         try:
#             self.cur.execute(insert_data_sql, (item['title'], item['content']))
#             self.conn.commit()
#         except Exception as e:
#             print(e)
#             self.conn.rollback()
#         return item
