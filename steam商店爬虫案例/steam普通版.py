import json
import requests
from lxml import etree
from multiprocessing.dummy import Pool
import asyncio
import aiohttp
class Steam_game(object):
    start_url = 'https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start=0&count=15&cc=CN&l=schinese&v=4&tagid=19'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
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
                    continue
            except:
                continue
            #只看一个分类
            # break
        return game_url_list

    # 异步对所有列表页url发请求
    # async def list_url_get(self,url):
    #     #     async with aiohttp.ClientSession as sess:
    #     #         async with await sess.get(url=url,headers=self.headers) as response:
    #     #             page_json = await response.text()
    #     #             return page_json
    def list_url_get(self,url):
        resp_json = requests.get(url=url,headers=self.headers).json()
    #     return resp_json
    # # 解析响应数据
    # def parse_page(self,resp_json):
        resp = resp_json
        result = resp['results_html'].strip()
        tree = etree.HTML(result)
        text = tree.xpath('.//a')
        for i in text:
            game_info = {}
            game_id = i.xpath('.//@data-ds-appid')[0]
            game_name = i.xpath('.//div[@class="tab_item_name"]/text()')[0]
            game_price = i.xpath('.//div[@class="discount_final_price"]/text()')
            if game_price == []:
                game_info['game_price'] = '暂无'
            else:
                game_info['game_price'] = game_price[0]
            game_tag = i.xpath('.//div[@class="tab_item_top_tags"]/span/text()')
            game_url = i.xpath('.//@href')[0]
            game_info['game_id'] = game_id
            game_info['game_name'] = game_name
            game_info['game_price'] = game_price
            game_info['game_tag'] = game_tag
            game_info['game_url'] = game_url
            print(game_info)
# 异步执行流程
#     def run(self):
#         game_url_list = self.game_list()
#         tasts = []
#         for url in game_url_list:
#             # 创建协程对象
#             c = self.list_url_get(url)
#             # 创建一个任务对象
#             task = asyncio.ensure_future(c)
#             # 绑定回调函数
#             task.add_done_callback(self.parse_page)
#             tasts.append(task)
#         # 创建事件循环对象
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(asyncio.wait(tasts))
    def run(self):
        poor = Pool(5)
        game_url_list = self.game_list()
        result_list = poor.map(self.list_url_get,game_url_list)
        print(result_list)



if __name__ == '__main__':
    Steam_game = Steam_game()
    Steam_game.run()