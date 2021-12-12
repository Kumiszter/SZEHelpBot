from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load, post_dump 
import json


from datetime import datetime


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


class Dates(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False, unique=True)
    event = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    def __init__(self, date, event):
        self.date = date
        self.event = event

class DatesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Dates
    id = auto_field()
    date = fields.DateTime('%Y.%b.%d', Required=True)	
    event = auto_field(Required=True)

    @post_load
    def make_date(self , data, **kwargs):
         return Dates(**data)


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
        

default_commands = ["!terkep", "!neptun", "!gyujtoszamla", "!linkek", "!to", "!datumok", "!szoctam"]


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parancs-letrehozas", methods=['POST', 'GET'])
def commandcreator():
    alap_commands = default_commands
    data = request.form
    if not request.method == 'POST':
      return render_template("commandcreator.html")
    if data['command'] in alap_commands:
      flash('alap command nev', category='error')
      return render_template("commandcreator.html")
    if not data['command'].startswith('!'):
      flash('commandnak "!"-kell kezdodnie', category='error')
      return render_template("commandcreator.html")
    commands_schema = CommandsSchema()
    dict_tpye = (commands_schema.dump(data))
    string_type = (json.dumps(dict_tpye))
    try:
      new_command = commands_schema.loads(string_type)
      db.session.add(new_command)
      db.session.commit()
      return redirect('/aktiv-parancsok')
    except:
      flash('ures mezo maradt', category='error')
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

#uj endpoint datum elerkezesenek
@app.route("/datum-letrehozas", methods=['POST', 'GET'])
def datecreator():
    data = request.form
    if not request.method == 'POST':
      return render_template("datecreator.html")
    dates_schema = DatesSchema(many=False)
    valami = json.dumps(data)
    valami2 = json.loads(valami)
    try:
        valami2['date'] = datetime.strptime(valami2['date'],'%Y.%m.%d')
    except:
        flash('rossz datum formatum (év.hónap.nap)' ,category='error')
        return render_template("datecreator.html")
    if valami2['date'] < datetime.today():
        flash('csak jövőbeni dátumot lehet megadni ', category='error')
        return render_template("datecreator.html")
    dict_tpye = (dates_schema.dump(valami2))
    string_type = (json.dumps(dict_tpye))
    print(string_type)
    try:
        new_date = dates_schema.loads(string_type)
        db.session.add(new_date)
        db.session.commit()
        return redirect('/aktiv-datumok')
    except:
        flash('ures mezo maradt', category='error')
        return render_template("datecreator.html")

@app.route("/datum-torles/<int:id>")
def delete_date(id):
    date_to_delete = Dates.query.get_or_404(id)
    try:
        db.session.delete(date_to_delete)
        db.session.commit()
        return redirect("/aktiv-datumok")
    except:
        return "Nem sikerült törölni a dátumot!"

@app.route("/aktiv-datumok")
def datelist():
    return render_template("dates.html", values=Dates.query.all())


if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)
