from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from data import db_session

app = Flask(__name__)

@app.route('/')
@app.route('/auth')
def authorization():
    return render_template('auth.html', title='auth')

def main():
    db_session.global_init('db/users.sqlite')
    #app.run(port=8080, host="127.0.0.1")
    app.run()
    return

if __name__ == '__main__':
    main()