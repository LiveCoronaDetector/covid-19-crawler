# -*- coding:utf-8 -*-
"""데이터 수집에 필요한 함수들"""


import re
import json
import requests
from slack import WebClient
from utils import load_json


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


def push_scraping_msg(name, data):
    """크롤링한 데이터를 실시간으로 slack에 알림

    Args:
        (str) name: 모듈 이름, 함수 이름
        (list) data: 수집한 데이터 [(국가/시/도, 실제 수집한 데이터), ...]
    """
    webhook_url_path = "./slack_covidbot_url.txt"
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


def push_update_msg(push_list):
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

    data_desc = load_json("./_data_desc.json")
    content = ""
    for pl in push_list:
        content += "<{}>".format(pl[0])
        diffkeys = [k for k in pl[1] if k in pl[2] and pl[1][k] != pl[2][k]]
        for k in diffkeys:
            content += "\n{}({}): {} --> {}"\
                .format(data_desc[k], k, pl[1][k], pl[2][k])
        content += "\n\n"

    print(content)
    payload = {"text": "```" + content + "```"}

    requests.post(webhook_url,
                  data=json.dumps(payload),
                  headers={"Content-Type": "application/json"})


def push_file_msg(file_path):
    """서버에서 수집하는 환자수 데이터 파일을 슬랙에 메시지로 보냄

    Args:
        file_path: 메시지로 보낼 파일 경로
    """
    webhook_url_path = "./slack_covidbot_token.txt"
    token = None
    with open(webhook_url_path, "r") as f:
        token = f.readline()
    if token:
        client = WebClient(token=token)
        client.files_upload(channels="#dev-alarm",
                            title=file_path[2:],
                            file=file_path,
                            filetype="javascript")
