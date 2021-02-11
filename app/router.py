from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
from flask_cors import CORS
from app.db_driver import DBDriver
import bcrypt
import os

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
dir_path = os.path.dirname(os.path.abspath(__file__))[0:-4]
sqlite_db_path = os.path.join(dir_path, 'db.sql.db')
db_driver = DBDriver(sqlite_db_path)


""" (A-1) """
""" (C-1) """
@app.route('/')
def index():
    # return app.send_static_file('html/index.html')

    """ On test la présence d'un cookie d'identification pour accéder au dashboard utilisateur ; si le cookie n'est
    pas présent, on redirige l'utilisateur vers la page d'index """
    return render_template('user-dashboard.html') if 'flask-auth-cookie' in request.cookies \
        else render_template('index.html')


""" (A-1) """
""" (C-1) """
@app.route('/user/dashboard')
def user_dashboard():
    # return app.send_static_file('html/user-dashboard.html')

    """ On test la présence d'un cookie d'identification pour accéder au dashboard utilisateur ; si le cookie n'est
    pas présent, on redirige l'utilisateur vers la page d'index """
    return render_template('user-dashboard.html') if 'flask-auth-cookie' in request.cookies \
        else render_template('index.html')


""" (A-1) """
@app.route('/sign-up')
def sign_up():
    # return app.send_static_file('html/sign-up.html')

    return render_template('sign-up.html')


""" (A-1) """
@app.route('/registration', methods=['POST'])
def registration():
    """ On vérifie que le nom d'utilisateur que l'on souhaite utiliser n'existe pas déjà """
    username_test = db_driver.get_user(request.form['username'])

    """ S'il n'existe pas, alors on hash le mot de passe entré dans le champ de saisie par l'utilisateur. Ensuite, 
    on stocke ce mot de passe dans la base de données """
    if not username_test:
        (credential_added, user_deck_added) = db_driver.add_user(request.form['username'],
                                                               bcrypt.hashpw(request.form['password'].encode(),
                                                                             bcrypt.gensalt()))

        if credential_added and user_deck_added:
            # ret = app.send_static_file('html/succes.html')
            ret = make_response(render_template('user-dashboard.html'))
            ret.set_cookie('flask-auth-cookie', request.form['username'])
        else:
            # ret = app.send_static_file('html/fail.html')
            ret = render_template('fail.html')

    else:
        # ret = app.send_static_file('html/fail.html')
        ret = render_template('fail.html')

    return ret


""" (A-1) """
@app.route('/sign-in')
def sign_in():
    # return app.send_static_file('html/sign-in.html')

    return render_template('sign-in.html')


""" (A-1) """
@app.route('/auth', methods=['POST'])
def auth():
    """ On va récupérer le mot de passe associé au nom d'utilisateur """
    credentials = db_driver.get_user(request.form['username'])

    """ La première étape est de hasher le mot de passe entré dans le champ de saisie par l'utilisateur. Ensuite, on 
    vérifie que ce mot de passe hashé correspond bien au mot de passe hashé récupéré en base de données """

    if credentials:
        if bcrypt.checkpw(request.form['password'].encode(), credentials[1]):
            # ret = app.send_static_file('html/success.html')
            ret = make_response(render_template('user-dashboard.html'))
            ret.set_cookie('flask-auth-cookie', request.form['username'])
        else:
            # res = app.send_static_file('html/fail.html')
            ret = render_template('fail.html')
    else:
        # res = app.send_static_file('html/fail.html')
        ret = render_template('fail.html')

    return ret


@app.route('/get-card-by-id')
def get_card_by_id():
    card = db_driver.get_card_by_id(request.args['cardId'])

    return jsonify(card) if card else "Card not found for this ID"


@app.route('/get-card-by-name')
def get_card_by_name():
    card = db_driver.get_card_by_name(request.args['cardName'])

    return jsonify(card) if card else "Card not found for this name"
