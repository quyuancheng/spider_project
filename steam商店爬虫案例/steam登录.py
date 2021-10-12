import requests
import time
import execjs
def req_post(url,data):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Referer':'https://store.steampowered.com/login/?redir=news%2F%3Fsnr%3D1_4_4__12&redir_ssl=1&snr=1_2108_4__global-header'
    }
    session = requests.session()
    response = session.post(url=url,headers=headers,data=data)
    return response.json()
def get_key():
    get_key_url = 'https://store.steampowered.com/login/getrsakey/'
    donotcache = int(time.time()*1000)
    data = {
        'donotcache': donotcache,
        'username': '15139987701'
    }
    key_json = req_post(get_key_url,data)
    return key_json


def login():
    login_url  = 'https://store.steampowered.com/login/dologin/'
    keys = get_key()
    publickey_exp = keys['publickey_exp']
    publickey_mod = keys['publickey_mod']
    password = 'a62951269'
    node = execjs.get()
    ctx = node.compile(open('RSA.js', encoding='utf-8').read())
    funcName = "getpwd('{0}','{1}','{2}')".format(password,publickey_mod,publickey_exp)
    pwd = ctx.eval(funcName)
    print(pwd)

    login_data = {
        'donotcache': int(time.time()*1000),
        'password': pwd,
        'username': 'quyuancheng',
        'rsatimestamp':'478958600000',
        'remember_login': 'false'
    }
    response = req_post(url=login_url,data=login_data)
    print(response)




if __name__ == '__main__':
    login()
