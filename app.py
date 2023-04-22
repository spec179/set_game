from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from flask_login import LoginManager, current_user
from flask_login import login_user

from flask_socketio import SocketIO, emit

from code.data import db_session
from code.data import users
from code.data import game as gm

from code.app_functions import init_game, check_set, check_set_on_field

# from .app_functions import init_game

'''folowing code shoud be in code/app_functions/init_game.py'''
# from random import shuffle
# import json
# from data import db_session
# from data import game as gm


# def run():
#     all_cards = []
#     for a in range(3):
#         for b in range(3):
#             for c in range(3):
#                 for d in range(3):
#                     card = {
#                         "color": a,
#                         "shape": b,
#                         "number": c,
#                         "fill": d
#                     }
#                     all_cards.append(card)
#     shuffle(all_cards)
#     game_json = {
#         "cards": [all_cards[i] for i in range(12)],
#         "trash-queue": [all_cards[i] for i in range(12, 27)]
#     }
#     game = gm.Game()
#     game.game = json.dumps(game_json)
#     db_sess = db_session.create_session()
#     db_sess.add(game)
#     db_sess.commit()
#     return game_json
'''*end*'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '179supertop'

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


@socketio.on('check_set', namespace='/set')
def handler_set(data):
    """data list of 3 indexes, for example data = {indexes: [0, 1, 2]}"""
    print(f'response: {data["indexes"]}')
    db_sess = db_session.create_session()
    game = db_sess.query(gm.Game).order_by(gm.Game.id.desc()).first().game
    print(game, type(game))
    trash_cards = [game['cards'][data['indexes'][0]],
             game['cards'][data['indexes'][1]],
             game['cards'][data['indexes'][2]]]
    game['cards'][data['indexes'][0]] = None
    game['cards'][data['indexes'][1]] = None
    game['cards'][data['indexes'][2]] = None
    if check_set.check_set(trash_cards):
        c1, c2, c3 = init_game.new_card(), init_game.new_card(), init_game.new_card()
        copy_cards = game['cards']
        copy_cards[data['indexes'][0]] = c1
        copy_cards[data['indexes'][1]] = c2
        copy_cards[data['indexes'][2]] = c3
        while (not (c1 != c2 != c3) or (c1 in game['cards'] + game['trash_queue'])
                or (c1 in game['cards'] + game['trash_queue']) or (c1 in game['cards'] + game['trash_queue'])
                or not check_set_on_field.check_exist_set_on_field(copy_cards)):
            c1, c2, c3 = init_game.new_card(), init_game.new_card(), init_game.new_card()
            copy_cards[data['indexes'][0]] = c1
            copy_cards[data['indexes'][1]] = c2
            copy_cards[data['indexes'][2]] = c3
        for i in range(3):
            game['trash_queue'].pop(0)
        game['trash_queue'] = game['trash_queue'] + trash_cards
        game['cards'] = copy_cards
        db_sess.commit()
        current_user.id
        emit('set_response', copy_cards, broadcast=True, namespace='/set')
    else:
        emit('set_response', False, namespace='/set')


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
    return render_template('demo.html')
    

def main():
    db_session.global_init('db/set.sqlite')
    print(init_game.run())
    socketio.run(app)

if __name__ == '__main__':
    main()