from flask import Flask, render_template, flash, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired('Enter a Cafe name!')])
    cafe_url = StringField(label='Cafe location on Google maps(URL)', validators=[DataRequired('Enter a valid URL!'),
                                                                                  URL(message='Invalid URL!')])
    open_time = StringField(label='Opening Time e.g(8:00AM)', validators=[DataRequired('Enter a Cafe opening time!')])
    close_time = StringField(label='Close Time e.g(10:00PM)', validators=[DataRequired('Enter a Cafe closing time!')])
    coffee_rating = SelectField(
        label='Coffee rating',
        choices=['✘', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'],
        validators=[DataRequired('Please select a field!')],
        render_kw={'style': 'width: 16ch'}
    )
    wifi = SelectField(
        label='WiFi',
        choices=['✘', '📶', '📶📶', '📶📶📶', '📶📶📶📶'],
        validators=[DataRequired('Please select a field!')],
        render_kw={'style': 'width: 16ch'}
    )
    power_socketing = SelectField(
        label='WiFi',
        choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌'],
        validators=[DataRequired('Please select a field!')],
        render_kw={'style': 'width: 16ch'}
    )
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪//🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm(meta={'csrf': True})
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding="utf8") as csv_file:
            csv_file.write(f'\n{form.cafe.data},{form.cafe_url.data},{form.open_time.data},'
                           f'{form.close_time.data},{form.coffee_rating.data},{form.wifi.data},'
                           f'{form.power_socketing.data}')
            flash('Data added!!!')
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # for the csv file
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        # uses the csv module to read the file
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        # print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
