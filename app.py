from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///films.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    films = Film.query.all()
    return render_template("index.html", films=films)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        new_film = Film(
            title=request.form["title"],
            genre=request.form["genre"],
            year=int(request.form["year"]),
        )
        db.session.add(new_film)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/update/<int:film_id>", methods=["GET", "POST"])
def update(film_id):
    film = Film.query.get_or_404(film_id)
    if request.method == "POST":
        film.title = request.form["title"]
        film.genre = request.form["genre"]
        film.year = int(request.form["year"])
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", film=film)

@app.route("/delete/<int:film_id>")
def delete(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)