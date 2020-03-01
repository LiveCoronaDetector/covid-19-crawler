# -*- coding:utf-8 -*-
"""자주 사용하는 공용 함수"""


import json


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
