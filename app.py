from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from flask_login import LoginManager, current_user
from flask_login import login_user, login_required, logout_user

from flask_restful import Api

from flask_socketio import SocketIO, emit

from codeeee.data import db_session
from codeeee.data import users
from codeeee.data import game as gm

from codeeee.app_functions import init_game, check_set, check_set_on_field

import json

from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '179supertop'

api = Api(app)

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)

@login_required
@socketio.on('check_set', namespace='/set')
def handler_set(data):
    """data list of 3 indexes, for example data = {indexes: [0, 1, 2]}"""
    print('--------------------------')
    print()
    print(f'requset: {data["indexes"]}')
    print()
    print('--------------------------')
    db_sess = db_session.create_session()
    gam = db_sess.query(gm.Game).order_by(gm.Game.id.desc()).first()
    game = json.loads(gam.game)
    print()
    print('--------------------------')
    print('CARDS')
    print('--------------------------')
    pprint(game['cards'])
    trash_cards = [game['cards'][data['indexes'][0]],
             game['cards'][data['indexes'][1]],
             game['cards'][data['indexes'][2]]]
    game['cards'][data['indexes'][0]] = None
    game['cards'][data['indexes'][1]] = None
    game['cards'][data['indexes'][2]] = None
    if check_set.check_set(trash_cards):
        print('-----------------------')
        print()
        print('SET IS CORRECT')
        print()
        print('-----------------------')
        c1, c2, c3 = init_game.new_card(), init_game.new_card(), init_game.new_card()
        print()
        print('-----------------------')
        print()
        print('c1')
        pprint(c1)
        print()
        print('-----------------------')
        print()
        print('-----------------------')
        print()
        print('c2')
        pprint(c2)
        print()
        print('-----------------------')
        print()
        print('-----------------------')
        print()
        print('c3')
        pprint(c3)
        print()
        print('-----------------------')
        copy_cards = game['cards'][:]
        copy_cards[data['indexes'][0]] = c1
        copy_cards[data['indexes'][1]] = c2
        copy_cards[data['indexes'][2]] = c3
        print(not (c1 != c2 != c3))
        print(c1 in (game['cards'] + game['trash-queue']))
        print(c2 in (game['cards'] + game['trash-queue']))
        print(c3 in (game['cards'] + game['trash-queue']))
        print(not check_set_on_field.check_exist_set_on_field(copy_cards))
        while ((not c1 != c2 != c3) or (c1 in (game['cards'] + game['trash-queue']))
               or (c2 in (game['cards'] + game['trash-queue'])) or (c3 in (game['cards'] + game['trash-queue']))
               or (not check_set_on_field.check_exist_set_on_field(copy_cards))):
            c1, c2, c3 = init_game.new_card(), init_game.new_card(), init_game.new_card()
            print()
            print('-----------------------')
            print()
            print('c1')
            pprint(c1)
            print()
            print('-----------------------')
            print()
            print('-----------------------')
            print()
            print('c2')
            pprint(c2)
            print()
            print('-----------------------')
            print()
            print('-----------------------')
            print()
            print('c3')
            pprint(c3)
            print()
            print('-----------------------')
            copy_cards[data['indexes'][0]] = c1
            copy_cards[data['indexes'][1]] = c2
            copy_cards[data['indexes'][2]] = c3
            print(not (c1 != c2 != c3))
            print(c1 in (game['cards'] + game['trash-queue']))
            print(c2 in (game['cards'] + game['trash-queue']))
            print(c3 in (game['cards'] + game['trash-queue']))
            print(not check_set_on_field.check_exist_set_on_field(copy_cards))
        for i in range(3):
            game['trash-queue'].pop(0)
        game['trash-queue'] = game['trash-queue'] + trash_cards
        game['cards'] = copy_cards
        gam.game = json.dumps(game)
        user = db_sess.query(users.User).filter(users.User.id == session['id']).first()
        # print('********')
        # print(session['id'])
        # print('********')
        print('------------------------')
        print()
        print('new field')
        pprint(copy_cards)
        print('------------------------')
        user.counter += 1
        db_sess.commit()
        emit('get_field_response', copy_cards, broadcast=True)
        emit('user_counter', user.counter)
    else:
        print()
        print('-----------------------')
        print()
        print('SET IS NOT CORRECT')
        emit('check_set_response', False, namespace='/set')


@socketio.on('get_field', namespace='/set')
def handler_field():
    db_sess = db_session.create_session()
    game = json.loads(db_sess.query(gm.Game).order_by(gm.Game.id.desc()).first().game)
    user = db_sess.query(users.User).filter(users.User.id == session['id']).first()
    emit('get_field_response', game['cards'])
    emit('user_counter', user.counter)


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
                session['id'] = user.id
                return redirect("/game")
            return render_template('auth.html',
                                   messages=["Неправильный логин или пароль"])

@login_required
@app.route('/game')
def game():
    return render_template('demo.html')
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/leader_table')
def leader_table():
    db_sess = db_session.create_session()
    user = db_sess.query(users.User).all()
    us = [(use.login, use.counter) for use in user]
    return render_template('table_leaders.html', us = sorted(us, key=lambda x: (-x[1], x[0])))


def main():
    db_session.global_init('db/set.sqlite')
    print(init_game.run())
    socketio.run(app, port=8888, host='127.0.0.1')

if __name__ == '__main__':
    main()
