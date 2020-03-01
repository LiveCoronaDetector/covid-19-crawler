# -*- coding:utf-8 -*-
"""대한민국 (+ 세계) 환자수 수집"""

import re
import time
import requests
from bs4 import BeautifulSoup
from utils import postprocess, save_json
from scrape_helper import push_scrape


patients = {"cc": None, "recovered": None, "dead": None}


# def scrape_namuWiki():
#     """나무위키에서 대한민국 확진환자수, 격리해제수, 사망자수 수집
#
#     Returns:
#         (dict) 한국의 세계 확진환자수(cc), 격리해제수(recovered), 사망자수(dead)
#     """
#     html = requests.get("https://namu.wiki/w/%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D")
#     soup = BeautifulSoup(html.text, "lxml")
#     table = soup.find("a", id=r's-3.2').parent.\
#         findNext("div", class_="wiki-heading-content").\
#         find("div", class_="wiki-table-wrap table-center").\
#         find("tbody")
#
#     data = table.find_all("tr")
#     for datum in data:
#         if "대한민국" in str(datum):
#             country_info = datum.find_all("div", class_="wiki-paragraph")
#             cc = country_info[1].text
#             dead = country_info[2].text
#             recovered = country_info[3].text
#             postproc = postprocess([cc, recovered, dead])
#             return_data = {"cc": postproc[0],
#                            "recovered": postproc[1],
#                            "dead": postproc[2]}
#             push_scrape("scraper_korea.py >> scrape_namuWiki()",
#                         [("대한민국", return_data)])
#             return return_data
#     push_scrape("scrape_korea.py >> scrape_namuWiki()",
#                 [("대한민국", None)])
#     return None


def scrape_worldOmeter(korea=True):
    """worldOmeter에서 세계 확진환자수, 격리해제수, 사망자수 수집

    Args:
        world: 대한민국 데이터만 수집하려면, True
               세계 데이터를 수집하려면, False

    Returns:
        (dict) 한국의 확진환자수(cc), 격리해제수(recovered), 사망자수(dead)
    """
    html = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(html.text, "html.parser")
    data = soup.select("#main_table_countries > tbody > tr")

    world_data = {}
    push = []
    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        cc = datum.find_all("td")[1].text.strip()
        recovered = datum.find_all("td")[6].text.strip()
        dead = datum.find_all("td")[3].text.strip()
        postproc = postprocess([cc, recovered, dead])
        cc, recovered, dead = postproc[0], postproc[1], postproc[2]

        if korea:
            if country != "S. Korea":
                continue
            korea_patients = patients.copy()
            korea_patients["cc"] = cc
            korea_patients["recovered"] = recovered
            korea_patients["dead"] = dead
            push.append(("S. Korea", korea_patients))
            push_scrape("scrape_korea.py >> scrape_worldOmeter()", push)
            return korea_patients

        world_data[country] = patients.copy()
        world_data[country]["cc"] = cc
        world_data[country]["recovered"] = recovered
        world_data[country]["dead"] = dead
        push.append((country, world_data[country]))
        time.sleep(0.2)

    push_scrape("scrape_korea.py >> scrape_worldOmeter()", push)
    save_json(world_data, "./_world.json")
    return world_data["S. Korea"]


def scrape_KCDC_korea():
    """KCDC에서 대한민국 확진환자수, 격리해제수, 사망자수 수집

    Returns:
        (dict) 한국의 세계 확진환자수(cc), 격리해제수(recovered), 사망자수(dead)
    """
    html = requests.get("http://ncov.mohw.go.kr/index_main.jsp")
    soup = BeautifulSoup(html.text, "lxml")
    data = soup.select("div.co_cur > ul > li > a.num")
    regex = re.compile(r"\d[,\d]+")
    cc = regex.search(data[0].text).group()
    recovered = regex.search(data[1].text).group()
    dead = regex.search(data[2].text).group()
    postproc = postprocess([cc, recovered, dead])
    return_data = {"cc": postproc[0],
                   "recovered": postproc[1],
                   "dead": postproc[2]}
    push_scrape("scrape_korea.py >> scrape_KCDC_korea()",
                [("대한민국", return_data)])
    return return_data


def run_korea():
    """사이트에서 수집한 대한민국 확진환자수, 격리해제수, 사망자수 취합
        사이트: KCDC, worldOmeter

    Returns:
        (dict) 각 사이트에서 취합한 대한민국 확진환자수, 격리해제수, 사망자수
    """
    func_list = [scrape_KCDC_korea, scrape_worldOmeter]
    base = {"cc": 0, "recovered": 0, "dead": 0}
    for func in func_list:
        datum = None
        for _ in range(3):
            try:
                datum = func()
            except Exception as e:  # TODO: 구채적인 error 처리
                print(e)
                print("[{}] scraping retry..".format(func.__name__))
            else:
                print("func [{}]: {}".format(func.__name__, datum))
                break

        for key in base.keys():
            if (datum is not None) and (datum[key] is not None):
                if base[key] < datum[key]:
                    base[key] = datum[key]
    return base


if __name__ == "__main__":
    run_korea()
