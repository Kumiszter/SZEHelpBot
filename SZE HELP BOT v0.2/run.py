from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_load, post_dump
import json


from datetime import datetime
from marshmallow.utils import timedelta_to_microseconds

from marshmallow_sqlalchemy.schema import auto_field

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commands.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(30), nullable=False, unique=True)
    title = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    output = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Name %r>' % self.id

    def __init__(self, command, title, name, output):
        self.command = command
        self.title = title
        self.name = name
        self.output = output
    #	self.date_created = date_created

class CommandsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Commands
    id = auto_field()
    command = auto_field(Required=True)	
    title = auto_field(Required=True)	
    name = auto_field(Required=True)	
    output = auto_field(Required=True)	

    @post_load
    def make_command(self, data, **kwargs):
        return Commands(**data)

    @post_dump
    def change_string_to_none(self, data, **kwargs):
        for field in data:
            if data[field] == "":
                data[field] = None
        return data
        


#seed? 
default_commands = ["!terkep", "!neptun", "!gyujtoszamla", "!linkek", "!to", "!datumok", "!szoctam"]

#Commands(command, title, name, output)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parancs-letrehozas", methods=['POST', 'GET'])
def commandcreator():
    alap_commands = default_commands
    data = request.form
    #TODO validate "!"" at the command start
    if request.method == 'POST' and data['command'] not in alap_commands:
        #TODO megnézni szebben? immutabledict->str
        commands_schema = CommandsSchema()
        dictes = (commands_schema.dump(data))
        string = (json.dumps(dictes))
        try:
            valami = commands_schema.loads(string)
            db.session.add(valami)
            db.session.commit()
        except:
            flash('ures mezo maradt', category='error')
        else:
            flash('alap command nev', category='error')
    return render_template("commandcreator.html")

@app.route("/aktiv-parancsok")
def commandlist():
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
    #db.create_all()
    app.run(debug=True)
