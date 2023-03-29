from flask import Flask, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException, abort

from poker_settler import PokerSettler

app = Flask(__name__)
settler = PokerSettler()  # TODO: Don't use global variables with Flask


@app.route('/')
def home():
    return render_template('home.html', settlement=settler.settlement())


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
            return add_player_rest(name=name, buyin=buyin, cashout=cashout)
    return render_template('add_player.html')


@app.route('/add-player/<name>/<int:buyin>/<int:cashout>')
def add_player_rest(name, buyin, cashout):
    settler.add_result(name, int(buyin), int(cashout))
    return redirect(url_for('home'))


@app.route('/reset')
def reset():
    settler.reset()
    return redirect(url_for('home'))


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e.get_response()
    else:
        return repr(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7653)
