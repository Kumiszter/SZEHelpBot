from asyncio import FastChildWatcher
from crypt import methods
from operator import iconcat
from typing_extensions import Required
from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load, post_dump 
import json


from datetime import datetime, timedelta


from marshmallow_sqlalchemy.schema import auto_field

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commands.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

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

class EventParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #type 0=esemény 1=időtartam
    type = db.Column(db.Integer, nullable=False)
    input_int = db.Column(db.Integer, nullable=False)

    def __init__(self,type,input_int):
        self.type = type
        self.input_int = input_int
#------------------------------------------ üdvözlő üzenet blokk -----------------------------------------------------
class Welcome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
    direct_message = db.Column(db.String(100))
    send_channel = db.Column(db.Boolean, unique=False, default=True)
    send_dm = db.Column(db.Boolean, unique=False, default=True)
    def __repr__(self):
        return '<Name %r>' % self.id
    def __init__(self, message, direct_message, send_channel, send_dm):
        self.message = message
        self.direct_message = direct_message
        self.send_channel = send_channel
        self.send_dm = send_dm
#------------------------------------------ üdvözlő üzenet blokk -----------------------------------------------------
class Emojis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)

    def __init__(self, role, icon,channel_id):
        self.role = role
        self.icon = icon

class Channels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)
    channel_id = db.Column(db.String(100), nullable=False)

    def __init__(self,event,channel_id):
        self.event = event
        self.channel_id = channel_id

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

class EmojisSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Emojis
    id = auto_field()
    icon = auto_field(Required=True)
    role = auto_field(Required=True)

    @post_load
    def make_date(self , data, **kwargs):
         return Emojis(**data)

class EventParamSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventParam
    id = auto_field()
    type = auto_field(Required=True)
    input_int = auto_field(Required=True)

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
    string_data = json.dumps(data)
    dict_data = json.loads(string_data)
    try:
        dict_data['date'] = datetime.strptime(dict_data['date'],'%Y.%m.%d')
    except:
        flash('rossz datum formatum (év.hónap.nap)' ,category='error')
        return render_template("datecreator.html")
    if dict_data['date'] < datetime.today():
        flash('csak jövőbeni dátumot lehet megadni ', category='error')
        return render_template("datecreator.html")
    dict_tpye = (dates_schema.dump(dict_data))
    string_type = (json.dumps(dict_tpye))
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

#TODO aktuális paramétert kiírni
@app.route("/aktiv-datumok", methods=['POST','GET'])
def datelist():
    if not request.method == 'POST':          
        dates = Dates.query.all()
        now = datetime.now()
        for date in dates:
            if date.date < now:
                try:
                    db.session.delete(date)
                    db.session.commit()
                except:
                    return "nem sikerült a törlés"
        return render_template("dates.html", values=Dates.query.all())
    else:
        data = request.form
        dates = Dates.query.all()
        curr_param = EventParam.query.all()
        curr_param[0].input_int = data['input_int']
        curr_param[0].type = data['param']
        try:
            db.session.commit()
        except:
            print("error")
            db.session.rollback()
        return render_template("dates.html", values=Dates.query.all())

#------------------------------------------ üdvözlő üzenet blokk -----------------------------------------------------
@app.route("/udvozlo-uzenet", methods=['GET', 'POST'])
def welcome():
    welcome_update = Welcome.query.first()
    if welcome_update is None:
        welcome_update = Welcome("", "", True, True)

    if request.method == "POST":
        # Channel üdvözlés legyen-e
        if request.form.get('disable_channel'):
            print("send channel message false")
            welcome_update.send_channel = False
        else:
            print("send channel message true")
            welcome_update.send_channel = True
        # DM üdvözlés legyen-e
        if request.form.get('disable_dm'):
            print("send direct message false")
            welcome_update.send_dm = False
        else:
            print("send direct message true")
            welcome_update.send_dm = True 

        welcome_update.message = request.form["message"]
        welcome_update.direct_message = request.form["direct_message"]
        db.session.add(welcome_update)
        db.session.commit()
        return render_template("welcome.html", welcome_update=welcome_update)
    else:
        return render_template("welcome.html", welcome_update=welcome_update)
#------------------------------------------ üdvözlő üzenet blokk -----------------------------------------------------
#TODO szebben/hibakezeles/input kezeles
@app.route("/role-adas", methods=['GET', 'POST'])
def role():
    if request.method == 'POST':
        data = request.form
        string_data = json.dumps(data)
        dict_data = json.loads(string_data)
        for key,_ in dict_data.items():
            emoji = Emojis.query.filter_by(role=key).all()
            for e in emoji:
                e.icon = dict_data[key]
        try:
            db.session.commit()
        except:
            print("hiba")
            db.session.rollback()
        return render_template("role.html")
    return render_template("role.html")

@app.route("/channel", methods=['GET', 'POST'])
def chanel():
    if request.method == 'POST':
        data = request.form
        found_event = Channels.query.filter_by(event=data['event']).all()
        if found_event:
            if not found_event[0].event == 'task_loop':
                found_event[0].channel_id = data['channel']
            else:
                found_event[0].channel_id = data['task_loop_time']
            try:
                db.session.commit()
            except:
                print("error")
                db.session.rollback()
        return render_template("channel.html")
    return render_template("channel.html")
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
