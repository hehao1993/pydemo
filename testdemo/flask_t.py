import time
from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    time.sleep(3)
    return 'done after 3s'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
