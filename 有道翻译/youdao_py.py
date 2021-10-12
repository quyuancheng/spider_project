#coding:utf-8
import requests
import hashlib
import time
import random


class Youdao(object):
    def __init__(self,word):
        self.url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-676104602@10.108.160.100; JSESSIONID=aaac40qHRBaDr_iGhSLUx; OUTFOX_SEARCH_USER_ID_NCOO=696608045.4734024; fanyi-ad-id=115021; fanyi-ad-closed=1; ___rl__test__cookies=1630572993167',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https: // fanyi.youdao.com /'
        }
        self.formdata = None
        self.word = word
    # 生成formdata
    def generate_formdata(self):
        word = self.word
        """
        1.分析表单中动态变化的参数(多次抓包对比)
        2.全局搜索动态参数的字段或者值
        3.找出对应实现的js代码,打断点分析
            ts: "" + (new Date).getTime(),
            salt: r + parseInt(10 * Math.random(), 10);
            sign: n.md5("fanyideskweb" + e + i + "Y2FYu%TNSbMCxc3t2u^XT") MD5 加密算法
         """
        # 4.将js代码转化为python代码实现
        # 获取字符串形式的时间戳
        lts = str(time.time()*1000)
        # 时间戳+随机数
        salt = lts + str(random.randint(1,9))
        # md5字符串加密32位
        tempstr = "fanyideskweb" + self.word + salt + "Y2FYu%TNSbMCxc3t2u^XT"
        md5 = hashlib.md5()
        md5.update(tempstr.encode())
        sign = md5.hexdigest()
        # 构造表单字典
        self.formdata = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': lts,
            'bv': '89e18957825871c419be045180c67d3b',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }
    def get_data(self):
        response = requests.post(url=self.url,headers=self.headers,data=self.formdata)
        return response.json()

    def run(self):
        # url
        # headers
        # formdata
        self.generate_formdata()
        # 发送请求,获取相应
        data = self.get_data()
        # 解析数据
        result = data['translateResult'][0][0]['tgt']
        print(result)
if __name__ == '__main__':
    word = input('请输入需要翻译的汉语:')
    Youdao = Youdao(word)
    Youdao.run()