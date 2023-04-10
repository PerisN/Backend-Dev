from flask import Flask, render_template, request

app = Flask(__name__)

notes = []

@app.route('/', methods=["GET", "POST"])  
def index():
    if request.method == "POST"  : # Did not have this condition but had a return statement
        note = request.form.get("note") # The 'request.args' should be 'request.form' since we are using the 'POST' method
        notes.append(note)
    return render_template("home.html", notes=notes)


if __name__ == '__main__':
    app.run(debug=True)