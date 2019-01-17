import re
import requests
import xml.dom.minidom
import os
import threading

import Page
import  Database
import utils


class DetailFetcher:
    def __init__(self, gadio):
        self.gadio = gadio
        self.bs = Page.Page(self.gadio.link).get_bs()
        pass

    def fetch_hl_img_link(self):
        img_link = self.bs.find('div', class_='swiper-wrapper').find('img', class_='img-responsive').get('src')
        re1 = r'(.*?)\?'
        rg = re.compile(re1, re.IGNORECASE | re.DOTALL)
        m = rg.findall(img_link)[0]
        return m

    def fetch_djs(self):
        djs = list(map(lambda tag: utils.get_fullname(tag),
                       self.bs.find('div', class_='story_djs_items').find_all('a')))
        return djs

    def fetch_audio_url(self):
        audio_url = self.bs.find('p', class_='story_actions').contents[1].get('href')
        return audio_url

    def fetch_timeline(self, high_res_flag=True):
        timeline = []
        timeline_dots = self.bs.find_all('div', class_='swiper-slide')[1:]
        for dot in timeline_dots:
            left_img_link = dot.find('div', class_='col-xs-5').find('img').get('src')
            if high_res_flag:
                left_img_link = left_img_link.replace('_limit', '')

            right_content = dot.find('div', class_='col-xs-7')
            title = right_content.find('h1', class_='audio_dot_titile').contents[0].strip()
            timestamp = int(right_content.find('h1', class_='audio_dot_titile').find('a').get('data-at'))
            text_content = right_content.find_all('p')
            text = text_content[0].get_text()
            if len(text_content) == 2:
                ref_link = text_content[1].find('a').get('href')
            else:
                ref_link = None
            timeline.append([left_img_link, title, text, ref_link, timestamp])
        return timeline

    def fetch_story(self):
        pass

    def download_timeline_xml(self, path):
        doc = xml.dom.minidom.Document()
        root_token = doc.createElement('gadio')
        doc.appendChild(root_token)

        # Write title token
        title_token = doc.createElement('title')
        root_token.appendChild(title_token)
        title_token.appendChild(doc.createTextNode(self.gadio.title))

        # Write date token
        date_token = doc.createElement('date')
        root_token.appendChild(date_token)
        date_token.appendChild(doc.createTextNode(self.gadio.date))

        # Write DJs token
        djs_token = doc.createElement('DJs')
        root_token.appendChild(djs_token)
        djs = self.fetch_djs()
        for dj in djs:
            djs_token.appendChild(doc.createTextNode(dj))

        # Write timeline token
        timeline_token = doc.createElement('timeline')
        root_token.appendChild(timeline_token)
        timeline = self.fetch_timeline()
        for timedot in timeline:
            # Init timedot token
            timedot_token = doc.createElement('timedot')
            timeline_token.appendChild(timedot_token)

            # Create timedot_title token
            timedot_title_token = doc.createElement('timedot_title')
            timedot_token.appendChild(timedot_title_token)
            timedot_title_token.appendChild(doc.createTextNode(timedot[1]))

            # Create timedot_content token
            timedot_content_token = doc.createElement('timedot_content')
            timedot_token.appendChild(timedot_content_token)
            timedot_content_token.appendChild(doc.createTextNode(timedot[2]))

            timedot_ref_link_token = doc.createElement('timedot_reflink')
            timedot_token.appendChild(timedot_ref_link_token)
            if timedot[3] is not None:
                timedot_ref_link_token.appendChild(doc.createTextNode(timedot[3]))
            else:
                timedot_ref_link_token.appendChild(doc.createTextNode(''))

            timedot_time_token = doc.createElement('timedoc_sec')
            timedot_token.appendChild(timedot_time_token)
            timedot_time_token.appendChild(doc.createTextNode(str(timedot[4])))

        with open(os.path.join(path, 'timeline.xml'), 'w', encoding='utf-8') as f:
            f.write(doc.toprettyxml(indent='    '))

    def download_imgs(self, path):
        threads = []
        folder = os.path.join(path, 'img')
        if not os.path.exists(folder):
            os.makedirs(folder)

        headline_img = self.fetch_hl_img_link()
        for idx, timedot in enumerate(self.fetch_timeline()):
            img_url = timedot[0]
            img_extension = img_url.split('.')[-1]
            if img_url is not None:
                dst_path = os.path.join(folder, '%d.%s' % (idx, img_extension))
                t = threading.Thread(target=self.__download_item, args=(img_url, dst_path))
                threads.append(t)

        for i in threads:
            i.start()
        for i in threads:
            i.join()

    @staticmethod
    def __download_item(url, path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)

    def download(self, path='../download', dl_timeline_flag=True):
        audio_url = self.fetch_audio_url()
        series = (self.gadio.series + '_' + self.gadio.vol).replace(' ', '_')
        title = self.gadio.title.replace(' ', '_')
        date = self.gadio.date.replace('-', '')
        folder = os.path.join(path, '%s_%s_%s' % (date, series, title))

        # Make dir for download
        if not os.path.exists(folder):
            os.makedirs(folder)

        print('Start downloading %s' % title)
        # Download timeline
        if dl_timeline_flag:
            print('Downloading timeline.')
            self.download_timeline_xml(folder)
            self.download_imgs(folder)

        # Download audio content
        print('Downloading audio content.')
        extension = audio_url.split('.')[-1]
        filename = '%s_%s_%s.%s' % (series, title, date, extension)
        self.__download_item(audio_url, os.path.join(folder, filename))

if __name__ == '__main__':
    db = Database.Database()
    res = db.select_gadio('gadio', 'link=="https://www.gcores.com/radios/104397"')
    df = DetailFetcher(res[0])
    df.download()
    pass

