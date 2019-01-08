import bs4
import requests

class Page:
    def __init__(self,url, encoding='uft-8',header=None):
        if header is None:
            header = {'Referer': 'https://www.gcores.com',
                      'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) '
                      'AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.181Safari / 537.36'
                      }
        response = requests.get(url,header)
        response.encoding = encoding
        self.bs = bs4.BeautifulSoup(response.text,'html.parser')

    def get_bs(self):
        return self.bs

if __name__ == '__main__':
    page = Page('https://www.gcores.com/')
    pass