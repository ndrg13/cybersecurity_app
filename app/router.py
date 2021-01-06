from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')


if __name__ == '__main__':
    app.run()
