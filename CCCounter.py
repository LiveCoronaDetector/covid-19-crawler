"""각 사이트의 확진환자수, 격리해제수, 사망자수 크롤링 함수들"""
# -*- coding:utf-8 -*-


import re
import requests
from bs4 import BeautifulSoup


def KCDC():
    """질병관리본부에서 확진환자수, 격리해제수, 사망자수 크롤링

    Returns:
        (int) cc : 확진환자수
        (int) recoverd : 격리해제수
        (int) dead : 사망자수
    """
    html = requests.get("http://ncov.mohw.go.kr/index_main.jsp").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select("div.co_cur > ul > li > a.num")
    regex = re.compile(r"\d[,\d]+")

    cc = int(regex.search(data[0].text).group().replace(',', ''))  # 확진환자수
    recovered = int(regex.search(data[1].text).group().replace(',', ''))  # 격리해제수
    dead = int(regex.search(data[2].text).group().replace(',', ''))  # 사망자수
    
    return [cc, recovered, dead]


def worldOmeter():
    """worldOmeter에서 확진환자수, 격리해제수, 사망자수 크롤링

    Returns:
        (int) cc : 확진환자수
        (int) recoverd : 격리해제수
        (int) dead : 사망자수
    """
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, "html.parser")
    data = soup.select("#table3 > tbody > tr")

    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        korea = ["S. Korea", "South Korea"]
        if country in korea:
            country_info = datum.find_all('td')
            cc = int(country_info[1].text.replace(',', ''))  # 확진환자수
            dead = int(country_info[3].text.replace(',', ''))  # 사망자수
            recovered = int(country_info[5].text.replace(',', ''))  # 격리해제수
            return [cc, recovered, dead]
    return None


def namuWiki():
    """나무위키에서 확진환자수, 격리해제수, 사망자수 크롤링

    Returns:
        (int) cc : 확진환자수
        (int) recoverd : 격리해제수
        (int) dead : 사망자수
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
            regex = re.compile(r"\d+")
            cc = int(regex.search(country_info[1].text).group().replace(',', ''))  # 확진환자수
            dead = int(country_info[2].text.replace(',', ''))  # 사망자수
            recovered = int(country_info[3].text.replace(',', ''))  # 격리해제수
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
    for func in crawl_func_list:
        datum = None
        # 크롤링이 실패할 경우 재시도
        for i in range(3):
            try:
                datum = func()
            except:  # TODO : 구체적인 exception 추가
                print("Retry..")

        print(f"from [{func.__name__}] : {datum}")
        for i in range(3):
            if (datum is not None) and (datum[i] is not None) and (base[i] < datum[i]):
                base[i] = datum[i]

    data["domesticConfirmed"] = base[0]
    data["domesticRecovered"] = base[1]
    data["domesticDead"] = base[2]

    if data["domesticConfirmed"] == 0:
        return False
    return data


if __name__ == "__main__":
    print(main())
