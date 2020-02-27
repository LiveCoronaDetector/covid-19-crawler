"""질병관리본부에서 시도별 발생 동향 수집"""
# -*- coding:utf-8 -*-


import requests
from bs4 import BeautifulSoup
from utils import save_json, load_json, postprocess


city_do = {"cc": None,  # 확진자
           "suspected": None,  # 의사환자
           "checking": None,  # 검사중
           "negative": None,  # 검사결과 (음성)
           "self": None,  # 자가격리자
           "monitoring": None,  # 감시중
           "unmonitor": None,  # 감시해제
           "dead": None,
           "time": None  # 업데이트 시간
           }


def scrape_seoul():
    """서울 발생 동향 수집

    _domestic.json에 업데이트
    """
    html = requests.get("http://www.seoul.go.kr/coronaV/coronaStatus.do").text
    soup = BeautifulSoup(html, "html.parser")
    time = soup.find("p", class_="top-text").text
    data = [datum.text for datum in soup.find_all("p", class_="counter")[:7]]
    cc, suspected, checking, negative, self, monitoring, unmonitor = data

    postresult = postprocess(cc, suspected, checking, negative, self,
                             monitoring, unmonitor)

    seoul = city_do.copy()
    seoul["cc"] = postresult[0]
    seoul["suspected"] = postresult[1]
    seoul["checking"] = postresult[2]
    seoul["negative"] = postresult[3]
    seoul["self"] = postresult[4]
    seoul["monitoring"] = postresult[5]
    seoul["unmonitor"] = postresult[6]
    seoul["time"] = time

    domestic = load_json("./_domestic.json")
    domestic["seoul"] = seoul
    save_json(domestic, "./_domestic.json")


def scrape_daegu():
    """대구 발생 동향 수집

    _domestic.json에 업데이트
    """
    html = requests.get("http://www.daegu.go.kr/").text
    soup = BeautifulSoup(html, "html.parser")
    time = soup.find("div", class_="con_l").text

    data = soup.find("div", class_="con_r").find_all("strong")
    cc, unmonitor, monitoring, dead = [datum.text[:-1] for datum in data]
    postresult = postprocess(cc, unmonitor, monitoring, dead)

    daegu = city_do.copy()
    daegu["cc"] = postresult[0]
    daegu["monitoring"] = postresult[2]
    daegu["unmonitor"] = postresult[1]
    daegu["dead"] = postresult[3]
    daegu["time"] = time

    domestic = load_json("./_domestic.json")
    domestic["daegu"] = daegu
    save_json(domestic, "./_domestic.json")


def scrape_jeju():
    """제주도 발생 동향 수집"""
    pass


def main():
    """전체 시도별 발생동향 수집 함수 실행"""
    scrape_seoul()
    scrape_daegu()


if __name__ == "__main__":
    main()
