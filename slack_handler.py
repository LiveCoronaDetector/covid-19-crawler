from singleton import Singleton
from utils import load_json
from slack import WebClient
import json
import requests

class SlackHandler(Singleton):
    message_scraping: str
    message_update: str
    scraping_url: str
    modification_url: str
    client: WebClient
    is_initialized = False
    
    def __init__(self):
        if self.is_initialized == False:
            webhook_url_path = "./slack_covidbot_url.txt"
            with open(webhook_url_path, "r") as f:
                self.scraping_url = f.readline()
                
            webhook_url_path = "./slack_update_url.txt"
            with open(webhook_url_path, "r") as f:
                self.modification_url = f.readline()
            self.data_desc = load_json("./_data_desc.json")
                
            self.message_scraping = "```"
            self.message_update = "```"
            
            webhook_url_path = "./slack_covidbot_token.txt"
            with open(webhook_url_path, "r") as f:
                self.token = f.readline()
                self.client = WebClient(token=self.token)
            self.is_initialized = True
    
    def add_scraping_msg(self, caller, data):
        """크롤링한 데이터를 실시간으로 slack에 알림

        Args:
            (str) caller: 모듈 이름, 함수 이름
            (list) data: 수집한 데이터 [(국가/시/도, 실제 수집한 데이터), ...]
        """
        self.message_scraping += f"==> {caller}\n\n"
        for datum in data:
            self.message_scraping += f"{datum[0]}\n{datum[1]}\n\n"
            
    def add_update_msg(self, push_list):
        """데이터를 업데이트 해야하는 경우 slack 알림

        Args:
            push_list: alram 보낼 list [[name, old, new], ...]
                        name: 대한민국 or 시도별 이름
                        old: 기존에 가지고 있던 데이터
                        new: 새로 업데이트 되는 데이터
        """
        for pl in push_list:
            self.message_update += f"<{pl[0]}>"
            diffkeys = [k for k in pl[1] if k in pl[2] and pl[1][k] != pl[2][k]]
            for k in diffkeys:
                self.message_update += f"\n{self.data_desc[k]}({k}): {pl[1][k]} --> {pl[2][k]}"
            self.message_update += ""
            
    def push_scraping_message(self):
        """크롤링 데이터 실시간 알림"""
        if self.message_scraping == "```":
            return
        payload = {"text": self.message_scraping + "```"}

        requests.post(self.scraping_url,
                      data=json.dumps(payload), 
                      headers={"Content-Type": "application/json"})
        self.message_scraping = "```"
                      
    def push_update_message(self):
        """데이터를 업데이트 해야하는 경우 slack 알림"""
        if self.message_update == "```":
            return
        payload = {"text": self.message_update + "```"}

        requests.post(self.modification_url,
                      data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})
        self.message_update = "```"

    def push_file_msg(self, file_path):
        """서버에서 수집하는 환자수 데이터 파일을 슬랙에 메시지로 보냄

        Args:
            file_path: 메시지로 보낼 파일 경로
        """
        if self.token:
            self.client.files_upload(channels="#dev-alarm",
                                title=file_path[2:],
                                file=file_path,
                                filetype="javascript")