import requests
import re
from bs4 import BeautifulSoup

def KCDC():
    response = requests.get('http://ncov.mohw.go.kr/index_main.jsp').text
    soup = BeautifulSoup(response, 'html.parser')

    selector='body > div > div.container.main_container > div > div:nth-child(1) > div.co_cur > ul > li:nth-child(1) > a'
    data = soup.select(selector)
    data = str(data)
    cc = int(re.search(r'\d+', data).group())

    selector='body > div > div.container.main_container > div > div:nth-child(1) > div.co_cur > ul > li:nth-child(2) > a'
    data = soup.select(selector)
    data = str(data)
    recoverd = int(re.search(r'\d+', data).group())
    return cc, recoverd, 0

def worldMeters():
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#table3 > tbody > tr')
    for d in datas:
        label = d.find_all('td')[0].text
        cc = d.find_all('td')[1].text
        recovered = d.find_all('td')[5].text
        if label == ' South Korea' or label == ' S. Korea ' or label == 'South Korea':
            return int(cc), int(recovered), 0

def namu():
    html = requests.get('https://namu.wiki/w/%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D').text
    soup = BeautifulSoup(html, 'html.parser')
    selector = '#app > div > div:nth-child(2) > article > div:nth-child(5) > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(2) > table > tbody > tr'
    data = soup.select(selector)
    for row in data:
        if '대한민국' in str(row):
            data = row
            break
    soup = BeautifulSoup(str(data), 'html.parser')
    data = soup.select('.wiki-paragraph')

    cc = str(data[1])
    dead = str(data[2])
    recovered = str(data[3])

    cc = int(re.search(r'\d+', cc).group())
    dead = int(re.search(r'\d+', dead).group())
    recovered = int(re.search(r'\d+', recovered).group())


    return cc, recovered, dead

def doTry(function, t=3):
    for i in range(t): #Error Retry
        try :
            return function()
        except :
            print('Crawling Failed! Retry..')

def main():
    data = [0,0,0]

    tmp = doTry(KCDC)
    for i in range(3):
        if tmp[i] is not None:
            data[i]=tmp[i]
    tmp = doTry(worldMeters)
    for i in range(3):
        if tmp[i] is not None and data[i] == 0:
            data[i] = tmp[i]
    tmp = doTry(namu)
    for i in range(3):
        if tmp[i] is not None and data[i] == 0:
            data[i] = tmp[i]

    data = {'confirmed':data[0], 'recovered':data[1], 'dead':data[2]}
    if data['confirmed'] != 0:
       return data

    print('all attempt to get data failed.')
    return False


if __name__ == '__main__':
    print(main())