from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from main import commands

db = SQLAlchemy()
DB_NAME = "database.db"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdasdasd'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


commands = ["terkep", "neptun", "gyujtoszamla", "linkek", "to","datumok", "szoctam"]


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/parancs-letrehozas", methods=['GET', 'POST'])
def commandcreator():
	data = request.form
	print(data)
	return render_template("commandcreator.html")


@app.route("/aktiv-parancsok")
def commandlist():
	return render_template("commands.html", commands=commands)


if __name__ == "__main__":
	app.run(debug=True)
