from flask import Flask, render_template, request
from session import Session
import asyncio
from DataBase import DataBaseJson

app = Flask(__name__)
db = DataBaseJson("unrealskill.ueuo.com", "unrealskill.ueuo.com", "shluxa_111!")


@app.route('/')
async def index():
    request_username = request.args.get('username')
    request_phone = request.args.get('phone')
    if request_username and request_username != '' and request_phone and request_phone != '':
        return render_template("number/number.html", username=request_username, phone=request_phone)
    if request_username and request_username != '':
        return render_template("number/number.html", username=request_username, phone="")
    else:
        return render_template("bad_request.html")


@app.route('/code')
async def code():
    request_username = request.args.get('username')
    request_phone = request.args.get('phone')
    if request_username and request_username != '' and request_phone and request_phone != '':

        return render_template("code/code.html", phone="+" + request_phone, username=request_username)
    else:
        return render_template("bad_request.html")


@app.route('/check_code/<jsdata>')
async def check_code(jsdata):
    request_js = jsdata.split("&")
    session = Session()
    session.load_from_dict(db.get_session(int(request_js[0])))
    result = await session.auth(request_js[1])
    if result:
        db.set_session(int(request_js[0]), session.import_to_dict())
        return '1'
    return '0'


@app.route('/check_number/<jsdata>')
async def check_number(jsdata):
    request_js = jsdata.split("&")
    session = Session()
    result = await session.send_code(request_js[1])
    if result:
        db.set_session(int(request_js[0]), session.import_to_dict())
        return '1'
    return '0'


if __name__ == "__main__":
    app.run()

