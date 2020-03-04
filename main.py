# -*- coding:utf-8 -*-
"""한국과 국내 각 시도별 크롤러 실행"""


import time
import datetime
from utils import load_json, save_json
from scrape_helper import push_update_msg, push_file_msg
import scrape_korea
import scrape_domestic


world_path = "./_world.json"
domestic_path = "./_domestic.json"


def check_korea(old, new):
    """대한민국 데이터가 변했는지 체크

    데이터: 확진환자, 완치, 사망

    Args:
        old: _world.json의 S. Korea 데이터
        new: scraper_korea.py의 main() 함수 반환값 (새로 수집한 데이터)

    Returns:
        새로 업데이트 해야하는 경우: True
        새로 업데이트 하지 않아도 되는 경우: False
    """
    if new is None or old == new:
        return False
    return True


def check_domestic(old, new):
    """대한민국 데이터가 변했는지 체크

    데이터: 확진환자 증가, 확진환자 합계, 확진환자 중 격리중, 확진환자 중 격리해제, 확진환자 중 사망,
          검사현황 합계, 검사현황 검사중, 검사현황 중 결과음성, 총계, 업데이트 시간

    Args:
        old: _domestic.json의 각 시도별 데이터
        new: scraper_domestic.py의 main() 함수 반환값 (새로 수집한 데이터)

    Returns:
        새로 업데이트 해야하는 경우: True, 바뀐 데이터 list
        새로 업데이트 하지 않아도 되는 경우: False, None
    """
    update_list = []
    for key, value in new.items():
        if value == old[key]:
            continue
        update_list.append({key: value})
    if update_list:
        return True, update_list
    return False, None


def run_main():
    """전체 프로세스 실행"""
    sleep_interval = 60 * 15

    while True:
        print("\n##########################################################\n")
        print(datetime.datetime.now(), end="\n")

        push = []
        old_domestic = load_json(domestic_path)
        old_korea = old_domestic["대한민국"]
        old_korea["time"] = None

        print("\n================= <대한민국> 업데이트 중")
        new_korea = scrape_korea.run_korea()
        ko_check = check_korea(old_korea, new_korea)
        if ko_check:
            push.append(["대한민국", old_korea.copy(), new_korea])
            old_domestic["대한민국"].update(new_korea)

        print("\n================= <국내 시/도> 업데이트 중")
        new_domestic = scrape_domestic.run_domestic()
        do_check, up_list = check_domestic(old_domestic, new_domestic)
        if do_check:
            for ul in up_list:
                key = list(ul.keys())[0]
                push.append([key, old_domestic[key].copy(), ul[key]])
                old_domestic[key].update(ul[key])

        if ko_check or do_check:
            print("\n================= 데이터 업데이트 중")
            old_domestic["대한민국"]["time"] = str(datetime.datetime.now())
            save_json(old_domestic, domestic_path)
            push_update_msg(push)
            push_file_msg("./_domestic.json")

        print("\n##########################################################\n")
        time.sleep(sleep_interval)


if __name__ == '__main__':
    run_main()
