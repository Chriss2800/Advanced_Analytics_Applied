import pandas as pd
import sqlite3
from datetime import datetime


class ExcelToSQLite():

    def __init__(self):
        self.sqlite_db_path = "database.db"

    def process_anacamarge_synthese_xlsx(self, excel_file):
        df = pd.read_excel(excel_file)
        print(df)

    def process_casse_caroline_xlsx(self, excel_file):
        sheet_names = pd.ExcelFile(excel_file).sheet_names

        for sheet_number in range(len(sheet_names)):
            sheet_name = f'Sheet{sheet_number+1}'
            df = pd.read_excel(excel_file, sheet_name, header=6)
            df = df.loc[:, ~df.columns.str.contains(
                "Unnamed: 0|Unnamed: 1|Unnamed: 4|Unnamed: 6")]
            df.rename(columns={'Unnamed: 2': "Index"}, inplace=True)

            # Extract the period from the xlsx --> should be removed with datepicker
            df['week'] = pd.read_excel(
                excel_file, sheet_name, header=None, usecols=[2], nrows=5).iloc[-1, 0]

            df['upload_date'] = pd.to_datetime(
                datetime.today().strftime('%d-%m-%Y'))

            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name=f"casse_caroline_{sheet_names[sheet_number]}", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()

    def process_pdf_and_insert_into_db(self, pdf_file):
        pass
