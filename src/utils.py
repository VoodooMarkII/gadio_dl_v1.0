import Database
import Page


def get_fullname(tag):
    name = tag.get_text(strip=True)
    if name.endswith('...'):
        user_url = tag.get('href')
        bs = Page.Page(user_url).get_bs()
        name = bs.find('p', class_='user_name').get_text(strip=True)
    return name


def is_up_to_date():
    db = Database.Database()
    local_title = db.query_newest_title()
    page = Page.Page('https://www.gcores.com/categories/9/originals?page=1').get_bs()
    online_title = page.find('div', class_='showcase').find('h4').get_text(strip=True)
    return local_title == online_title


