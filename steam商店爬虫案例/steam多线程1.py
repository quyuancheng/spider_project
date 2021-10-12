import pymysql
import requests
from lxml import etree
from multiprocessing.dummy import Pool
import threading
import asyncio
import aiohttp

class Mysql_cli(object):
    rlock = threading.RLock()
    conn = pymysql.connect(user='root',port=3306,password='123456',db='steam',charset='utf8')
    cur = conn.cursor()
    def process(self,*args):
        insert_data_sql = 'insert into game_info(game_id,game_name,game_price,game_tag,game_url) values (%s,%s,%s,%s,%s)'
        try:
            # self.rlock.acquire()
            self.cur.execute(insert_data_sql,*args)
            self.conn.commit()
            # self.rlock.release()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()


class Steam_game(object):
    start_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start=0&count=15&cc=CN&l=schinese&v=4&tagid=19'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    sql = Mysql_cli()
    def get_tagid(self):
        resp = requests.get(url=self.start_url,headers=self.headers).json()
        rgSolrFacetCounts = resp['rgSolrFacetCounts'].keys()
        stagid_list = list(rgSolrFacetCounts)
        return stagid_list
    # 获取所有游戏列表url
    def game_list(self):
        stagid_list = self.get_tagid()
        game_url_list = []
        for stagid in stagid_list:
            try:
                start_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start=0&count=15&cc=CN&l=schinese&v=4&tagid={}'.format(stagid)
                start_resp = requests.get(url=start_url,headers=self.headers).json()
                # 获取对应分类的结果数
                total_count = start_resp['total_count']
                if start_resp['results_html'] != '':
                    start = 0
                    while start < total_count:
                        game_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start={}&count=15&cc=CN&l=schinese&v=4&tagid={}'.format(start,stagid)
                        start += 15
                        game_url_list.append(game_url)
                        print(game_url)
                    else:
                        print('此类型页面获取结束')
                else:
                    continue
            except Exception as e:
                print(e)
            #只看一个分类
            break
        return game_url_list

    def list_url_get(self,url):
        resp_json = requests.get(url=url,headers=self.headers).json()
        resp = resp_json
        result = resp['results_html'].strip()
        tree = etree.HTML(result)
        text = tree.xpath('.//a')
        for i in text:
            game_id = i.xpath('.//@data-ds-appid')[0]
            game_name = i.xpath('.//div[@class="tab_item_name"]/text()')[0]
            game_price = i.xpath('.//div[@class="discount_final_price"]/text()')
            if game_price == []:
                game_price= '暂无'
            else:
                game_price= game_price[0]
            game_tag = i.xpath('.//div[@class="tab_item_top_tags"]/span/text()')
            game_url = i.xpath('.//@href')[0]
            # game_info['game_id'] = game_id
            # game_info['game_name'] = game_name
            # game_info['game_price'] = game_price
            # game_info['game_url'] = game_url
            game_tag = ''.join(game_tag)
            game_info = (game_id,game_name,game_price,game_tag,game_url)
            print('正在添加---{}'.format(game_info))
            self.sql.process(game_info)


    def run(self):
        poor = Pool(5)
        game_url_list = self.game_list()
        poor.map(self.list_url_get,game_url_list)
        self.sql.close()

if __name__ == '__main__':
    Steam_game = Steam_game()
    Steam_game.run()
