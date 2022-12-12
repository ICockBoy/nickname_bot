from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
async def index():
    request_login = request.args.get('login')
    if request_login and request_login != '':
        return render_template("number/number.html", username=request_login)
    else:
        return render_template("number/bad_request.html")


@app.route('/code', methods=['POST'])
async def code():
    request_login = request.args.get('login')
    request_phone = request.args.get('phone')
    if request_login and request_login != '' and request_phone and request_phone != '':
        return render_template("number/number.html", username=request_login)
    else:
        return render_template("number/bad_request.html")

if __name__ == "__main__":
    app.run()

