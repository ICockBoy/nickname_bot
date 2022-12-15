from telebot import TeleBot, types
from settings import *
from DataBase import DataBaseJson
import asyncio
from session import Session


class Status:
    Start = '/main'
    CreateNewNickname = "/create_new_nickname"
    StopChangeNickname = "/stop_change_nickname"
    AcceptNumber = "/accept_number"
    StopLengthNickname = "/stop_length_nick_name"
    GetPhoneCode = "/get_phone_code"


class StatusText:
    Start = "Меню"
    CreateNewNickname = "Новый динамический никнейм"
    StopLengthNickname = "Закончить"
    AcceptNumber = "Подтвердить номер"
    StopChangeNickname = "Остановить изменение никнейма"


bot = TeleBot(token=token)
callback_data = {}
db = DataBaseJson("unrealskill.ueuo.com", "unrealskill.ueuo.com", "shluxa_111!")


def buttons(message):
    markupReply = types.ReplyKeyboardMarkup()
    if db.get_status(message.chat.id) == Status.Start:
        btn1 = types.KeyboardButton(StatusText.CreateNewNickname)
        markupReply.add(btn1)
        btn2 = types.KeyboardButton(StatusText.StopChangeNickname)
        markupReply.add(btn2)
        return markupReply
    if db.get_status(message.chat.id) == Status.CreateNewNickname:
        btn1 = types.KeyboardButton(StatusText.StopLengthNickname)
        markupReply.add(btn1)
        return markupReply
    if db.get_status(message.chat.id) == Status.AcceptNumber:
        btn1 = types.KeyboardButton(StatusText.AcceptNumber, request_contact=True)
        markupReply.add(btn1)
        return markupReply
    if db.get_status(message.chat.id) == Status.GetPhoneCode:
        return markupReply


def sendMessage(message, message_to_send):
    bot.send_message(message.chat.id, message_to_send, reply_markup=buttons(message))


def date_to_string(date):
    return f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}-{date.second}"


def editMessageWithMarkup(message, message_to_edit):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_to_edit)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                  reply_markup=buttons(message))


def editMessage(message, message_to_edit):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_to_edit)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    db.set_status(message.chat.id, Status.Start)
    sendMessage(message, "Привет, я бот для создания динамического никнейма\n👇 Снизу появились команды для управления")


@bot.message_handler(content_types=['contact'])
def number(message):
    if db.get_status(message.chat.id) == Status.AcceptNumber:
        db.set_status(message.chat.id, Status.GetPhoneCode)
        session = Session()
        asyncio.run(session.send_code(message.contact.phone_number))
        db.set_session(message.chat.id, session.import_to_dict())
        sendMessage(message, "Чтобы дать доступ к изменению ника, нужно прислать код из официального чата телеграм")


@bot.message_handler(content_types=['text'])
def body(message):
    if message.text == StatusText.CreateNewNickname:
        db.set_status(message.chat.id, Status.CreateNewNickname)
        sendMessage(message, "Отправляй сообщения состояний ника (от 2 до 20)\nЧтобы завершить нажми на кнопку 'закончить'")
        db.set_nickname(message.chat.id, [])
    if message.text == StatusText.StopChangeNickname:
        db.set_status(message.chat.id, Status.StopChangeNickname)
    if message.text == StatusText.StopLengthNickname:
        db.set_status(message.chat.id, Status.StopLengthNickname)
        sendMessage(message, "Теперь введи задержку между изменениями\n(от 1 до 10 секунд, таковы ограничения телеграма😔)")
    if db.get_status(message.chat.id) == Status.CreateNewNickname:
        current_nickname = db.get_nickname(message.chat.id)
        current_nickname.append(message.text)
        db.set_nickname(message.chat.id, current_nickname)
    if db.get_status(message.chat.id) == Status.StopLengthNickname:
        if message.text.isdigit():
            db.set_duration(message.chat.id, int(float(message.text)))
            db.set_status(message.chat.id, Status.AcceptNumber)
            sendMessage(message, "Отлично, теперь нужно настроить api для телеграма и подтвердить номер телефрна")
    if db.get_status(message.chat.id) == Status.GetPhoneCode:
        code = message.text
        if code is not None:
            session = Session()
            session.load_from_dict(db.get_session(message.chat.id))
            if asyncio.run(session.auth(code)):
                db.set_status(message.chat.id, Status.Start)
                sendMessage(message, "Отлично, запушено в работу")
            else:
                sendMessage(message, "Не то сообщение, код неверен")
        else:
            sendMessage(message, "Не то сообщение")



bot.polling(non_stop=True)


