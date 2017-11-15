import requests
from lxml import etree
import json


class NeteaseMusic(object):
    def __init__(self):
        self.url = 'http://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }
        self.proxies = {}
        self.index_f = open('player_list.json', 'w', encoding='utf-8')
        self.get_proxy()

    def get_proxy(self):
        try:
            proxy = requests.get('http://127.0.0.1:5010/get', timeout=5)
            self.proxies['http'] = 'http:{}'.format(proxy.text)
            self.proxies['https'] = 'https:{}'.format(proxy.text)
            print(self.proxies)
        except:
            self.get_proxy()

    def get_index(self, url):
        """
        获取网易云首页专辑数据
        :return: 
        """
        try:  # 如果请求超时,换代理重新请求
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=5)
            if response.status_code != 200:
                self.get_proxy()
                return self.get_index(url)
            else:
                html = response.content
                return html
        except:
            self.get_proxy()
            return self.get_index(url)

    def parse_index(self, html):
        html = etree.HTML(html.decode())
        player_list = html.xpath('//*[@id="m-pl-container"]/li/div[@class="u-cover u-cover-1"]')
        results = []
        for player in player_list:
            result = {}
            result['title'] = player.xpath('./a/@title')[0]
            result['href'] = 'http://music.163.com/#' + player.xpath('./a/@href')[0]
            result['count'] = player.xpath('./div/*[@class="nb"]/text()')[0]
            results.append(result)
            self.index_save(result)
            self.parse_index(result['href'])

        return results

    def index_save(self, result):
        str_result = json.dumps(result, ensure_ascii=False) + ',\n'
        self.index_f.write(str_result)

    def __del__(self):
        self.index_f.close()

    def parse_detail(self,url):
        html = self.get_index(url)
        html = etree.HTML(html) # 将返回的数据转化为element对象
        song_list= html.xpath('//div[@id="song-list-pre-cache"]/ul/li')

    def run(self):
        for i in range(38):
            url = self.url.format('全部', 35 * i)
            data = self.get_index(url)
            self.parse_index(data)
            print('第{}页保存完毕!'.format(i + 1))


if __name__ == '__main__':
    neteasemusic = NeteaseMusic()
    neteasemusic.run()
