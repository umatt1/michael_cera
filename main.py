
# flask
from flask import Flask, render_template, Blueprint, request
from flask import session
from chess import openings_guru
from twitter import synthetic_parrot
from covid_simulator import covid_simulator
from motif_finder import motifer
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from weather import what2wear

app = Flask(__name__)
app.secret_key = "this key is a secret"
app.permanent_session_lifetime = timedelta(seconds=30)

app.register_blueprint(openings_guru, url_prefix="/chess")
app.register_blueprint(synthetic_parrot, url_prefix="/twitter")
app.register_blueprint(covid_simulator, url_prefix="/covid")
app.register_blueprint(motifer, url_prefix="/motif_finder")
app.register_blueprint(what2wear, url_prefix="/what2wear")

@app.route("/")
def home():
    return render_template("home.html")

# image board

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    message = db.Column(db.String(100))
    image = db.Column(db.String(100))

    def __init__(self, message, image):
        self.message = message
        self.image = image

@app.route("/board/", methods=["POST", "GET"])
def image_board():
    # process post
    if request.method == 'POST' and not session.get('posted'):
        image = request.form['image']
        message = request.form['message']
        session['posted'] = True
        post = posts(message, image)
        db.session.add(post)
        db.session.commit()
        print("posted a post")

    print(session.get('posted'))
    # display image board
    all_posts = reversed(posts.query.all())
    return render_template('board.html', values=all_posts)

db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
