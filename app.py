from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from flask_login import LoginManager
from flask_login import login_user

from data import db_session
from data import users 

# from .app_functions import init_game

'''folowing code shoud be in app_functions/init_game.py'''
from random import shuffle
import json
from data import db_session
from data import game as gm


def run():
    all_cards = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    card = {
                        "color": a,
                        "shape": b,
                        "number": c,
                        "fill": d
                    }
                    all_cards.append(card)
    shuffle(all_cards)
    game_json = {
        "cards": [all_cards[i] for i in range(12)],
        "trash-queue": [all_cards[i] for i in range(12, 27)]
    }
    game = gm.Game()
    game.game = json.dumps(game_json)
    db_sess = db_session.create_session()
    db_sess.add(game)
    db_sess.commit()
    return game_json
'''*end*'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '179supertop'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/auth', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html', message='')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        if request.form.get('checkbox', False):
            if db_sess.query(users.User).filter(users.User.login == request.form['login']).first():
                return render_template('auth.html',
                                       messages=["Такой пользователь уже есть"])
            user = users.User(login=request.form['login'])
            user.set_password(request.form['password'])
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect("/game")
        else:
            user = db_sess.query(users.User).filter(users.User.login == request.form['login']).first()
            if user and user.check_password(request.form['password']):
                login_user(user)
                return redirect("/game")
            return render_template('auth.html',
                                   messages=["Неправильный логин или пароль"])


@app.route('/game')
def game():
    return render_template('set.html')
    

def main():
    db_session.global_init('db/set.sqlite')
    #print(run())
    app.run(port=8080, host="127.0.0.1")

if __name__ == '__main__':
    main()