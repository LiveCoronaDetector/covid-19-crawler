# -*- coding:utf-8 -*-
"""데이터 수집에 필요한 함수들"""


import re
import json
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