# -*- coding:utf-8 -*-
"""질병관리본부, worldOmeter, namuWiki에서 국내 확진환자수, 격리해제수, 사망자수 수집"""


import re
import requests
from bs4 import BeautifulSoup
from utils import postprocess, push_scrape


def scrape_KCDC():
    """질병관리본부에서 국내 확진환자수, 격리해제수, 사망자수 수집

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("http://ncov.mohw.go.kr/index_main.jsp")
    soup = BeautifulSoup(html.text, "lxml")
    data = soup.select("div.co_cur > ul > li > a.num")
    regex = re.compile(r"\d[,\d]+")
    cc = regex.search(data[0].text).group()
    recovered = regex.search(data[1].text).group()
    dead = regex.search(data[2].text).group()

    postproc = postprocess([cc, recovered, dead])
    cc, recovered, dead = postproc[0], postproc[1], postproc[2]
    return_data = [cc, recovered, dead]
    push_scrape("scraper_korea.py >> scrape_KCDC()", [("대한민국", return_data)])
    return return_data


def scrape_worldOmeter():
    """worldOmeter에서 국내 확진환자수, 격리해제수, 사망자수 수집

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(html.text, "lxml")
    data = soup.select("#main_table_countries > tbody > tr")
    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        if country == "S. Korea":
            cc = datum.find_all("td")[1].text
            dead = datum.find_all("td")[3].text
            recovered = datum.find_all("td")[6].text
            postproc = postprocess([cc, recovered, dead])
            cc, recovered, dead = postproc[0], postproc[1], postproc[2]
            return_data = [cc, recovered, dead]
            push_scrape("scraper_korea.py >> scrape_worldOmeter()",
                        [("대한민국", return_data)])
            return return_data
    push_scrape("scraper_korea.py >> scrape_worldOmeter()", [("대한민국", None)])
    return None


def scrape_namuWiki():
    """나무위키에서 국내 확진환자수, 격리해제수, 사망자수 크롤링

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("https://namu.wiki/w/%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D")
    soup = BeautifulSoup(html.text, "lxml")
    table = soup.find("a", id=r's-3.2').parent.\
        findNext("div", class_="wiki-heading-content").\
        find("div", class_="wiki-table-wrap table-center").\
        find("tbody")

    data = table.find_all("tr")
    for datum in data:
        if "대한민국" in str(datum):
            country_info = datum.find_all("div", class_="wiki-paragraph")
            cc = country_info[1].text
            dead = country_info[2].text
            recovered = country_info[3].text
            postproc = postprocess([cc, recovered, dead])
            cc, recovered, dead = postproc[0], postproc[1], postproc[2]
            return_data = [cc, recovered, dead]
            push_scrape("scraper_korea.py >> scrape_namuWiki()",
                        [("대한민국", return_data)])
            return return_data
    push_scrape("scraper_korea.py >> scrape_namuWiki()", [("대한민국", None)])
    return None


def main():
    """[KCDC, worldOmeter, namuWiki] 사이트에서 국내  확진환자수, 격리해제수, 사망자수 수집

    Returns:
        (dict) 각 사이트에서 취합한 확진환자수, 격리해제수, 사망자수
    """
    crawl_func_list = [scrape_KCDC, scrape_worldOmeter]
    base = [0, 0, 0]
    for func in crawl_func_list:
        datum = None
        for _ in range(3):
            try:
                datum = func()
            except Exception as e:  # TODO: 구채적인 error 처리
                print(e)
                print("[{}] scraping retry..".format(func.__name__))
            else:
                print("from [{}] : {}".format(func.__name__, datum))
                break

        for i in range(3):
            if (datum is not None) and (datum[i] is not None):
                if base[i] < datum[i]:
                    base[i] = datum[i]

    # 데이터 반환
    data = {"cc": 0, "recovered": 0, "dead": 0}
    data["cc"] = base[0]
    data["recovered"] = base[1]
    data["dead"] = base[2]

    if data["cc"] == 0:
        return None
    return data


if __name__ == "__main__":
    main()
