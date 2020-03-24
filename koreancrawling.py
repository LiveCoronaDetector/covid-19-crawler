import json
with open('koreacrawl.js', 'r', encoding='UTF-8-sig') as f:
    data = json.load(f)
import json
from datetime import date
today = date.today()
day = today.strftime(f"{today.month}/{today.day}")

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import pandas as pd

html = urlopen("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=")
source = html.read()
html.close()

soup = BeautifulSoup(source, 'lxml')
table = soup.find("div", class_ = "data_table mgt16")
tables2 = table.find_all("td")

num=[]
for i in range(0, len(tables2)) :
    a = tables2[i].get_text()
    num.append(a)

before_tot = data[len(data)-1][1]
today_tot = int(num[0].replace(',',''))
diff=today_tot - before_tot
death = int(num[3])
release = int(num[1].replace(',',''))

now = []
now.append(day)
now.append(today_tot)
now.append(diff)
now.append(death)
now.append(release)

if data[len(data)-1][0] == day :
    with open('koreacrawl.js', 'r') as f:
        data = json.load(f)
else : 
    data.append(now)

with open('koreacrawl.js', 'w', encoding='utf-8') as make_file:
    json.dump(data, make_file, indent="\t")
data
