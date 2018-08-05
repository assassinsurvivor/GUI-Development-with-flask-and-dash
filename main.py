from server import server
from flask import render_template
from content_management import Content


from app import app as app1
from app8 import app as app2



TOPIC_DICT = Content()


@server.route('/',endpoint='dashboard')
@server.route('/dashboard/',endpoint='dashboard')
def dashboard():
    return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)


@server.route('/model/',endpoint='model')
def model():
    return render_template("model.html",TOPIC_DICT = TOPIC_DICT)




if __name__ == '__main__':
    server.run()
