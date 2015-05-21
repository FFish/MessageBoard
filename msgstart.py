from flask import Flask, render_template, request, g
import sqlite3


# Configuration
DATABASE = "/db/message.db"

app = Flask(__name__)
app.config.from_object(__name__)

def contect_db():
    return sqlite3.connect(app.config['DATABASE']) 

@app.before_request
def before_request():
    g.db = contect_db()

@app.teardown_request
def teardown_request():
    db = getattr(g, 'db', None)
    if db is not None:
	db.close()

@app.route("/add", methods=['POST'])
def add(): 
    g.db.execute('insert into entries (title, content) values (?,?)', (request.form['title'], request.form['content']))
    g.db.commit()
    return "Add Successfully" 

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
