class DataBaseJsonBot:
    def __init__(self):
        self.db = {"sessions": []}

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

    def set_nickname(self, chat_id, nickname: list):
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        self.db[str(chat_id)]['nickname'] = nickname

    def get_nickname(self, chat_id) -> list:
        if str(chat_id) not in self.db:
            self.db[str(chat_id)] = {}
        if 'nickname' in self.db[str(chat_id)]:
            return self.db[str(chat_id)]['nickname']
        else:
            return []

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

