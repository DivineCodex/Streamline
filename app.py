from flask import Flask, session, redirect, url_for, flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

"""app.config["UPLOADS_FOLDER"] = "/storage/emulated/0/Application/flask_blog/static/uploads"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change the database URI as needed
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(40))
    image_filename = db.Column(db.String(100))
    
class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(300))
    image_post = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


"""@app.route("/")
def show_entries():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("/entries/index.html")"""

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        image = request.files["image"]
        
        users = User.query.filter_by(email = email).first()
        if users:
            return "<h1>User email already exists</h1>"
        else:
            image.save("static/uploads/" + image.filename)
            new_user = User(
            username = username,
            email = email,
            password = password,
            image_filename = image.filename
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("signup.html")



@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email = email, password = password).first()
        if user:
            session["logged_in"] = True
            session["user_id"] = user.id
            return redirect(url_for("show_entries"))
    
        else:
            return "<h1>user not registered</h1>"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("show_entries"))


@app.route("/")
def show_entries():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        if "user_id" in session:
            user_id = session["user_id"]
            if user_id:
                user = User.query.get(user_id)
                if user:
                    return render_template("entries/home.html", name = user)

@app.route("/groups")
def groups():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        if "user_id" in session:
            user_id = session["user_id"]
            if user_id:
                user = User.query.get(user_id)
                if user:
                    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
                    return render_template("entries/groups.html", name = user, entries = entries)

@app.route("/post")
def post():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    else:
        return render_template("entries/post.html")

@app.route("/create_post", methods = ["GET", "POST"])
def create_post():
    if request.method == "POST":
        text = request.form["text"]
        image = request.files["image"]
        
        image.save("static/uploads/" + image.filename)
        entry = Entry (
        text = text,
        image_post = image.filename
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("groups"))





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
