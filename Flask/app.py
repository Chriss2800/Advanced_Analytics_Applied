import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

FILE_LIST = [
    'ANACAMARGE_SYNTHESE',
    'CA BENCH REPORTING FACTORIE',
    'CA HT CAROLINE',
    'CA MARKET CAROLINE SUPER',
    'CASSE CAROLINE',
]


class UploadFileForm(FlaskForm):
    num_files = 5  # Anzahl der Dateifelder

    for i in range(num_files):
        locals()[f'file{i}'] = FileField(FILE_LIST[i])

    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    html_table = ''
    form = UploadFileForm()

    if form.validate_on_submit():
        for i in range(form.num_files):
            file_field = getattr(form, f'file{i}')
            file = file_field.data
            if file:
                df = pd.read_excel(file)
                html_table = df.to_html(index=False)

    return render_template("index.html", form=form, html_table=html_table)


if __name__ == '__main__':
    app.run(debug=True)
