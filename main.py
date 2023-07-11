from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import random
import csv

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)

class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField(label='Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee = SelectField(label='Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    wifi = SelectField(label='Wifi Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    power = SelectField(label='Power Socket Availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField(label='Submit')

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")

## HTTP POST - Create Record

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

        with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
            csv_file.write(f'\n{form.cafe.data},'
                       f'{form.location.data},'
                       f'{form.open.data},'
                       f'{form.close.data},'
                       f'{form.coffee.data},'
                       f'{form.wifi.data},'
                       f'{form.power.data}')
        return redirect(url_for('cafes'))

    return render_template(template_name_or_list='add.html', form=form)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',') # csv.reader() method creates an iterable object, which we then iterate thru w a for loop (see below)
        list_of_rows = []
        for index, row in enumerate(csv_data): # CONTINUED FROM ABOVE... each iteration of the loop returns a row as a list of values which is printed to the console
            list_of_rows.append((index, row))
            print(row)
    return render_template('cafes.html', cafes=list_of_rows)

@app.route('/delete/<int:index>', methods=["POST"])
def delete(index):
    with open('cafe-data.csv', 'r', newline='', encoding='utf-8') as file:
        rows=list(csv.reader(file))
    del rows[index]

    with open('cafe-data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return redirect(url_for('cafes'))

if __name__ == '__main__':
    app.run(debug=True)