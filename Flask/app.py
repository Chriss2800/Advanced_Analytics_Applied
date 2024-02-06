import os
import pandas as pd

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

from excel_to_sql import ExcelToSQLite

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

FILE_LIST = [
    'ANACAMARGE_SYNTHESE.xlsx',
    'CA BENCH REPORTING FACTORIE.pdf',
    'CA HT CAROLINE.pdf',
    'CA MARKET CAROLINE SUPER.pdf',
    'CASSE CAROLINE.xlsx',
]

excel_service = ExcelToSQLite()


class UploadFileForm(FlaskForm):
    file1 = FileField(FILE_LIST[0])
    file2 = FileField(FILE_LIST[1])
    file3 = FileField(FILE_LIST[2])
    file4 = FileField(FILE_LIST[3])
    file5 = FileField(FILE_LIST[4])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    html_table = ''
    form = UploadFileForm()

    if form.validate_on_submit():
        if request.files['file1'].filename == 'ANACAMARGE_SYNTHESE.xlsx':
            file1 = request.files['file1']
            excel_service.process_anacamarge_synthese_xlsx(file1)
        if request.files['file5'].filename == 'CASSE CAROLINE.xlsx':
            file5 = request.files['file5']
            excel_service.process_casse_caroline_xlsx(file5)

    return render_template("index.html", form=form, html_table=html_table, file_list=FILE_LIST)


if __name__ == '__main__':
    app.run(debug=True)
