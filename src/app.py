from flask import Flask, render_template

app = Flask(__name__)


@app.route('/add-player/<name>/<float:buyin>/<float:cashout>')
def add_player(name, buyin, cashout):
    return render_template('add_player_result.html', name=name, buyin=buyin, cashout=cashout)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7653)
