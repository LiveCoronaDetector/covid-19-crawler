# Confirmed Case Counter
신종 코로나 바이러스의 확진자 정보 업데이트가 질병관리본부(KCDC)의 언론 공개로 공유되고 있어, WHO
나 일부 사이트만을 이용하여 국내 확진자의 수를 정확히 파악하는 것에 어려움이 있습니다.

[코로나맵](http://livecorona.co.kr/) 사이트에 빠르게 확진자 수를 반영하기 위해, KCDC
와 여러 사이트에서 확진자 수를 크롤링하여 정확한 확진자 수를 반영합니다.

[KCDC](http://ncov.mohw.go.kr/index_main.jsp)에서의 크롤링이 실패해도, [worldometer
](https://www.worldometers.info/coronavirus/)
와 [나무위키](https://namu.wiki/w/%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D-19?from=%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D)의 확진자 데이터를 가져와 반영합니다.

<br>

## requirements
```shell script
conda env create -f requirements.yaml
```
<br>

## TODO

<br>

## Update note
- **2020.02.08**
    - 이제 크롤러가 KCDC, 나무위키, worldMeter 순으로 정보를 강화
    - 완치자, 사망자 정보도 수집
- **2020.02.25**
    - `CCCounter.py`에서 함수명 변경
        - `worldMeters()` → `worldOmeter()`
        - `namu()` → `namuWiki()`
    - `CCCounter.py`에 `doTry()` 삭제하고, `main()`에 코드로 삽임
    - `CCCounter.py`에 주석 추가 & 코드 정리