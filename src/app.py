from flask import Flask, render_template, request

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
            print("Name is empty")
        elif not buyin:
            print("Buy-in is empty")
        elif not cashout:
            print("Cashout is empty")
        else:
            try:
                buyin = float(buyin)
                cashout = float(cashout)
            except ValueError:
                return "Bad request!", 400
            # TODO: Call add_player on algorithm class
            return render_template('add_player_result.html', name=name, buyin=buyin, cashout=cashout)
    return render_template('add_player.html')


@app.route('/add-player/<name>/<float:buyin>/<float:cashout>')
def add_player_rest(name, buyin, cashout):
    return render_template('add_player_result.html', name=name, buyin=buyin, cashout=cashout)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7653)
