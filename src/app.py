from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException, abort

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add-player/', methods=('GET', 'POST'))
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        buyin = request.form['buyin']
        cashout = request.form['cashout']
        if not name:
            abort(400, "Player name is empty")
        elif not buyin:
            abort(400, "Buy-in is empty")
        elif not cashout:
            abort(400, "Cashout is empty")
        else:
            # TODO: Call add_player on algorithm class
            return render_template('add_player_result.html', name=name, buyin=float(buyin), cashout=float(cashout))
    return render_template('add_player.html')


@app.route('/add-player/<name>/<float:buyin>/<float:cashout>')
def add_player_rest(name, buyin, cashout):
    return render_template('add_player_result.html', name=name, buyin=buyin, cashout=cashout)


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e.get_response()
    else:
        return repr(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7653)
