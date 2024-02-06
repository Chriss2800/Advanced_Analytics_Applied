import pandas as pd
import sqlite3
import tabula
from datetime import datetime


class FileToSQLite():

    def __init__(self):
        self.sqlite_db_path = "database.db"

    def process_anacamarge_synthese_xlsx(self, excel_file):
        try:
            df = pd.read_excel(excel_file, header=[2, 3])
            df.rename(
                columns={
                    'Unnamed: 5': df.columns[4],
                    'Unnamed: 6': df.columns[4],
                    'Unnamed: 8': df.columns[7],
                    'Unnamed: 9': df.columns[7],
                    'Unnamed: 11': df.columns[10],
                    'Unnamed: 12': df.columns[10],
                }, inplace=True)
            column_names = [
                ' '.join(filter(pd.notna, col)) for col in df.columns]
            df.columns = [col.replace('.', '') for col in column_names]
            df = df.drop([df.columns[0], df.columns[3]], axis=1)
            df.rename(
                columns={
                    'Unnamed: 1_level_0 Unnamed: 1_level_1': 'Id',
                    'Unnamed: 2_level_0 Unnamed: 2_level_1': 'Category'
                }, inplace=True)
            df = df.iloc[:-2]
            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name="anacamarge_synthese", con=connection,
                      if_exists="append", index=False)

            df['upload_date'] = pd.to_datetime(
                datetime.today().strftime('%d-%m-%Y'))

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error: {e}")

    def process_ca_bench_reporting_factorie_pdf(self, pdf_file):
        pass

    def process_ca_ht_caroline_pdf(self, pdf_file):
        pass

    def process_ca_market_caroline_super_pdf(self, pdf_file):
        pass

    def process_casse_caroline_xlsx(self, excel_file):
        try:
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

        except Exception as e:
            print(f"Error: {e}")


file_service = FileToSQLite()
dfs = tabula.read_pdf("CA BENCH REPORTING FACTORIE.pdf",
                      pages=1, multiple_tables=False)
df = dfs[0]
df.columns = df.iloc[0]
df = df.drop(0)
print(type(df))
