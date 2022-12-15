import json
from cryptocode import encrypt, decrypt
from ftplib import FTP
import urllib.request
from contextlib import closing
import requests

class DataBaseJson:
    def __init__(self, host, user, passwd):
        try:
            self.key = "fuhf234hsdkjfls234fsda4324ifg"
            self.host = host
            self.sessionFTP = FTP(host, user, passwd)
            self.update()
        except Exception as e:
            print(f'(data_base.py)Ошибка: ({e})')
            self.db = {"sessions": []}
            self.save()

    def get_duration(self, chat_id) -> int:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if 'duration' in self.db[str(chat_id)]:
            return self.db[str(chat_id)]['duration']
        else:
            return -1

    def set_duration(self, chat_id, duration: int):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]['duration'] = duration
        self.save()

    def set_nickname(self, chat_id, nickname: list):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]['nickname'] = nickname
        self.save()

    def get_nickname(self, chat_id) -> list:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if 'nickname' in self.db[str(chat_id)]:
            return self.db[str(chat_id)]['nickname']
        else:
            return []

    def set_session(self, chat_id, dictionary: dict):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]['session'] = dictionary
        self.save()

    def get_session(self, chat_id):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if 'session' in self.db[str(chat_id)]:
            return self.db[str(chat_id)]['session']
        else:
            return None

    def get_status(self, chat_id) -> str:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if 'status' in self.db[str(chat_id)]:
            return self.db[str(chat_id)]['status']
        else:
            return ''

    def set_status(self, chat_id, status):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]['status'] = status
        self.save()

    def update(self):
        with open('file', 'wb') as file:
            self.sessionFTP.retrbinary('RETR ' + 'data.json', file.write)
            file.close()
        with open('file', 'r') as file:
            self.db = json.loads(decrypt(file.read(), self.key))
            file.close()

    def save(self):
        with open("file", "w+") as file:
            file.write(encrypt(json.dumps(self.db), self.key))
            file.close()
        with open("file", "rb+") as file:
            self.sessionFTP.storbinary('STOR ' + 'data.json', file)
            file.close()

