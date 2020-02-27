"""질병관리본부, worldOmeter, namuWiki에서 국내 확진환자수, 격리해제수, 사망자수 수집

국내 데이터는 제외하고 수집
"""
# -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from utils import save_json, load_json, postprocess


def scrape_KCDC():
    """질병관리본부에서 국내 확진환자수, 격리해제수, 사망자수 수집

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("http://ncov.mohw.go.kr/index_main.jsp").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select("div.co_cur > ul > li > a.num")
    regex = re.compile(r"\d[,\d]+")
    cc = regex.search(data[0].text).group()
    recovered = regex.search(data[1].text).group()
    dead = regex.search(data[2].text).group()

    cc, recovered, dead = postprocess(cc, recovered, dead)
    return [cc, recovered, dead]


def scrape_worldOmeter():
    """worldOmeter에서 국내 확진환자수, 격리해제수, 사망자수 수집

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select("#table3 > tbody > tr")
    korea = ["S. Korea", "South Korea"]

    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        if country in korea:
            cc = datum.find_all("td")[1].text
            dead = datum.find_all("td")[3].text
            recovered = datum.find_all("td")[5].text
            cc, recovered, dead = postprocess(cc, recovered, dead)
            return [cc, recovered, dead]
    return None


def scrape_namuWiki():
    """나무위키에서 국내 확진환자수, 격리해제수, 사망자수 크롤링

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("https://namu.wiki/w/%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D").text
    soup = BeautifulSoup(html, "html.parser")
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
            cc, recovered, dead = postprocess(cc, recovered, dead)
            return [cc, recovered, dead]
    return None


def main():
    """[KCDC, worldOmeter, namuWiki] 사이트에서 국내  확진환자수, 격리해제수, 사망자수 수집

    수집 결과를 worldmarker.json에 저장

    Returns:
        (dict) 각 사이트에서 취합한 확진환자수, 격리해제수, 사망자수
    """
    crawl_func_list = [scrape_KCDC, scrape_worldOmeter, scrape_namuWiki]

    base = [0, 0, 0]
    datum = None
    for func in crawl_func_list:
        for i in range(3):  # 크롤링이 실패할 경우 재시도
            try:
                datum = func()
            except:  # TODO : 구체적인 exception 추가
                print("[{}] scraping retry..".format(func.__name__))

        print("from [{}] : {}".format(func.__name__, datum))
        for i in range(3):
            if (datum is not None) and (datum[i] is not None):
                if base[i] < datum[i]:
                    base[i] = datum[i]

    # worldmarker 업데이트
    worldmarker = load_json("./_worldmarker.json")
    korea = worldmarker["대한민국"]
    korea["확진자수"] = base[0]
    korea["완치자수"] = base[1]
    korea["사망자수"] = base[2]
    save_json(worldmarker, "./_worldmarker.json")

    # 데이터 반환
    data = {"domesticConfirmed": 0, "domesticRecovered": 0, "domesticDead": 0}
    data["domesticConfirmed"] = base[0]
    data["domesticRecovered"] = base[1]
    data["domesticDead"] = base[2]

    if data["domesticConfirmed"] == 0:
        return False
    return data


if __name__ == "__main__":
    print(main())
