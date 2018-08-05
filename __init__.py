from flask import Flask, render_template
from content_management import Content
from server import server
TOPIC_DICT = Content()
app = Flask(name='dashboard', sharing=True, server=server, url_base_pathname='/dashboard')

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)

if __name__ == "__main__":
    app.run(debug=True)
