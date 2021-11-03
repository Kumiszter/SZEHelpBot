from flask import Flask, redirect, url_for, render_template
#from main import commands

app = Flask(__name__)

commands = ["terkep", "neptun", "gyujtoszamla", "linkek", "to","datumok", "szoctam"]


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/parancs-letrehozas")
def commandcreator():
	return render_template("commandcreator.html")


@app.route("/aktiv-parancsok")
def commandlist():
	return render_template("commands.html", commands=commands)


if __name__ == "__main__":
	app.run(debug=True)