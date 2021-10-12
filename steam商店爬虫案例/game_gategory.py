import requests
from lxml import etree
def category_game():
    url = 'https://store.steampowered.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers)
    tree = etree.HTML(response.text)
    divs = tree.xpath('.//div[@id="genre_flyout"]/div/div')
    title_list = []
    url_list = []
    for div in divs:
        titles = div.xpath('./a/text()|./a/span/text()|./div[@data-genre-group="action"]/a/text()|'
                           './div[@data-genre-group="adventure_and_casual"]/a/text()|'
                           './div[@data-genre-group="rpg"]/a/text()|'
                           './div[@data-genre-group="simulation"]/a/text()|'
                           './div[@data-genre-group="strategy"]/a/text()|'
                           './div[@data-genre-group="sports_and_racing"]/a/text()|'
                           './div[@data-genre-group="themes"]/a/text()|'
                           './div[@data-genre-group="social_and_players"]/a/text()')
        game_list_url = div.xpath('./a/@href|./a/span/@href|./div[@data-genre-group="action"]/a/@href|'
                                  './div[@data-genre-group="adventure_and_casual"]/a/@href|'
                                  './div[@data-genre-group="rpg"]/a/@href|'
                                  './div[@data-genre-group="simulation"]/a/@href|'
                                  './div[@data-genre-group="strategy"]/a/@href|'
                                  './div[@data-genre-group="sports_and_racing"]/a/@href|'
                                  './div[@data-genre-group="themes"]/a/@href|'
                                  './div[@data-genre-group="social_and_players"]/a/@href')
        for title in titles:
            title_list.append(title.strip())
        for url in game_list_url:
            url_list.append(url)
    title_list = [i for i in title_list if i != '']
    url_list = [i for i in url_list if i != '']
    dict1 = dict(zip(title_list,url_list))
    print(dict1)




category_game()