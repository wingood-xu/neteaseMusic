import requests
from lxml import etree
import json
import time


class NeteaseMusic(object):
    def __init__(self):
        self.url = 'http://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }
        self.proxies = {}

        self.index_f = open('player_list.json', 'w', encoding='utf-8')

    def get_proxy(self):
        proxy = requests.get('http://127.0.0.1:5010/get/')
        self.proxies['http'] = 'http:{}'.format(proxy.text)
        self.proxies['https'] = 'https:{}'.format(proxy.text)
        print(self.proxies)
        return proxy.status_code

    def get_index(self,url):
        """
        获取网易云首页专辑数据
        :return: 
        """
        is_ok = self.get_proxy()
        if is_ok != 200:  # 获取代理,如果代理获取失败,则重新获取
            self.get_index(url)
        try:  # 如果请求超时,换代理重新请求
            response = requests.get(url, headers=self.headers, proxies=self.proxies)
            print(response.status_code)
            if response.status_code != 200:
                self.get_index(url)
            else:
                html = response.content
                # return html
                # print(etree.HTML(html))
                # data = etree.HTML(html)
                # print(data,11111111)
                return html
        except:
            self.get_index(url)

    def parse_index(self, html):
        print(type(html))
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

        return results

    def index_save(self, result):
        print('start_save')
        str_result = json.dumps(result,ensure_ascii=False)+',\n'
        self.index_f.write(str_result)

    def __del__(self):
        self.index_f.close()

    def get_detail(self):
        pass

    def parse_detail(self):
        pass

    def run(self):
        for i in range(38):
            url = self.url.format('全部',35*i)
            r = self.get_index(url)
            print(r)
            # while 1:
            #     try:
            # print('again')
            self.parse_index(r)
            # time.sleep(1)

        #     break
        # except:
        #     self.get_index(url)

if __name__ == '__main__':
    neteasemusic = NeteaseMusic()
    neteasemusic.run()
