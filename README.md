# Confirmed Case Counter
[코로나맵](http://livecorona.co.kr/) 사이트에 환자 수를 반영하기 위해 여러 사이트의 데이터를 가져옵니다.

<br>

## 수집하는 사이트

| 사이트 | 카테고리 | 수집하는 데이터 |
|---|---|---|
| [worldometer](https://www.worldometers.info/coronavirus/) | 세계 & 국내 | 확진자수, 격리해제수, 사망자수 |
| [질병관리본부](http://ncov.mohw.go.kr/index_main.jsp) | 국내 | 확진자수, 격리해제수, 사망자수 |
| [~~나무위키~~](https://namu.wiki/w/%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D) | ~~국내~~ | ~~확진자수, 격리해제수, 사망자수~~ |
| [질병관리본부 - 시도별 발생동향](http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=) | 국내 시도별 | 확진환자 증가, 확진환자 격리해제, 사망자수, 검사 중, 결과 음성 |
| [I SEOUL YOU - 코로나19](http://www.seoul.go.kr/coronaV/coronaStatus.do) | 서울 | 확진자수, 격리해제수, 사망자수 |

<br>

## Code Structure

| Path | Description
| :--- | :----------
| [CoronaCrawler](https://github.com/LiveCoronaDetector/CoronaCrawler) | Main folder
|&boxvr;&nbsp; [scraper_domestic.py](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/scraper_domestic.py) | 질병관리본부, 각 시도에서 운영하는 사이트에서 시도별 발생 동향 수집
|&boxvr;&nbsp; [scraper_korea.py](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/scraper_korea.py) | 질병관리본부, worldOmeter, namuWiki에서 **국내** 확진환자수, 격리해제수, 사망자수 수집
|&boxvr;&nbsp; [scraper_world.py](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/scraper_korea.py) | worldOmeter에서 **세계** 확진환자수, 격리해제수, 사망자수 수집 (대한민국 포함)
|&boxvr;&nbsp; [update_data.py](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/update_data.py) | 한국과 국내 각 시도별 환자 수가 바뀔 때 슬랙에 알림
|&boxvr;&nbsp; [utils.py](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/utils.py) | 자주 사용하는 공용 함수
|&boxvr;&nbsp; [_domestic.json](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/_domestic.json) | 국내 시도별 환자수 데이터
|&boxvr;&nbsp; [_world.json](https://github.com/LiveCoronaDetector/CoronaCrawler/blob/master/_domestic.json) | 세계 국가별 환자수 데이터
|&boxvr;&nbsp; [slack_update_url.txt]() | slack bot-alarm 채널 url (업데이트 확인용)
|&boxvr;&nbsp; [slack_test_url.txt]() | slack test-alarm 채널 url (개발 테스트용)

<br>

## requirements
```shell script
conda env create -f requirements.yaml
```
<br>

## TODO
* [ ] [크롤러 모니터링 고도화](https://github.com/LiveCoronaDetector/CoronaCrawler/issues/9)
* [ ] [페이지 정보 갱신 자동화](https://github.com/LiveCoronaDetector/CoronaCrawler/issues/8)
* [ ] `scraper_domestic.py`의 각 시도별 사이트 함수 완성