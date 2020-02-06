import requests
import re
from bs4 import BeautifulSoup

def KCDC():
    response = requests.get('http://ncov.mohw.go.kr/').text
    soup = BeautifulSoup(response, 'html.parser')
    data = soup.select('body > div > div.container.main_container > div > div:nth-child(1) > div.co_cur > ul > li:nth-child(1) > a')
    data = str(data)

    data = int(re.search(r'\d+', data).group())

    return data

def worldMeters():
    html = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select('#table3 > tbody > tr')
    for d in datas:
        label = d.find_all('td')[0].text
        data = d.find_all('td')[1].text
        if label == ' South Korea' or label == ' S. Korea ' or label == 'South Korea':
            return int(data)

def namu():
    html = requests.get('https://namu.wiki/edit/%EC%8B%A0%EC%A2%85%20%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4%EA%B0%90%EC%97%BC%EC%A6%9D?section=5').text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select('#app > div > div:nth-child(2) > article > div:nth-child(3) > form > div > div.a > textarea')

    data = str(data)
    data = re.search(r'[참조]\D+\d+[명]', data).group()
    data = int(re.search(r'\d+', data).group())

    return data

def doTry(function, t=3):
    for i in range(t): #Error Retry
        try :
            return function()
        except :
            print('Crawling Failed! Retry..')

def main():
    confirmed = 0

    confirmed = doTry(KCDC)
    if confirmed:
        return confirmed
    confirmed = doTry(worldMeters)
    if confirmed:
        return confirmed
    confirmed = doTry(namu)
    if confirmed:
        return confirmed
    print('all attempt to get CC data failed.')
    return False



if __name__ == '__main__':
    print(worldMeters())