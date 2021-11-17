from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commands.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Commands(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	command = db.Column(db.String(30), nullable=False, unique=True)
	title = db.Column(db.String(30), nullable=False)
	name = db.Column(db.String(30), nullable=False)
	output = db.Column(db.String(300), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.now)

	def __repr__(self):
		return '<Name %r>' % self.id

	# def __init__(self, command, title, name, output):
	# 	self.command = command
	# 	self.title = title
	# 	self.name = name
	# 	self.output = output
	# 	self.date_created = date_created



default_commands = ["terkep", "neptun", "gyujtoszamla", "linkek", "to", "datumok", "szoctam"]

#Commands(command, title, name, output)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/parancs-letrehozas", methods=['GET', 'POST'])
def commandcreator():
	data = request.form
	print(data)

	if request.method == "POST":
		command_command = request.form["command"]
		command_title = request.form["title"]
		command_name = request.form["name"]
		command_output = request.form["output"]
		

		new_command = Commands(command=command_command, title=command_title, 
								name=command_name, output=command_output)

		try:
			db.session.add(new_command)
			db.session.commit()
			return redirect("/aktiv-parancsok")
		except:
			return "Nem sikerült hozzáadni a parancsot!"

	else:
		commands = Commands.query.order_by(Commands.date_created)
		return render_template("commandcreator.html", commands=commands)

@app.route("/aktiv-parancsok")
def commandlist():
	#return render_template("commands.html", commands=commands)
	return render_template("commands.html", values=Commands.query.all())

@app.route("/parancs-modositas/<int:id>", methods=['GET', 'POST'])
def update(id):
	command_to_update = Commands.query.get_or_404(id)
	if request.method == "POST":
		command_to_update.command = request.form["command"]
		command_to_update.title = request.form["title"]
		command_to_update.name = request.form["name"]
		command_to_update.output = request.form["output"]

		try:
			db.session.commit()
			return redirect("/aktiv-parancsok")
		except:
			return "Nem sikerült módosítani a parancsot!"
	else:
		return render_template("update.html", command_to_update=command_to_update)

@app.route("/parancs-torles/<int:id>")
def delete(id):
	command_to_delete = Commands.query.get_or_404(id)

	try:
		db.session.delete(command_to_delete)
		db.session.commit()
		return redirect("/aktiv-parancsok")
	except:
		return "Nem sikerült törölni a parancsot!"


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)
