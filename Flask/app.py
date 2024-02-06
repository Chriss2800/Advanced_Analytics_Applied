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

#Input Form
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
    form = UploadFileForm()
    success_list = []  # List of sucessfull uploads

    if form.validate_on_submit():
        if request.files['file1'].filename == 'ANACAMARGE_SYNTHESE.xlsx':
            file1 = request.files['file1']
            excel_service.process_anacamarge_synthese_xlsx(file1) # processing and commiting of excel file, see excel_to_sql.py
            success_list.append(request.files['file1'].filename) #if sucessfull processed and uploaded, file name gets into the list of successfull uploads

        if request.files['file5'].filename == 'CASSE CAROLINE.xlsx':
            file5 = request.files['file5']
            excel_service.process_casse_caroline_xlsx(file5)# processing and commiting of excel file, see excel_to_sql.py
            success_list.append(request.files['file5'].filename)#if sucessfull processed and uploaded, file name gets into the list of successfull uploads
        
   
    # render index again while giving information about input form (form), file names (FILE_LIST) and a possible list of sucessfull uploads (success_list) if existing
    return render_template("index.html", form=form, file_list=FILE_LIST, success_list=success_list)


if __name__ == '__main__':
    app.run(debug=True)
