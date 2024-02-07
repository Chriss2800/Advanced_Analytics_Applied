import os
import pandas as pd

from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, StringField

from excel_to_sql import FileToSQLite

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

FILE_LIST = [
    'ANACAMARGE_SYNTHESE.xlsx',
    'CA BENCH REPORTING FACTORIE.pdf',
    'CA HT CAROLINE.pdf',
    'CA MARKET CAROLINE SUPER.pdf',
    'CASSE CAROLINE.xlsx',
]

file_service = FileToSQLite()


class UploadFileForm(FlaskForm):
    file1 = FileField(FILE_LIST[0])
    file2 = FileField(FILE_LIST[1])
    file3 = FileField(FILE_LIST[2])
    file4 = FileField(FILE_LIST[3])
    file5 = FileField(FILE_LIST[4])
    week = StringField('Week')
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadFileForm()
    success_list = []

    if form.validate_on_submit():
        if request.method == 'POST':
            selected_week = request.form.get('date')
            print(selected_week)
        if request.files['file1'].filename == 'ANACAMARGE_SYNTHESE.xlsx':
            file1 = request.files['file1']
            file_service.process_anacamarge_synthese_xlsx(file1, selected_week)
            success_list.append(request.files['file1'].filename)
        if request.files['file2'].filename == 'CA BENCH REPORTING FACTORIE.pdf':
            file2 = request.files['file2']
            file_service.process_ca_bench_reporting_factorie_pdf(file2, selected_week)
            success_list.append(request.files['file2'].filename)
        if request.files['file3'].filename == 'CA HT CAROLINE.pdf':
            file3 = request.files['file3']
            file_service.process_ca_ht_caroline_pdf(file3, selected_week)
            success_list.append(request.files['file3'].filename)
        if request.files['file4'].filename == 'CA MARKET CAROLINE SUPER.pdf':
            file4 = request.files['file4']
            file_service.process_ca_market_caroline_super_pdf(file4, selected_week)
            success_list.append(request.files['file4'].filename)
        if request.files['file5'].filename == 'CASSE CAROLINE.xlsx':
            file5 = request.files['file5']
            file_service.process_casse_caroline_xlsx(file5, selected_week)
            success_list.append(request.files['file5'].filename)
        
            

            session['success_list'] = success_list
        return redirect(url_for('download'))

    return render_template("upload.html", form=form, file_list=FILE_LIST)


@app.route('/download', methods=['GET', 'POST'])
def download():
    success_list = session.get('success_list', [])

    return render_template("download.html", success_list=success_list)


if __name__ == '__main__':
    app.run(debug=True)
