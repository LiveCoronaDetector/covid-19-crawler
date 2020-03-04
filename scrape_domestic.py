# -*- coding:utf-8 -*-
"""국내 환자수 수집"""


import requests
from bs4 import BeautifulSoup
from utils import postprocess, load_json
from scrape_helper import push_scraping_msg, check_update


citydo = load_json("./_data.json")


def scrape_KCDC_citydo():
    """질병관리본부의 시도별 발생동향 수집"""
    request_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.3.902460717.1582188059; _gid=GA1.3.1299466237.1583138633; JSESSIONID=hUEn1QgHlDMNI2gSSZJxuN0zYGahJogaUyaeAEvgyXstvqyq4C13pOf4dNGoOdid.mohwwas1_servlet_engine40; NetFunnel_ID=; _gat_gtag_UA_26269343_2=1',
        'Host': 'ncov.mohw.go.kr',
        'Referer': 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=&fbclid=IwAR3NoNL_j1phitehSggDQedf7S165308xIEeG8ljACy-VRq-T5efcbcTK_s',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }

    session = requests.Session()
    session.max_redirects = 6000000
    html = session.get("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=", headers=request_headers)
    soup = BeautifulSoup(html.text, "html.parser")
    time = soup.select_one("p.info > span").text
    data = soup.select("table.num > tbody > tr")

    push = []
    new_data = {}
    for datum in data:
        name = datum.find("th").text
        number = datum.find_all("td")
        var_list = []
        for i in range(4):
            var_list.append(number[i].text)
        postproc = postprocess(var_list)
        new_data[name] = citydo.copy()
        new_data[name]["increasing"] = postproc[0]
        new_data[name]["cc_sum"] = postproc[1]
        new_data[name]["dead"] = postproc[2]
        new_data[name]["incidence"] = postproc[3]
        new_data[name]["time"] = time
        push.append((name, new_data[name]))
    push_scraping_msg("scrape_domestic.py >> scrape_KCDC_citydo()", push)
    return new_data


def scrape_seoul():
    """서울 발생 동향 수집"""
    html = requests.get("http://www.seoul.go.kr/coronaV/coronaStatus.do")
    soup = BeautifulSoup(html.text, "html.parser")
    time = soup.select_one("div.status-seoul > h4 > span").text
    var_list = [d.text for d in soup.find_all("p", class_="counter")[:7]]
    postproc = postprocess(var_list)

    # TODO: 수집한 데이터를 해당하는 키에 할당
    seoul = {}
    # seoul["increasing"] =
    seoul["cc_sum"] = postproc[0]
    # seoul["recovered"] =
    # seoul["dead"] =
    # seoul["incidence"] =
    seoul["time"] = time
    push_scraping_msg("scrape_domestic.py >> scrape_seoul()", [("서울", seoul)])
    return seoul


def scrape_jeju():
    """제주 발생 동향 수집"""
    # TODO: 코드 완성
    html = requests.get("https://jeju.go.kr/covid19.jsp")


def scrape_incheon():
    """인천 발생 동향 수집"""
    # TODO: 코드 완성
    html = requests.get("https://www.incheon.go.kr/health/HE020409")


def run_domestic():
    """전체 시도별 발생동향 수집 함수 실행

    각 사이트의 최신 버전을 _domestic.json에 저장
    """
    citydo_data = scrape_KCDC_citydo()

    seoul = scrape_seoul()
    if check_update(citydo_data["서울"]["time"], seoul["time"]):
        citydo_data["서울"].update(seoul)

    return citydo_data


if __name__ == "__main__":
    run_domestic()
