from pyrogram import Client
import datetime
from pyrogram.raw.functions.auth import ResetAuthorizations
from opentele.api import API
import asyncio

class Session:
    pyrogram_str: str = ''
    valid: bool = False
    reg_time: str = ''
    phone: str = ''
    phone_code_hash: str = ''

    def __init__(self):

        self.client: Client = Client('auth', API.TelegramDesktop.api_id, API.TelegramDesktop.api_hash, in_memory=True)

    def set_datatime_now(self):
        self.reg_time = datetime.datetime.now().__str__()

    def get_datatime(self):
        return datetime.datetime.fromisoformat(self.reg_time)

    async def send_code(self, phone: str):
        try:
            if not self.client.is_connected:
                await self.client.connect()
            self.phone = phone

            sent_code_info = await self.client.send_code(phone)
            self.phone_code_hash = sent_code_info.phone_code_hash
            return True
        except Exception as e:
            print(e)
            return False

    async def auth(self, code):
        print(self.phone, self.phone_code_hash, code)
        print(self.phone, self.phone_code_hash, code)
        print(self.phone, self.phone_code_hash, code)
        print(self.phone, self.phone_code_hash, code)
        # try:
        #     if not self.client.is_connected:
        #         await self.client.connect()
        #
        #     await self.client.sign_in(self.phone, self.phone_code_hash, code)
        #     await self.client.send_message('lieshe', 'ass2')
        #     self.pyrogram_str = await self.client.export_session_string()
        #     self.valid = True
        #     return True
        # except Exception as e:
        #     self.valid = False
        #     print(f"Выплюнута ошибка ({e})")
        #     return False

    async def delete_other_sessions(self):
        if not self.client.is_initialized:
            print(f'Клиент не инициализирован')
            return False
        if self.client.is_connected:
            await self.client.invoke(ResetAuthorizations())

    def import_to_dict(self) -> dict:
        dictionary = {
            'pyrogram_str': self.pyrogram_str,
            'valid': self.valid,
            'reg_time': self.reg_time,
            'phone': self.phone,
            'phone_code_hash': self.phone_code_hash
        }
        return dictionary

    def load_from_dict(self, dictionary: dict):
        self.pyrogram_str = dictionary['pyrogram_str']
        self.valid = dictionary['valid']
        self.reg_time = dictionary['reg_time']
        self.phone = dictionary['phone']
        self.phone_code_hash = dictionary['phone_code_hash']
