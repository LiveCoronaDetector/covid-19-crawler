import requests
import os
import json
import time
import datetime
import CCCounter

logFilePath = os.path.dirname(os.path.abspath(__file__)) + "/log.txt"
slackUrlFilePath = os.path.dirname(os.path.abspath(__file__)) + "/slack.txt"
def needPush(newItem):
    lastItem = 0

    try:
        with open(logFilePath, "r") as f:
            lastItem = int(f.readline())
    except:
        pass
    print("last : ", lastItem, ", new : ", newItem)
    return newItem != lastItem

def saveData(newItem):
    with open(logFilePath, "w") as f:
        f.write(str(newItem))
    
def pushSlack(newItem):
    pushUrl = ""
    try:
        with open(slackUrlFilePath, "r") as f:
            pushUrl = f.readline()
    except:
        print("Failed to get webhook url.")
        return
    headers = {'Content-type': 'application/json; charset=utf-8'}
    data = {"text": "국내 확진자 : " + str(newItem)}
    
    try:
        print(data)
        requests.post(pushUrl, headers=headers, data=json.dumps(data))
        saveData(newItem)
    except:
        print("Failed to send message.")

if __name__ == '__main__':
    sleepInterval = 60 * 30
    while True:
        print(datetime.datetime.now())
        newItem = CCCounter.main()
        if needPush(newItem):
            pushSlack(newItem)
            
        time.sleep(sleepInterval)