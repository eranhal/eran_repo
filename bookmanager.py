import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "postgres:///{}".format(os.path.join(project_dir, "postgres.db"))

DB_URL = 'postgresql://postgres:ErnikoErniko1@localhost:5432/postgres'


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return "<Title: {}>".format(self.first_name)


@app.route("/", methods=["GET", "POST"])
def home():
    users = None

    if request.form:
        try:
            book = Users(id=request.form.get("id"), first_name=request.form.get('first_name'))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    users = Users.query.filter_by()
    return render_template("home.html", users=users)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Users.query.filter_by(id=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Users.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8087, debug=True)
