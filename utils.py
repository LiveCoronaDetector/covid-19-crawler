# -*- coding:utf-8 -*-
"""자주 사용하는 공용 함수"""

import json
import requests


def save_json(data, path):
    """json으로 파일 저장

    Args:
        data: 저장할 데이터
        path: 저장할 경로
    """
    with open(path, "w", encoding="utf-8") as jf:
        json.dump(data, jf, indent="\t", ensure_ascii=False)


def load_json(path):
    """json 파일 load

    Args:
        path: 불러올 파일 경로

    Returns:
        불러온 데이터
    """
    with open(path, encoding="utf-8-sig") as jf:
        data = json.load(jf)
    return data


def postprocess(var_list):
    """수집한 환자수 후처리

    Args:
        후처리 할 데이터
    Returns:
        후처리된 결과
    """
    result = []
    for var in var_list:
        var = var.replace(',', '').strip()
        if var:
            var = int(var)
        else:
            var = None
        result.append(var)
    return result


def push_scrape(name, data):
    """크롤링한 데이터를 실시간으로 slack에 알림

    Args:
        (str) name: 모듈 이름, 함수 이름
        (list) data: 수집한 데이터 [(국가/시/도, 실제 수집한 데이터), ...]
    """
    webhook_url_path = "./slack_test_url.txt"
    webhook_url = None
    with open(webhook_url_path, "r") as f:
        webhook_url = f.readline()

    content = "==> {}".format(name)
    for datum in data:
        content += "\n\n{}\n{}".format(datum[0], datum[1])

    payload = {"text": "```" + content + "```"}

    requests.post(webhook_url,
                  data=json.dumps(payload),
                  headers={"Content-Type": "application/json"})


def push_update(push_list):
    """데이터를 업데이트 해야하는 경우 slack 알림

    Args:
        push_list: alram 보낼 list [[name, old, new], ...]
                    name: 대한민국 or 시도별 이름
                    old: 기존에 가지고 있던 데이터
                    new: 새로 업데이트 되는 데이터

    """
    webhook_url_path = "./slack_update_url.txt"
    webhook_url = None
    with open(webhook_url_path, "r") as f:
        webhook_url = f.readline()

    content = ""
    for pl in push_list:
        content += "<{}>".format(pl[0])
        for k in pl[1].keys():
            content += "\n {}: {} --> {}".format(k, pl[1][k], pl[2][k])
        content += "\n\n"

    print(content)
    payload = {"text": "```" + content + "```"}

    requests.post(webhook_url,
                  data=json.dumps(payload),
                  headers={"Content-Type": "application/json"})
