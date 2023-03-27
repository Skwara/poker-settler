from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return f"Hello from {app.name}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7653)
