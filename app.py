from flask import Flask, render_template, redirect, url_for, abort, request
from time import sleep

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home/index.html')

@app.route("/make_login_google_account")
def make_login_google_account():
    return {"status_login": "SUCCESS"}

@app.route("/get_schedule_nice_platform", methods=['POST'])
def get_schedule_nice_platform():
    sleep(1)
    if request.method == 'POST':
        user_mocked = "teste"
        pass_mocked = "teste123"
        data = request.get_json()
        print(data)
        if user_mocked == data['inputUser'] and pass_mocked == data['inputPassword']:
            return {"status_requisition": "login_success"}
        else:
            # return {"status_requisition": "login_failed"}
            abort(401)

    else:
        abort(405)


if __name__ == "__main__":
    app.run(debug=True)