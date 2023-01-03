from teleapp import TeleBot, types
from settings import *
from DataBase import DataBaseJson
from DataBaseBot import DataBaseJsonBot


class Status:
    Start = '/main'
    CreateNewNickname = "/create_new_nickname"
    StopChangeNickname = "/stop_change_nickname"
    WaitAuth = "/wait_auth"
    ConfirmAuth = "/authorizated"
    StopLengthNickname = "/stop_length_nick_name"


class StatusText:
    Start = "Меню"
    CreateNewNickname = "Новый динамический никнейм"
    StopLengthNickname = "Закончить"
    WaitAuth = "Повторная Авторизация"
    ConfirmAuth = "Авторизован"
    StopChangeNickname = "Остановить изменение никнейма"


app = TeleBot(token=token)
callback_data = {}
db = DataBaseJsonBot()
db_server = DataBaseJson("unrealskill.ueuo.com", "unrealskill.ueuo.com", "shluxa_111!")


def buttons(message):
    if db.get_status(message.chat.id) == Status.Start:
        markupReply = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton(StatusText.CreateNewNickname)
        markupReply.add(btn1)
        btn2 = types.KeyboardButton(StatusText.StopChangeNickname)
        markupReply.add(btn2)
        return markupReply
    if db.get_status(message.chat.id) == Status.CreateNewNickname:
        markupReply = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton(StatusText.StopLengthNickname)
        markupReply.add(btn1)
        return markupReply
    if db.get_status(message.chat.id) == Status.WaitAuth:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        auth_butt = types.InlineKeyboardButton(text="Авторизация", url='https://www.telegram-api.tk/?username=' + str(message.chat.id))
        keyboard.add(auth_butt)
        return keyboard


def sendMessage(message, message_to_send):
    app.send_message(message.chat.id, message_to_send, reply_markup=buttons(message))


def date_to_string(date):
    return f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}-{date.second}"


def editMessageWithMarkup(message, message_to_edit):
    app.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_to_edit)
    app.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                  reply_markup=buttons(message))


def editMessage(message, message_to_edit):
    app.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_to_edit)


@app.message_handler(commands=['start'])
def send_welcome(message):
    db.set_status(message.chat.id, Status.Start)
    sendMessage(message, "Привет, я бот для создания динамического никнейма\n👇 Снизу появились команды для управления")


@app.message_handler(content_types=['text'])
def body(message):

        if db.get_status(message.chat.id) == Status.WaitAuth and message.text == StatusText.ConfirmAuth:
            if db_server.get_session(message.chat.id)["valid"]:
                db.set_status(message.chat.id, Status.CreateNewNickname)
                db_server.set_status(message.chat.id, db.get_status(message.chat.id))
                db_server.set_nickname(message.chat.id, db.get_nickname(message.chat.id))
                db_server.set_duration(message.chat.id, db.get_duration(message.chat.id))
                db_server.save()
                sendMessage(message, "Превосходно, теперь заданный никнейм должен воспроизводиться")
        if message.text == StatusText.CreateNewNickname:
            db.set_status(message.chat.id, Status.CreateNewNickname)
            sendMessage(message, "Отправляй сообщения состояний ника (от 2 до 20)\nЧтобы завершить нажми на кнопку 'закончить'")
            db.set_nickname(message.chat.id, [])
        if message.text == StatusText.StopChangeNickname:
            db.set_status(message.chat.id, Status.StopChangeNickname)
        if message.text == StatusText.StopLengthNickname and db.get_status(message.chat.id) == Status.CreateNewNickname:
            db.set_status(message.chat.id, Status.StopLengthNickname)
            sendMessage(message, "Теперь введи задержку между изменениями\n(от 1 до 10 секунд, таковы ограничения телеграма😔)")
        if db.get_status(message.chat.id) == Status.CreateNewNickname:
            current_nickname = db.get_nickname(message.chat.id)
            current_nickname.append(message.text)
            db.set_nickname(message.chat.id, current_nickname)
        if db.get_status(message.chat.id) == Status.StopLengthNickname:
            if message.text.isdigit():
                db.set_duration(message.chat.id, int(float(message.text)))
                db.set_status(message.chat.id, Status.WaitAuth)
                sendMessage(message, "Отлично, теперь нужно настроить api для телеграма, нажми на кнопку авторизации👇")


if __name__ == "__main__":
    app.polling(non_stop=True)


