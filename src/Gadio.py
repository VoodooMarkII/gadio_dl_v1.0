class Gadio:
    def __init__(self, title, date, series, vol, intro, link, img_link):
        self.title = title
        self.date = date
        self.series = series
        self.vol = vol
        self.intro = intro
        self.link = link
        self.img_link = img_link

    def get_brief(self):
        #dst = {'title': self.title, 'date': self.date, 'series': self.series, 'vol': self.vol, 'intro': self.intro,
        #       'link': self.link, 'img_link': self.img_link}
        dst = (self.title,self.date,self.series,self.vol,self.intro,self.link,self.img_link)
        return dst

    def get_detailed(self):
        pass
