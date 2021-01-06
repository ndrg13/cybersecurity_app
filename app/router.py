from flask import Flask, render_template, request
from app.db_driver import DBDriver

app = Flask(__name__)
db_driver = DBDriver('db.sql.db')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')


@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')


@app.route('/auth', methods=['POST'])
def auth():
    res = None
    credentials = db_driver.get_user(request.form['username'])

    if request.form['password'] == credentials[1]:
        res = render_template('success.html')
    else:
        res = render_template('fail.html')

    return res


@app.route('/registration', methods=['POST'])
def registration():
    res = None
    username_test = db_driver.get_user(request.form['username'])

    if username_test is None:
        add_result = db_driver.add_user(request.form['username'], request.form['password'])
        res = render_template('success.html')
    else:
        res = render_template('fail.html')

    return res
