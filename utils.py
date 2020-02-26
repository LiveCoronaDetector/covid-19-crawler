"""자주 사용하용하는 공용 함수"""

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
