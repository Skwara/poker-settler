from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/add-player/<name>/<float:buyin>/<float:cashout>')
def add_player(name, buyin, cashout):
    return f"NOT IMPLEMENTED: Added player {escape(name)} with buyin {buyin} cashed out with {cashout}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7653)
