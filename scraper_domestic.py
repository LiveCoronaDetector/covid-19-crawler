# -*- coding:utf-8 -*-
"""질병관리본부, 각 시도에서 운영하는 사이트에서 시도별 발생 동향 수집"""


import re
import requests
from bs4 import BeautifulSoup
from utils import postprocess, push_scrape


city_do = {"increasing": None,  # 확진환자 증가
           "cc_sum": None,  # 확진환자 합계
           "isolating": None,  # 확진환자 중 격리중
           "recovered": None,  # 확진환자 중 격리해제
           "dead": None,  # 확진환자 중 사망
           "ch_sum": None,  # 검사현황 합계
           "ch_examined": None,  # 검사현황 검사중
           "ch_negative": None,  # 검사현황 중 결과음성
           "total": None,  # 총계
           "time": None
           }


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
    # seoul["isolating"] =
    # seoul["recovered"] =
    # seoul["dead"] =
    # seoul["ch_sum"] =
    # seoul["ch_examined"] =
    # seoul["ch_negative"] =
    # seoul["total"] =
    seoul["time"] = time
    push_scrape("scraper_domestic.py >> scrape_seoul()", [("서울", seoul)])
    return seoul


def scrape_jeju():
    """TODO: https://jeju.go.kr/covid19.jsp 수집"""
    pass


def scrape_city_do_KCDC():
    """질병관리본부의 시도별 발생동향 수집"""
    html = requests.get("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=&fbclid=IwAR3NoNL_j1phitehSggDQedf7S165308xIEeG8ljACy-VRq-T5efcbcTK_s")
    soup = BeautifulSoup(html.text, "html.parser")
    time = soup.select_one("p.info > span").text
    data = soup.select("table.num > tbody > tr")

    push = []
    new_data = {}
    for datum in data:
        name = datum.find("th").text
        number = datum.find_all("td")

        var_list = []
        for i in range(9):
            var_list.append(number[i].text)
        postproc = postprocess(var_list)

        new_data[name] = city_do.copy()
        new_data[name]["increasing"] = postproc[0]
        new_data[name]["cc_sum"] = postproc[1]
        new_data[name]["isolating"] = postproc[2]
        new_data[name]["recovered"] = postproc[3]
        new_data[name]["dead"] = postproc[4]
        new_data[name]["ch_sum"] = postproc[5]
        new_data[name]["ch_examined"] = postproc[6]
        new_data[name]["ch_negative"] = postproc[7]
        new_data[name]["total"] = postproc[8]
        new_data[name]["time"] = time
        push.append((name, new_data[name]))
    push_scrape("scraper_domestic.py >> scrape_city_do_KCDC()", push)
    return new_data


def check_update(old_time, new_time):
    """시간을 비교해서 업데이트 해야할지, 말아야할지 결정

    Args:
        old_time: kcdc 업데이트 날짜와 시간
        new_time: 각 사이트 업데이트 날짜와 시간

    Returns:
        새로 업데이트 해야한다면 True, 아니라면 False
    """
    def check_time(time_list):
        if time_list[0] not in ["2020", "20"]:
            time_list.insert(0, "20")
        if len(time_list[0]) == 4:
            time_list[0] = time_list[0][:2]
        for i in range(1, len(time_list)):
            if len(time_list[i]) == 1:
                time_list[i] = "0" + time_list[i]
        if time_list[-1] == "00":
            time_list.pop()
        return time_list

    regex = re.compile(r"\d+")
    old_time_txt = check_time(regex.findall(old_time))
    new_time_txt = check_time(regex.findall(new_time))
    old_time_num = ''.join(old_time_txt)
    new_time_num = ''.join(new_time_txt)

    if old_time_num >= new_time_num:
        return False
    return True


def main():
    """전체 시도별 발생동향 수집 함수 실행

    각 사이트의 최신 버전을 _domestic.json에 저장
    """
    kcdc = scrape_city_do_KCDC()

    seoul = scrape_seoul()
    if check_update(kcdc["서울"]["time"], seoul["time"]):
        kcdc["서울"].update(seoul)

    return kcdc


if __name__ == "__main__":
    main()
