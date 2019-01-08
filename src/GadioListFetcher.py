import re

import Page
import Gadio


class GadioListFtecher:
    """
    Fetching the brief info of all gadio from gcores website.
    """
    def __init__(self, home_url='https://www.gcores.com/categories/9/originals'):
        """
        Init.

        :param home_url: The url of gadio category. Leave this parameter default.
        """
        self.home_url = home_url
        self.url_list = []
        self.__gadio_list = []

    def generate_gadio_list(self):
        # Find the index of last page.
        first_page = Page.Page(self.home_url).get_bs()
        link = first_page.find('a', text='末页').attrs['href']
        re1 = '(\\d+$)'
        rg = re.compile(re1, re.IGNORECASE | re.DOTALL)
        m = rg.search(link)
        if m:
            max_page_num = int(m.group(1))
        else:
            raise RuntimeError('Error occurs in finding maximum page num.')

        url_prefix = self.home_url + '?page='
        for page_num in range(1, max_page_num + 1):
            self.url_list.append(url_prefix + str(page_num))

        for url in self.url_list:
            page = Page.Page(url).get_bs()
            showcases = page.find_all('div', class_='showcase')
            for showcase in showcases:
                title = showcase.find('h4').get_text(strip=True)
                date = showcase.find('div', class_='showcase_time').contents[2].strip()

                series_n_vol = list(map(lambda x: x.strip(),
                                       showcase.find('div', class_='showcase_time').find('a').get_text(
                                           strip=True).split('\n')))
                if len(series_n_vol)>1:
                    series,vol = series_n_vol
                else:
                    series = series_n_vol[0]
                    vol= 'vol.0'
                intro = showcase.find('div', class_='showcase_info').get_text()
                link = showcase.find('div', class_='showcase_img').find('a').get('href')

                img_link = showcase.find('div', class_='showcase_img').find('img').get('src')
                re1 = r'(.*?)\?'
                rg = re.compile(re1, re.IGNORECASE | re.DOTALL)
                m = rg.findall(img_link)
                if m:
                    img_link = m[0]
                else:
                    img_link = None

                gadio = Gadio.Gadio(title=title, date=date, series=series, vol=vol, intro=intro, link=link,
                                    img_link=img_link)
                self.__gadio_list.append(gadio)
        return self.gadio_list

    @property
    def gadio_list(self):
        return self.__gadio_list


if __name__ == '__main__':
    glf = GadioListFtecher()
    l = glf.generate_gadio_list()
