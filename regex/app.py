from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/match', methods=['POST'])
def match():
    regex = request.form['regex']
    test_string = request.form['test_string']
    matches = re.findall(regex, test_string)
    count = len(matches)
    return render_template('result.html', regex=regex, test_string=test_string, count=count)

if __name__ == '__main__':
    app.run(debug=True)
