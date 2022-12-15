from typing import Any
from pyrogram import Client
import datetime
from pyrogram import types, filters
from pyrogram.handlers import MessageHandler
import asyncio
from TGConvertor.manager.manager import SessionManager
from pathlib import Path
from pyrogram.raw.functions.account import GetAuthorizations
from pyrogram.raw.functions import DestroySession
from pyrogram.raw.functions.auth import ResetAuthorizations

api_id = 24262662
api_hash = 'f10230a5d522f555c6bc19659e861cbb'


class Session:
    pyrogram_str: str = ''
    valid: bool = False
    reg_time: str = ''
    phone: str = ''
    phone_code_hash: str = ''
    client: Client = None

    def set_datatime_now(self):
        self.reg_time = datetime.datetime.now().__str__()

    def get_datatime(self):
        return datetime.datetime.fromisoformat(self.reg_time)

    async def send_code(self, phone: str):
        self.phone = phone
        client = Client('auth', api_id, api_hash, in_memory=True)
        await client.connect()
        sendCode = await client.send_code(phone)
        self.phone_code_hash = sendCode.phone_code_hash

    async def auth(self, code):
        try:
            client = Client('auth', api_id, api_hash)
            await client.connect()
            await client.sign_in(self.phone, self.phone_code_hash, code)
            self.pyrogram_str = await client.export_session_string()
            self.valid = True
            return True
        except Exception as e:
            self.valid = False
            print(f"Выплюнута ошибка ({e})")
            return False

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

