"""
제주특별자치도 보건서비스 현황 및 브리핑자료
http://www.jeju.go.kr/wel/healthCare/corona/coronaNotice.htm

Author: Eunhak Lee (@return0927)
"""
import re
import requests
from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
from datetime import datetime


# Preferences
url = "http://www.jeju.go.kr/wel/healthCare/corona/coronaNotice.htm?act=rss"

# Model


def parse():
    req = requests.get(url)
    soup = Soup(req.text, 'html.parser')

    title = getattr(soup.find("title"), 'text', 'Empty Title')
    description = getattr(soup.find('description'), 'text', 'Empty Description')
    items = []

    for elem in soup.findAll("item"):
        elem_title = getattr(elem.find("title"), 'text', '')
        # elem_link = getattr(elem.find("link"), 'text', '') -> TODO: soup load 시 item -> link 가 깨지는 이유 밝히기
        elem_link = re.findall(
            r'((http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)',
            elem.text)[-1][0]
        elem_description = getattr(elem.find("description"), 'text', '')
        elem_author = getattr(elem.find("author"), 'text', '')

        _bare_date = getattr(elem.find("pubdate"), 'text', '')
        elem_pubDate = datetime.strptime(_bare_date, "%a, %d %b %Y %H:%M:%S GMT")

        items.append({
            "title": elem_title,
            "link": elem_link,
            "description": elem_description,
            "pubDate": elem_pubDate,
            "author": elem_author
        })

    return {
        'title': title,
        'description': description,
        'items': items
    }


if __name__ == "__main__":
    parse()
