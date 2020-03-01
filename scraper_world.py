# -*- coding:utf-8 -*-
"""worldOmeter에서 세계 확진환자수, 격리해제수, 사망자수 수집"""


import time
import requests
from bs4 import BeautifulSoup
from utils import postprocess, load_json, push_scrape


def scrape_worldOmeter():
    """worldOmeter에서 세계 확진환자수, 격리해제수, 사망자수 크롤링"""
    html = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(html.text, "html.parser")
    data = soup.select("#main_table_countries > tbody > tr")
    world = load_json("./_world.json")

    push = []
    sum_cc, sum_dead, sum_recovered = 0, 0, 0
    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        cc = datum.find_all("td")[1].text.strip()
        dead = datum.find_all("td")[3].text.strip()
        recovered = datum.find_all("td")[5].text.strip()
        postproc = postprocess([cc, recovered, dead])
        cc, recovered, dead = postproc[0], postproc[1], postproc[2]

        if cc:
            sum_cc += cc
        if dead:
            sum_dead += dead
        if recovered:
            sum_recovered += recovered

        if country not in world.keys():  # 데이터가 없는 경우
            new = {"cc": cc, "dead": dead, "recovered": recovered}
            world[country] = new
        else:
            world[country]["cc"] = cc
            world[country]["recovered"] = recovered
            world[country]["dead"] = dead
        push.append((country, world[country]))
        time.sleep(0.2)

    push_scrape("scrape_world.py >> scrape_worldOmeter()", push)
    world["world"] = {}
    world["world"]["cc"] = sum_cc
    world["world"]["dead"] = sum_dead
    world["world"]["recovered"] = sum_recovered


if __name__ == "__main__":
    scrape_worldOmeter()
