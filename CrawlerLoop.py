import requests
import os
import json
import time
import datetime
import CCCounter

logFilePath = os.path.dirname(os.path.abspath(__file__)) + "/log.txt"    
def needPush(newItem):
    lastItem = 0

    try:
        with open(logFilePath, "r") as f:
            lastItem = int(f.readline())
            f.close()
    except:
        pass
    print("last : ", lastItem, ", new : ", newItem)
    return newItem != lastItem

def saveData(newItem):
    with open(logFilePath, "w") as f:
        f.write(str(newItem))
        f.close()
    
def pushSlack(newItem):
    pushUrl = "https://hooks.slack.com/services/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"
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