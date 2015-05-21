import sqlite3

from flask import Flask, render_template, request, g, redirect, url_for



# Configuration
DATABASE = "db/message.db"

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if exception is not None:
        print exception
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route("/add", methods=['POST'])
def add():
    g.db.execute('insert into entries (title, text) values (?,?)', (request.form['title'], request.form['content']))
    g.db.commit()
    return redirect(url_for("index"))


@app.route("/index")
def index():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("index.html", entries=entries)


@app.route("/")
def root():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
