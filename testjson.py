#-*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import json

def worldMeters():
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#table3 > tbody > tr')
    marker = [
    {
        "Name": "이집트",
        "Name_en": "Egypt",
        "Name_ch": "埃及",
        "lat": 30.0594838,
        "lng": 31.2234448,
        "확진자수": 1,
        "사망자수": 0,
        "추가날짜": "2/16"
    }, {
        "Name": "벨기에",
        "Name_en": "Belgium",
        "Name_ch": "比利时",
        "lat": 50.8550625,
        "lng": 4.3053503,
        "확진자수": 2,
        "사망자수": 0,
        "추가날짜": "2/5"
    }, {
        "Name": "스페인",
        "Name_en": "Spain",
        "Name_ch": "西班牙",
        "lat": 40.4378698,
        "lng": -3.8196189,
        "확진자수": 2,
        "사망자수": 0,
        "추가날짜": "2/2"
    }, {
        "Name": "스웨덴",
        "Name_en": "Sweden",
        "Name_ch": "瑞典语",
        "lat": 59.3260668,
        "lng": 17.8419725,
        "확진자수": 1,
        "사망자수": 0,
        "추가날짜": "2/2"
    }, {
        "Name": "이탈리아",
        "Name_en": "Italy",
        "Name_ch": "义大利",
        "lat": 41.902782,
        "lng": 12.496366,
        "확진자수": 3,
        "사망자수": 0,
        "추가날짜": "2/1"
    }, {
        "Name": "러시아",
        "Name_en": "Russia",
        "Name_ch": "俄罗斯",
        "lat": 55.751244,
        "lng": 37.618423,
        "확진자수": 2,
        "사망자수": 0,
        "완치자수": 2,
        "추가날짜": "2/1"
    }, {
        "Name": "캐나다",
        "Name_en": "Canada",
        "Name_ch": "加拿大",
        "lat": 54.7235693,
        "lng": -113.7164202,
        "확진자수": 7,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "미국",
        "Name_en": "USA",
        "Name_ch": "美国",
        "lat": 37.2757368,
        "lng": -104.6549972,
        "확진자수": 15,
        "사망자수": 0,
        "완치자수": 3
    }, {
        "Name": "핀란드",
        "Name_en": "Finland",
        "Name_ch": "芬兰",
        "lat": 60.1102086,
        "lng": 24.7378224,
        "확진자수": 1,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "프랑스",
        "Name_en": "France",
        "Name_ch": "法国",
        "lat": 46.1390503,
        "lng": -2.4346589,
        "확진자수": 11,
        "사망자수": 1,
        "완치자수": 2
    }, {
        "Name": "영국",
        "Name_en": "U.K.",
        "Name_ch": "英国",
        "lat": 51.509865,
        "lng": -0.118092,
        "확진자수": 9,
        "사망자수": 0,
        "추가날짜": "2/1",
        "완치자수": 1
    }, {
        "Name": "네팔",
        "Name_en": "Nepal",
        "Name_ch": "尼泊尔",
        "lat": 28.3838445,
        "lng": 81.8867804,
        "확진자수": 1,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "마카오",
        "Name_en": "Macao",
        "Name_ch": "澳门",
        "lat": 22.1619078,
        "lng": 113.5351333,
        "확진자수": 10,
        "사망자수": 0,
        "완치자수": 3
    }, {
        "Name": "홍콩",
        "Name_en": "Hong Kong",
        "Name_ch": "香港",
        "lat": 22.3529808,
        "lng": 113.9876162,
        "확진자수": 56,
        "사망자수": 1,
        "완치자수": 1
    }, {
        "Name": "태국",
        "Name_en": "Thailand",
        "Name_ch": "泰国",
        "lat": 13.0110763,
        "lng": 96.9952628,
        "확진자수": 34,
        "사망자수": 0,
        "완치자수": 12
    }, {
        "Name": "호주",
        "Name_en": "Australia",
        "Name_ch": "澳大利亚",
        "lat": -24.9936027,
        "lng": 115.2351577,
        "확진자수": 15,
        "사망자수": 0,
        "완치자수": 8
    }, {
        "Name": "싱가포르",
        "Name_en": "Singapore",
        "Name_ch": "新加坡",
        "lat": 1.3143394,
        "lng": 103.7041659,
        "확진자수": 72,
        "사망자수": 0,
        "완치자수": 15
    }, {
        "Name": "말레이시아",
        "Name_en": "Malaysia",
        "Name_ch": "马来西亚",
        "lat": 4.1389178,
        "lng": 105.1226078,
        "확진자수": 21,
        "사망자수": 0,
        "완치자수": 3
    }, {
        "Name": "캄보디아",
        "Name_en": "Cambodia",
        "Name_ch": "柬埔寨",
        "lat": 12.1458696,
        "lng": 103.8594161,
        "확진자수": 1,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "베트남",
        "Name_en": "Vietnam",
        "Name_ch": "越南",
        "lat": 15.7583637,
        "lng": 101.4157502,
        "확진자수": 16,
        "사망자수": 0,
        "완치자수": 7
    }, {
        "Name": "필리핀",
        "Name_en": "Philippines",
        "Name_ch": "菲律宾",
        "lat": 14.5965787,
        "lng": 120.9444545,
        "확진자수": 3,
        "사망자수": 1,
        "완치자수": 1
    }, {
        "Name": "대만",
        "Name_en": "Taiwan",
        "Name_ch": "台湾",
        "lat": 25.0174719,
        "lng": 121.3662943,
        "확진자수": 18,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "스리랑카",
        "Name_en": "Sri Lanka",
        "Name_ch": "斯里兰卡",
        "lat": 7.8589214,
        "lng": 79.5850432,
        "확진자수": 1,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "독일",
        "Name_en": "Germany",
        "Name_ch": "德国",
        "lat": 51.0968735,
        "lng": 5.9694438,
        "확진자수": 16,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "인도",
        "Name_en": "India",
        "Name_ch": "印度",
        "lat": 28.5274228,
        "lng": 77.1387735,
        "확진자수": 3,
        "사망자수": 0
    }, {
        "Name": "아랍에미리트",
        "Name_en": "U.A.E.",
        "Name_ch": "阿拉伯联合酋长国",
        "lat": 24.3870789,
        "lng": 54.4185368,
        "확진자수": 8,
        "사망자수": 0,
        "완치자수": 1
    }, {
        "Name": "중국",
        "Name_en": "China",
        "Name_ch": "中国",
        "lat": 39.9385466,
        "lng": 116.117281,
        "확진자수": 68500,
        "사망자수": 1665,
        "완치자수": 6900
    }, {
        "Name": "일본",
        "Name_en": "Japan",
        "Name_ch": "日本",
        "lat": 34.6777642,
        "lng": 135.4160247,
        "확진자수": 52,
        "사망자수": 1,
        "완치자수": 9
    }, {
        "Name": "일본크루즈",
        "Name_en": "Japan Cruise ship",
        "Name_ch": "日本 邮轮",
        "lat": 34.6777642,
        "lng": 135.4160247,
        "확진자수": 285,
        "사망자수": 0
    }, {
        "Name": "한국",
        "Name_en": "S. Korea",
        "Name_ch": "韩国",
        "lat": 37.5456299,
        "lng": 126.9540667,
        "확진자수": 29,
        "사망자수": 0,
        "완치자수": 9,
        "검사진행": 692,
    }]
    for d in datas:
        국가이름 = d.find_all('td')[0].text
        확진자 = d.find_all('td')[1].text
        사망자 = d.find_all('td')[3].text
        완치자 = d.find_all('td')[5].text
        # print(f'국가이름 : {국가이름}')
        # print(f'확진자 : {확진자}')
        # print(f'사망자 : {사망자}')
        # print(f'완치자 : {완치자}')
        for se in marker:
            if 국가이름.strip() == se["Name_en"]:
                se["확진자수"] = 확진자
                se["사망자수"] = 사망자
                se["완치자수"] = 완치자
        return marker

def main():
    datajson = worldMeters()
    datajson = json.dumps(datajson, indent=4, ensure_ascii=False)
    # print(datajson)
    with open('crawlerMarker.js', 'w', encoding='UTF-8-sig') as file:
        file.write(datajson)
    
    return datajson


if __name__ == '__main__':
    print(main())