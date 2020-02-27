"""질병관리본부, worldOmeter, namuWiki에서 세계 확진환자수, 격리해제수, 사망자수 수집"""
# -*- coding:utf-8 -*-


import requests
from bs4 import BeautifulSoup
from utils import postprocess, save_json, load_json


def scrape_worldOmeter():
    """worldOmeter에서 세계 확진환자수, 격리해제수, 사망자수 크롤링

    크롤링 한 결과를 worldmarker.json애 저장
    """
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select("#table3 > tbody > tr")

    worldmarker = load_json("./_worldmarker.json")

    # 가지고 있던 데이터인지 확인하기 위해
    cr_cuntries = []
    for wma in worldmarker.values():
        cr_cuntries.extend(wma["Name_cr"])

    korea = ["S. Korea"]
    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        if country in korea:
            continue
        cc = datum.find_all("td")[1].text.strip()
        dead = datum.find_all("td")[3].text.strip()
        recovered = datum.find_all("td")[5].text.strip()
        cc, recovered, dead = postprocess(cc, recovered, dead)

        if country not in cr_cuntries:  # 데이터가 없는 경우
            new = {
                "Name_cr": [country],
                "확진자수": cc,
                "사망자수": dead,
                "완치자수": recovered
            }
            worldmarker[country] = new
        else:
            for wm in worldmarker.values():
                if country in wm["Name_cr"]:
                    wm["확진자수"] = cc
                    wm["사망자수"] = recovered
                    wm["완치자수"] = dead

    save_json(worldmarker, "./_worldmarker.json")


if __name__ == "__main__":
    scrape_worldOmeter()
