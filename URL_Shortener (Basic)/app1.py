from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pyshorteners

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(200), nullable=False)
    shortened_url = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"URL('{self.original_url}', '{self.shortened_url}')"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    shortener = pyshorteners.Shortener()
    shortened_url = shortener.tinyurl.short(original_url)
    url = URL(original_url=original_url, shortened_url=shortened_url)
    db.session.add(url)
    db.session.commit()
    return render_template('home.html', shortened_url=shortened_url)

@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)