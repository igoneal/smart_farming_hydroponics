from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydrop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'slate'
app.config['SECRET_KEY'] = 'Password123'

admin = Admin(app, name='Hydroponics Monitor', template_mode='bootstrap3', url='/')
db = SQLAlchemy(app)


class Sensor(db.Model):  # defines the tables of same name
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    name = db.Column(db.String)
    pin = db.Column(db.Integer)


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    desc = db.Column(db.String)
    value = db.Column(db.Float)


admin.add_view(ModelView(Sensor, db.session))
admin.add_view(ModelView(Reading, db.session))
#app.route('/')
#def hello_world():  # put application's code here
 #   return render_template('index.html')


# if __name__ == '__main__':
#   app.run()
