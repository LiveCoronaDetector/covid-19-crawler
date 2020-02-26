"""각 사이트의 확진환자수, 격리해제수, 사망자수 크롤링 함수들"""
# -*- coding:utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup
from utils import save_json, load_json


def postprocess(cc, recovered, dead):
    """크롤링 한 환자수 후처리

    Args:
        cc: 확진환자수 크롤링한 결과
        recovered: 격리해제수 크롤링한 결과
        dead: 사망자수 크롤링한 결과

    Returns:
        후처리된 결과
    """
    cc = cc.replace(',', '').strip()
    recovered = recovered.replace(',', '').strip()
    dead = dead.replace(',', '').strip()

    if cc:
        cc = int(cc)
    if recovered:
        recovered = int(recovered)
    if dead:
        dead = int(dead)

    return cc, recovered, dead


def KCDC():
    """질병관리본부에서 국내 확진환자수, 격리해제수, 사망자수 크롤링

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


def worldOmeter():
    """worldOmeter에서 세계 확진환자수, 격리해제수, 사망자수 크롤링

    크롤링 한 결과를 worldmarker.js애 저장

    Returns:
        (int) cc: 국내 확진환자수
        (int) recoverd: 국내 격리해제수
        (int) dead: 국내 사망자수
    """
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select("#table3 > tbody > tr")

    worldmarker = load_json("./worldmarker.json")

    # 가지고 있던 데이터인지 확인하기 위해
    cr_cuntries = []
    for wma in worldmarker:
        cr_cuntries.extend(wma["Name_cr"])

    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        cc = datum.find_all("td")[1].text.strip()
        dead = datum.find_all("td")[3].text.strip()
        recovered = datum.find_all("td")[5].text.strip()
        cc, recovered, dead = postprocess(cc, recovered, dead)

        if country not in cr_cuntries:
            new = {
                "Name_cr": [country],
                "확진자수": cc,
                "사망자수": dead,
                "완치자수": recovered
            }
            worldmarker.append(new)
        else:
            for wm in worldmarker:
                if country in wm["Name_cr"]:
                    wm["확진자수"] = cc
                    wm["사망자수"] = recovered
                    wm["완치자수"] = dead

                    if "S. Korea" in wm["Name_cr"]:
                        korea = wm

    save_json(worldmarker, "./worldmarker.json")
    save_json(worldmarker, "./worldmarker.js")

    cc = korea["확진자수"]
    recovered = korea["사망자수"]
    dead = korea["완치자수"]
    return [cc, recovered, dead]


def namuWiki():
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
    """[KCDC, worldOmeter, namuWiki] 사이트의 확진환자수, 격리해제수, 사망자수 크롤링

    Returns:
        (dict) 각 사이트에서 취합한 확진환자수, 격리해제수, 사망자수
    """
    crawl_func_list = [KCDC, worldOmeter, namuWiki]
    data = {"domesticConfirmed": 0, "domesticRecovered": 0, "domesticDead": 0}

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

    data["domesticConfirmed"] = base[0]
    data["domesticRecovered"] = base[1]
    data["domesticDead"] = base[2]

    if data["domesticConfirmed"] == 0:
        return False
    return data


if __name__ == "__main__":
    print(main())
