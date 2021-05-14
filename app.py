from flask import Flask
from find_slot import run

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to Notifier"

@app.route("/notify")
def notify():
    print("Hell")
    return run()

