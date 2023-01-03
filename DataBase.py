import json
from ftplib import FTP
import io


def xor(text, key):
    if len(text) > len(key):
        key = key*(len(text)//len(key)+1)
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(text, key)])


class DataBaseJson:
    def __init__(self, host, user, passwd):
        self.key = "fuhf234hsdkjfls234fsda4324ifg"
        self.host = host
        self.sessionFTP = FTP(host, user, passwd)
        try:
            self.update()
        except Exception as e:
            print(f"(data_base.py)Ошибка: ({e})")
            self.db = {"sessions": []}
            self.save()

    def get_duration(self, chat_id) -> int:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if "duration" in self.db[str(chat_id)]:
            return self.db[str(chat_id)]["duration"]
        else:
            return -1

    def set_duration(self, chat_id, duration: int):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]["duration"] = duration
        self.save()

    def set_nickname(self, chat_id, nickname: list):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]["nickname"] = nickname
        self.save()

    def get_nickname(self, chat_id) -> list:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if "nickname" in self.db[str(chat_id)]:
            return self.db[str(chat_id)]["nickname"]
        else:
            return []

    def set_session(self, chat_id, dictionary: dict):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]["session"] = dictionary
        self.save()

    def get_session(self, chat_id):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if "session" in self.db[str(chat_id)]:
            return self.db[str(chat_id)]["session"]
        else:
            return None

    def get_status(self, chat_id) -> str:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if "status" in self.db[str(chat_id)]:
            return self.db[str(chat_id)]["status"]
        else:
            return ""

    def set_status(self, chat_id, status):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]["status"] = status
        self.save()

    def update(self):
        bytes_stream = io.BytesIO(b'')
        self.sessionFTP.retrbinary('RETR ' + 'data.json', bytes_stream.write)
        bytes_stream.seek(0)
        data = xor(str(bytes_stream.read().decode("ascii")), self.key)
        self.db = json.loads(data)
        bytes_stream.close()

    def save(self):
        data = io.BytesIO(bytes(xor(json.dumps(self.db), self.key), "ascii"))
        self.sessionFTP.storbinary('STOR ' + 'data.json', data, 1024)
