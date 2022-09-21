from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vqqrxftinrhewo:2db1c8167baceee77e310ecb385a834d6b90bc4b60ff77500822d58bde33b8fe@ec2-52-70-45-163.compute-1.amazonaws.com:5432/dcgo2vualjgh2'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        # Check if url exits
        url_received = request.form["url-form"]
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return render_template('index.html', url=found_url.short)
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return render_template('index.html', url=short_url)
    else:
        return render_template('index.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template("404.html")




if __name__ == '__main__':
    app.run(debug=True)
