import pymysql
import requests
import threading
from queue import Queue
from lxml import etree
from multiprocessing.dummy import Pool

# queue_list_page_url = Queue(5000)
# queue_del_page_url = Queue(1000)
# queue_sql = Queue(1000)

def stagid_list(queue_stagid):
    start_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start=0&count=15&cc=CN&l=schinese&v=4&tagid=19'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    resp = requests.get(url=start_url,headers=headers).json()
    rgSolrFacetCounts = resp['rgSolrFacetCounts'].keys()
    stag_list = list(rgSolrFacetCounts)
    for i in stag_list:
        queue_stagid.put(i)

class product_list_url(threading.Thread):
    def __init__(self, queue_list_page_url,stagid_queue, *args, **kwargs):
        super(product_list_url, self).__init__(*args, **kwargs)
        self.queue_list_page_url = queue_list_page_url
        self.stagid_queue = stagid_queue
        stagid = stagid_queue.get()
        try:
            start_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start=0&count=15&cc=CN&l=schinese&v=4&tagid={}'.format(
                stagid)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
            }
            start_resp = requests.get(url=start_url, headers=headers).json()
            # 获取对应分类的结果数
            total_count = start_resp['total_count']
            if start_resp['results_html'] != '':
                start = 0
                while start < total_count:
                    game_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start={}&count=15&cc=CN&l=schinese&v=4&tagid={}'.format(
                        start, stagid)
                    start += 15
                    self.queue_list_page_url.put(game_url)
                    print('添加queue成功')
                else:
                    print('此类型页面获取结束')
        except Exception as e:
            print(e)

class consumer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    def __init__(self,queue_list_page_url,queue_mysql,*args,**kwargs):
        super(consumer,self).__init__(*args,**kwargs)
        self.queue_list_page_url = queue_list_page_url
        self.queue_mysql = queue_mysql

    def parse_list(self,url):
        resp_json = requests.get(url=url, headers=self.headers).json()
        resp = resp_json
        result = resp['results_html'].strip()
        tree = etree.HTML(result)
        text = tree.xpath('.//a')
        for i in text:
            game_id = i.xpath('.//@data-ds-appid')[0]
            game_name = i.xpath('.//div[@class="tab_item_name"]/text()')[0]
            game_price = i.xpath('.//div[@class="discount_final_price"]/text()')
            if game_price == []:
                game_price = '暂无'
            else:
                game_price = game_price[0]
            game_tag = i.xpath('.//div[@class="tab_item_top_tags"]/span/text()')
            game_url = i.xpath('.//@href')[0]
            game_tag = ''.join(game_tag)
            game_info = (game_id, game_name, game_price, game_tag)
            self.queue_mysql.put(game_info)
            # print('{}存入mysql成功'.format(game_info))
    def run(self):
        while True:
            url = self.queue_list_page_url.get()
            self.parse_list(url)

class mysql_queue(threading.Thread):
    conn = pymysql.connect(user='root', port=3306, password='123456', db='steam', charset='utf8')
    cur = conn.cursor()
    alock = threading.Lock()
    def __init__(self, queue_list_page_url, queue_mysql,*args, **kwargs):
        super(mysql_queue, self).__init__(*args, **kwargs)
        self.queue_list_page_url = queue_list_page_url
        self.queue_mysql = queue_mysql
    def run(self):
        while True:
            game_id, game_name, game_price, game_tag = self.queue_mysql.get()
            self.alock.acquire()
            self.insert_data(game_id, game_name, game_price, game_tag)
            print('插入成功{}'.format(game_name))
            self.alock.release()
    def insert_data(self,*args):
        insert_data_sql = 'insert into game_info(game_id,game_name,game_price,game_tag) values (%s,%s,%s,%s)'
        try:
            self.cur.execute(insert_data_sql,*args)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()



# 详情页解析
class detil_page(threading.Thread):
    pass

def main():
    queue_stagid = Queue(500)
    queue_list_page_url = Queue(3000)
    queue_mysql = Queue(2000)
    stagid_list(queue_stagid)
    for i in range(2):
        t = product_list_url(queue_list_page_url,queue_stagid)
        t.start()
    for i in range(5):
        t = consumer(queue_list_page_url,queue_mysql)
        t.start()
    for i in range(3):
        t = mysql_queue(queue_list_page_url, queue_mysql)
        t.start()

if __name__ == '__main__':
    main()
    # for i in range(5):
    #     t = consumer(queue_list_page_url,queue_mysql)
    #     t.start()
    # for i in range(5):
    #     t = mysql_queue(queue_list_page_url,queue_mysql)
    #     t.start()


