from queue import Queue
import requests
from lxml import etree
import os
from urllib import request
import threading

class Procuder(threading.Thread):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            # 获取每一页Url
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)
    def parse_page(self,url):
        response = requests.get(url,headers=self.headers)
        html = etree.HTML(response.text)
        imgs = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            if alt == '':
                alt = "没名字"
            suffix = os.path.splitext(img_url)[1]
            filename = alt + suffix
            self.img_queue.put((img_url, filename))

class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, filename = self.img_queue.get()
            request.urlretrieve(img_url,'图片素材/'+filename)
            print(filename,"下载完成")

def main():
    page_queue = Queue(100)
    img_queue = Queue(5000)
    for i in range(1,101):
        url = 'https://www.doutula.com/photo/list/?page={}'.format(i)
        page_queue.put(url)
    for x in range(5):
        t = Procuder(page_queue,img_queue)
        t.start()
    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()
