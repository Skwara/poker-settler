from flask import Flask, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException, abort

from poker_settler import PokerSettler

app = Flask(__name__)
settler = PokerSettler()  # TODO: Don't use global variables with Flask


@app.route('/')
def home():
    return render_template('home.html', results=settler.results, settlement=settler.settlement())


@app.route('/submit_results', methods=['POST'])
def submit_results():
    settler.reset()
    result_count = int(request.form['resultCount'])
    for player_idx in range(result_count):
        name = request.form[f'name{player_idx}']
        buyin = request.form[f'buyin{player_idx}']
        cashout = request.form[f'cashout{player_idx}']
        if not name:
            abort(400, "Player name is empty")
        elif not buyin:
            abort(400, "Buy-in is empty")
        elif not cashout:
            abort(400, "Cashout is empty")
        settler.add_result(name, int(buyin), int(cashout))
    return redirect(url_for('home'))


@app.route('/reset', methods=['POST'])
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
